#!/usr/bin/env python3

import argparse
import curses
import csv
import json
import os
import re
import shutil
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple


SEPARATOR_RE = re.compile(r"^=+$")


def parse_transcript_file(path: Path) -> dict:
    metadata = {}
    body_lines = []
    in_body = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if SEPARATOR_RE.match(line.strip()):
            in_body = True
            continue
        if not in_body:
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
            continue
        body_lines.append(line)

    return {
        "machine_text": "\n".join(body_lines).strip(),
        "selected_pass": metadata.get("Selected Pass", ""),
        "detected_lang": metadata.get("Detected Lang", ""),
        "avg_logprob": metadata.get("Avg Logprob", ""),
    }


def load_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {"last_filename": None, "records": {}}
    with state_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=True, indent=2, sort_keys=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_metadata(metadata_csv: Path) -> dict:
    if not metadata_csv.exists():
        return {}
    with metadata_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {row["filename"]: row["text"] for row in reader if row.get("filename")}


def write_metadata(metadata_csv: Path, rows: dict) -> None:
    metadata_csv.parent.mkdir(parents=True, exist_ok=True)
    with metadata_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["filename", "text"])
        writer.writeheader()
        for filename in sorted(rows):
            writer.writerow({"filename": filename, "text": rows[filename]})


def ensure_corrected_dataset(corrected_audio_dir: Path, metadata_csv: Path) -> None:
    corrected_audio_dir.mkdir(parents=True, exist_ok=True)
    if not metadata_csv.exists():
        write_metadata(metadata_csv, {})


def discover_items(raw_dir: Path, output_dir: Path, corrected_audio_dir: Path) -> list:
    items = []
    for audio_path in sorted(raw_dir.iterdir()):
        if not audio_path.is_file() or audio_path.name.startswith("."):
            continue
        if audio_path.suffix.lower() != ".wav":
            continue
        stem = audio_path.stem
        transcript_path = output_dir / f"{stem}_transcript.txt"
        timestamps_path = output_dir / f"{stem}_timestamps.txt"
        parsed = {
            "machine_text": "",
            "selected_pass": "",
            "detected_lang": "",
            "avg_logprob": "",
        }
        if transcript_path.exists():
            parsed = parse_transcript_file(transcript_path)

        items.append(
            {
                "filename": audio_path.name,
                "audio_path": audio_path,
                "transcript_path": transcript_path,
                "timestamps_path": timestamps_path,
                "corrected_audio_path": corrected_audio_dir / audio_path.name,
                **parsed,
            }
        )
    return items


def find_start_index(items: list, last_filename: Optional[str], start_from: Optional[str]) -> int:
    target = start_from or last_filename
    if not target:
        return 0
    for idx, item in enumerate(items):
        if item["filename"] == target:
            return idx
    return 0


def play_audio(audio_path: Path) -> None:
    player = shutil.which("afplay")
    if not player:
        print("Audio playback unavailable: `afplay` not found.")
        return
    subprocess.run([player, str(audio_path)], check=False)


def normalize_text(text: str) -> str:
    return " ".join(text.splitlines()).strip()


def wrap_block(text: str, width: int) -> list:
    lines = []
    for paragraph in (text or "").splitlines() or [""]:
        wrapped = textwrap.wrap(
            paragraph,
            width=width,
            replace_whitespace=False,
            drop_whitespace=False,
        )
        lines.extend(wrapped or [""])
    return lines or [""]


def show_popup(stdscr: "curses._CursesWindow", title: str, text: str) -> None:
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    usable_width = max(20, width - 2)

    row = 0
    stdscr.addnstr(row, 0, title, usable_width, curses.A_BOLD)
    row += 2

    wrapped = wrap_block(text, usable_width)
    max_body = max(1, height - 4)
    for line in wrapped[:max_body]:
        stdscr.addnstr(row, 0, line, usable_width)
        row += 1

    if len(wrapped) > max_body:
        stdscr.addnstr(row, 0, "...", usable_width, curses.A_DIM)
        row += 1

    if row < height:
        stdscr.addnstr(row, 0, "Press any key to return.", usable_width, curses.A_DIM)
    stdscr.refresh()
    stdscr.get_wch()


def launch_editor(
    item: dict,
    initial_text: str,
    index: int,
    total: int,
    accepted_count: int,
) -> Tuple[str, str]:
    machine_text = normalize_text(item["machine_text"]) or "[no machine transcript found]"
    starting_text = normalize_text(initial_text)

    def _run(stdscr: "curses._CursesWindow") -> Tuple[str, str]:
        try:
            curses.curs_set(1)
        except curses.error:
            pass
        stdscr.keypad(True)
        caret_attr = curses.A_REVERSE | curses.A_BOLD

        text = starting_text
        cursor = len(text)
        scroll = 0

        while True:
            stdscr.erase()
            height, width = stdscr.getmaxyx()
            usable_width = max(20, width - 1)

            row = 0

            def add_line(value: str, attr: int = 0) -> None:
                nonlocal row
                if row >= height - 1:
                    return
                stdscr.addnstr(row, 0, value, usable_width, attr)
                row += 1

            add_line("=" * min(usable_width, 72), curses.A_DIM)
            add_line(f"[{index + 1}/{total}] {item['filename']}", curses.A_BOLD)
            add_line(f"Accepted    : {accepted_count}")
            add_line(f"Audio       : {item['audio_path']}")
            add_line(
                f"Transcript  : {item['transcript_path'] if item['transcript_path'].exists() else 'missing'}"
            )
            add_line(
                f"Timestamps  : {item['timestamps_path'] if item['timestamps_path'].exists() else 'missing'}"
            )
            if item["selected_pass"]:
                add_line(f"Pass/Lang   : {item['selected_pass']} | {item['detected_lang']} | {item['avg_logprob']}")

            add_line("")
            add_line("Machine transcript:", curses.A_BOLD)
            reserved_rows = 5
            max_machine_rows = max(3, height - row - reserved_rows)
            machine_lines = wrap_block(machine_text, usable_width)
            for line in machine_lines[:max_machine_rows]:
                add_line(line)
            if len(machine_lines) > max_machine_rows:
                add_line("... Ctrl-T shows the full transcript", curses.A_DIM)

            add_line("")
            prompt = "corrected> "
            edit_width = max(10, usable_width - len(prompt))
            if cursor < scroll:
                scroll = cursor
            if cursor >= scroll + edit_width:
                scroll = cursor - edit_width + 1
            visible_text = text[scroll : scroll + edit_width]

            if row < height - 1:
                stdscr.addnstr(row, 0, prompt, usable_width, curses.A_BOLD)
                stdscr.addnstr(row, len(prompt), visible_text, edit_width)
                cursor_offset = cursor - scroll
                cursor_x = min(usable_width - 1, len(prompt) + cursor_offset)
                if 0 <= cursor_offset < edit_width:
                    caret_char = text[cursor] if cursor < len(text) else " "
                    stdscr.addnstr(row, len(prompt) + cursor_offset, caret_char, 1, caret_attr)
                stdscr.move(row, cursor_x)
                row += 1

            add_line("Enter accept | Ctrl-R replay | Ctrl-K skip | Ctrl-P back | Ctrl-Q quit | Ctrl-T transcript", curses.A_DIM)
            stdscr.refresh()

            key = stdscr.get_wch()

            if key in ("\n", "\r") or key == curses.KEY_ENTER:
                return ("accept", text.strip())
            if key == "\x12":
                return ("replay", text)
            if key == "\x0b":
                return ("skip", text)
            if key == "\x10":
                return ("back", text)
            if key == "\x11":
                return ("quit", text)
            if key == "\x14":
                show_popup(stdscr, "Machine transcript", machine_text)
                continue

            if key in (curses.KEY_LEFT, "\x02"):
                cursor = max(0, cursor - 1)
                continue
            if key in (curses.KEY_RIGHT, "\x06"):
                cursor = min(len(text), cursor + 1)
                continue
            if key in (curses.KEY_HOME, "\x01"):
                cursor = 0
                continue
            if key in (curses.KEY_END, "\x05"):
                cursor = len(text)
                continue
            if key in (curses.KEY_BACKSPACE, "\x08", "\x7f"):
                if cursor > 0:
                    text = text[: cursor - 1] + text[cursor:]
                    cursor -= 1
                continue
            if key == curses.KEY_DC:
                if cursor < len(text):
                    text = text[:cursor] + text[cursor + 1 :]
                continue
            if key == curses.KEY_RESIZE:
                continue

            if isinstance(key, str) and key.isprintable():
                text = text[:cursor] + key + text[cursor:]
                cursor += len(key)

    return curses.wrapper(_run)


def update_metadata_and_move(
    item: dict,
    corrected_text: str,
    corrected_audio_dir: Path,
    metadata_csv: Path,
    metadata_rows: dict,
    keep_output_files: bool,
) -> None:
    corrected_audio_dir.mkdir(parents=True, exist_ok=True)
    target_audio = corrected_audio_dir / item["filename"]

    if item["audio_path"].exists():
        shutil.move(str(item["audio_path"]), str(target_audio))

    metadata_rows[item["filename"]] = corrected_text
    write_metadata(metadata_csv, metadata_rows)

    if not keep_output_files:
        item["transcript_path"].unlink(missing_ok=True)
        item["timestamps_path"].unlink(missing_ok=True)


def build_state_record(item: dict, corrected_text: str, skipped: bool, completed: bool, notes: str = "") -> dict:
    return {
        "machine_text": item["machine_text"],
        "corrected_text": corrected_text,
        "notes": notes,
        "skipped": skipped,
        "completed": completed,
        "last_updated": now_iso(),
    }


def run_reviewer(args: argparse.Namespace) -> int:
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)
    corrected_dir = Path(args.corrected_dir)
    corrected_audio_dir = corrected_dir / "audio"
    metadata_csv = corrected_dir / "metadata.csv"
    state_path = Path(args.state_file)

    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")

    ensure_corrected_dataset(corrected_audio_dir, metadata_csv)
    if not state_path.exists():
        save_state(state_path, {"last_filename": None, "records": {}})

    items = discover_items(raw_dir, output_dir, corrected_audio_dir)
    if not items:
        print("No pending WAV files found in data/raw.")
        return 0

    state = load_state(state_path)
    metadata_rows = load_metadata(metadata_csv)
    index = find_start_index(items, state.get("last_filename"), args.start_from)

    if not args.no_autoplay:
        play_audio(items[index]["audio_path"])

    while items:
        item = items[index]
        record = state["records"].get(item["filename"], {})
        draft_text = record.get("corrected_text") or item["machine_text"]
        while True:
            action, corrected_text = launch_editor(
                item=item,
                initial_text=draft_text,
                index=index,
                total=len(items),
                accepted_count=len(metadata_rows),
            )

            if action == "replay":
                draft_text = corrected_text
                play_audio(item["audio_path"])
                continue

            if action == "skip":
                state["records"][item["filename"]] = build_state_record(
                    item=item,
                    corrected_text=corrected_text,
                    skipped=True,
                    completed=False,
                    notes=record.get("notes", ""),
                )
                index = (index + 1) % len(items)
                state["last_filename"] = items[index]["filename"]
                save_state(state_path, state)
                if not args.no_autoplay:
                    play_audio(items[index]["audio_path"])
                break

            if action == "back":
                state["records"][item["filename"]] = build_state_record(
                    item=item,
                    corrected_text=corrected_text,
                    skipped=record.get("skipped", False),
                    completed=False,
                    notes=record.get("notes", ""),
                )
                index = (index - 1) % len(items)
                state["last_filename"] = items[index]["filename"]
                save_state(state_path, state)
                if not args.no_autoplay:
                    play_audio(items[index]["audio_path"])
                break

            if action == "quit":
                state["records"][item["filename"]] = build_state_record(
                    item=item,
                    corrected_text=corrected_text,
                    skipped=record.get("skipped", False),
                    completed=False,
                    notes=record.get("notes", ""),
                )
                state["last_filename"] = item["filename"]
                save_state(state_path, state)
                print(f"Progress saved to {state_path}")
                return 0

            if not corrected_text:
                print("Empty correction not saved. Type the transcript or use Ctrl-K to skip.")
                draft_text = corrected_text
                continue

            update_metadata_and_move(
                item=item,
                corrected_text=corrected_text,
                corrected_audio_dir=corrected_audio_dir,
                metadata_csv=metadata_csv,
                metadata_rows=metadata_rows,
                keep_output_files=args.keep_output_files,
            )

            state["records"][item["filename"]] = build_state_record(
                item=item,
                corrected_text=corrected_text,
                skipped=False,
                completed=True,
            )

            items.pop(index)
            if not items:
                state["last_filename"] = None
                save_state(state_path, state)
                print("All pending clips reviewed.")
                return 0

            index = min(index, len(items) - 1)
            state["last_filename"] = items[index]["filename"]
            save_state(state_path, state)
            if not args.no_autoplay:
                play_audio(items[index]["audio_path"])
            break

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Interactive correction tool for building Whisper fine-tuning data incrementally."
    )
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--output-dir", default="data/output")
    parser.add_argument("--corrected-dir", default="data/corrected")
    parser.add_argument("--state-file", default="data/correction_state.json")
    parser.add_argument("--no-autoplay", action="store_true")
    parser.add_argument("--keep-output-files", action="store_true")
    parser.add_argument("--start-from")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_reviewer(args)


if __name__ == "__main__":
    raise SystemExit(main())
