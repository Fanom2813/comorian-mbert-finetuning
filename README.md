# Comorian mBERT/XLM-RoBERTa Fine-tuning on Google Colab

Fine-tune multilingual BERT models (mBERT or XLM-RoBERTa) for the Comorian language using Google Colab's free GPU. Perfect for low-resource language processing!

## 🎯 Project Overview

This project helps you:
- **Fine-tune XLM-RoBERTa** on Comorian language data
- **Use Google Colab** (free GPU, no setup needed)
- **Process story-based data** for better language learning
- **Train custom models** in 2-4 hours
- **Save models** to Google Drive for later use

## 🚀 Quick Start

### Option 1: Open in Google Colab (Easiest)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Fanom2813/comorian-mbert-finetuning/blob/main/Comorian_XLM_RoBERTa_Finetuning.ipynb)

**Steps:**
1. Click the badge above or [this link](https://colab.research.google.com/github/Fanom2813/comorian-mbert-finetuning/blob/main/Comorian_XLM_RoBERTa_Finetuning.ipynb)
2. Go to **Runtime > Change runtime type > Select GPU**
3. Run cells sequentially from top to bottom
4. When prompted, authenticate with your Google account
5. Upload your Comorian data (or use sample data)
6. Wait for training to complete (~2-4 hours with GPU)
7. Model is saved to Google Drive automatically

### Option 2: Local Setup

```bash
# Clone the repository
git clone https://github.com/Fanom2813/comorian-mbert-finetuning.git
cd comorian-mbert-finetuning

# Install dependencies
pip install -r requirements.txt

# Prepare your data
python data_preparation.py --input raw_stories.txt --output processed_stories.txt

# Run the notebook locally
jupyter notebook Comorian_XLM_RoBERTa_Finetuning.ipynb
```

## 📁 Project Structure

```
comorian-mbert-finetuning/
├── Comorian_XLM_RoBERTa_Finetuning.ipynb  # Main Colab notebook
├── data_preparation.py                     # Data cleaning script
├── requirements.txt                        # Python dependencies
├── README.md                              # This file
├── LICENSE                                # MIT License
└── data/
    ├── raw/
    │   └── sample_data.txt                # Example stories
    └── processed/
        └── (your cleaned data goes here)
```

## 📝 Data Format

### Input: Raw Stories

Stories should be in plain text (.txt) files, one story per file or separated by blank lines:

```
Hadithi ya Juma

Siku moja, Juma alikuwa anabakabaika jijini. 
Alikuwa ana njaa sana lakini hana pesa...

---

Hadithi ya Fatima

Fatima alikuwa msichana mdogo lakini ana ndoto kubwa...
```

### Output: Processed Data

After preparation, data is formatted as one sentence/paragraph per line:

```
Hadithi ya Juma
Siku moja, Juma alikuwa anabakabaika jijini.
Alikuwa ana njaa sana lakini hana pesa.
Alitembea kwenye barabara na kumkuta rafiki yake Salim.
```

## 🔧 Data Preparation

### Using the Script

```bash
python data_preparation.py \
    --input data/raw/your_stories.txt \
    --output data/processed/prepared_stories.txt \
    --min_length 5 \
    --max_length 512
```

### Or in Colab

The notebook includes automatic data preparation. Just upload your file!

## 📊 Training Configuration

Default settings in the notebook:

- **Model:** XLM-RoBERTa-base (recommended for Comorian)
- **Epochs:** 3-5
- **Batch Size:** 8 (adjustable based on GPU)
- **Learning Rate:** 2e-5
- **Block Size:** 256 tokens
- **GPU:** T4 (free on Colab)

### Adjust for Your Needs:

| Parameter | For More Data | For Less Data |
|-----------|---------------|--------------|
| Epochs | 2-3 | 5-10 |
| Batch Size | 16-32 | 4-8 |
| Learning Rate | 5e-5 | 1e-5 |

## 💾 Saving & Loading Your Model

### After Training (Automatic in Colab)

Model is saved to:
```
Google Drive/comorian-xlm-roberta-finetuned/
```

### Load Later

```python
from transformers import AutoTokenizer, AutoModel

model_path = "path/to/comorian-xlm-roberta-finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

# Use for predictions
text = "Habari yako?"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
```

## 📚 Data Collection Tips

### Where to Find Comorian Text:

1. **Traditional Stories** - Collect from elders/communities
2. **Social Media** - Twitter, Facebook (with permission)
3. **News** - Comorian news websites
4. **Literature** - Books and educational materials
5. **Web Resources** - Wikipedia, blogs (if available in Comorian)
6. **Back-translation** - Translate from Swahili/French using Google Translate

### Minimum Data Requirements:

- **Minimum:** 10,000 sentences (~50K words)
- **Good:** 50,000+ sentences (~250K words)
- **Excellent:** 100,000+ sentences (~500K words)

## 🎯 Next Steps After Training

### 1. Fine-tune for Specific Tasks

```python
from transformers import AutoModelForSequenceClassification

# Text Classification
model = AutoModelForSequenceClassification.from_pretrained(
    "path/to/your/model",
    num_labels=2
)

# Named Entity Recognition (NER)
model = AutoModelForTokenClassification.from_pretrained(
    "path/to/your/model",
    num_labels=5  # O, PER, LOC, ORG, MISC
)
```

### 2. Create Downstream Task Datasets

- Text classification (sentiment, intent)
- Named entity recognition
- Question answering
- Text generation

### 3. Publish Your Model

Share your fine-tuned model on [Hugging Face Model Hub](https://huggingface.co/models):

```python
model.push_to_hub("comorian-xlm-roberta-finetuned", use_auth_token=True)
tokenizer.push_to_hub("comorian-xlm-roberta-finetuned", use_auth_token=True)
```

## 🛠️ Troubleshooting

### GPU Out of Memory

- Reduce batch size (8 → 4)
- Reduce block size (256 → 128)
- Use gradient accumulation

### Slow Training

- Normal! GPU training takes time
- Monitor progress in the notebook
- Estimated: 2-4 hours for 50K sentences

### Data Not Loading

- Check file encoding (should be UTF-8)
- Verify file path is correct
- Check for special characters in filename

## 📖 Resources

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/)
- [XLM-RoBERTa Paper](https://arxiv.org/abs/1911.02116)
- [BERT Fine-tuning Guide](https://huggingface.co/docs/transformers/training)
- [mBERT on Hugging Face](https://huggingface.co/bert-base-multilingual-cased)
- [XLM-RoBERTa on Hugging Face](https://huggingface.co/xlm-roberta-base)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Have improvements? Found issues?

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💬 Support

- **Questions?** Open an issue in the repository
- **Want to share results?** Start a discussion
- **Found a bug?** Report it with details

## 🎓 Citation

If you use this project in your research, please cite:

```bibtex
@software{comorian_mbert_2026,
  title={Comorian mBERT/XLM-RoBERTa Fine-tuning on Google Colab},
  author={Fanom2813},
  year={2026},
  url={https://github.com/Fanom2813/comorian-mbert-finetuning}
}
```

## 📢 Acknowledgments

- Hugging Face for the Transformers library
- Google for Colab GPU access
- The Comorian language community

---

**Happy fine-tuning! 🚀 If you find this helpful, please star the repository!**