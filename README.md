# BBS-AIIM - Natural Language Processing Course Materials

This repository contains comprehensive materials for a Natural Language Processing (NLP) course, organized into progressive modules covering both classical and modern NLP techniques. The content is designed for learning text processing, machine learning applications in NLP, and state-of-the-art embedding methods.

## Repository Structure

The course is organized into the following main modules:

### Module 1: Text Preprocessing and Fundamentals
- **[01_Text_Preprocessing_Pipeline.ipynb](BBS-AIIM/module1/01_Text_Preprocessing_Pipeline.ipynb)** - Complete text preprocessing pipeline using spaCy and NLTK
  - Multilingual text processing (English and Italian)
  - Tokenization, stop word removal, stemming vs lemmatization
  - POS tagging and Named Entity Recognition (NER)
  - Performance comparison between NLTK and spaCy
  
- **[02_Modern_Tokenization_Comparison.ipynb](BBS-AIIM/module1/02_Modern_Tokenization_Comparison.ipynb)** - Modern tokenization techniques
- **[03_Advanced_spaCy_Features.ipynb](BBS-AIIM/module1/03_Advanced_spaCy_Features.ipynb)** - Advanced spaCy functionalities

### Module 2: Traditional NLP Techniques and Embeddings
- **[01-N-grams.ipynb](BBS-AIIM/module2/01-N-grams.ipynb)** - N-gram language models
- **[02-Bag-of-Words.ipynb](BBS-AIIM/module2/02-Bag-of-Words.ipynb)** - Bag of Words implementation with sklearn
  - Manual BoW implementation
  - CountVectorizer usage
  - TF-IDF vectorization
  
- **[03-Text-Classification-Project.ipynb](BBS-AIIM/module2/03-Text-Classification-Project.ipynb)** - Practical text classification project
- **[04_Feature_Engineering_Text_Data.ipynb](BBS-AIIM/module2/04_Feature_Engineering_Text_Data.ipynb)** - Feature engineering for text data
- **[05_Word-Vectors.ipynb](BBS-AIIM/module2/05_Word-Vectors.ipynb)** - Word2Vec and traditional word embeddings
- **[06_Word-Vectors-GloVe.ipynb](BBS-AIIM/module2/06_Word-Vectors-GloVe.ipynb)** - GloVe embeddings
- **[07_Sentence-Transformers-Embeddings.ipynb](BBS-AIIM/module2/07_Sentence-Transformers-Embeddings.ipynb)** - Modern transformer-based embeddings
  - Sentence-Transformers library usage
  - Semantic similarity and search
  - Multilingual models
  - Clustering and duplicate detection
  - Visualization with t-SNE

### Module 3: Advanced Topics
- Directory exists but content to be added

### Module 4: Modern Language Models and Generation
- **[01_Text_Generation.ipynb](BBS-AIIM/module4/01_Text_Generation.ipynb)** - Text generation with GPT models
  - Understanding decoder architectures (GPT vs BERT)
  - Autoregressive text generation
  - Sampling strategies (temperature, top-k, top-p)
  - Generation quality metrics (perplexity, diversity, BLEU, ROUGE)
  - Controlled generation and prompt engineering
  
- **[NLP14_1_RAG_Pipeline.ipynb](BBS-AIIM/module4/NLP14_1_RAG_Pipeline.ipynb)** - Retrieval-Augmented Generation (RAG)
- **[NLP14_2_Modern_LLMs.ipynb](BBS-AIIM/module4/NLP14_2_Modern_LLMs.ipynb)** - Working with modern LLMs
- **[NLP14_2_Modern_LLMs_Gemini.ipynb](BBS-AIIM/module4/NLP14_2_Modern_LLMs_Gemini.ipynb)** - Google Gemini integration


## Technologies and Libraries Used

- **Python Libraries:**
  - `spaCy` - Industrial-strength NLP
  - `NLTK` - Natural Language Toolkit
  - `scikit-learn` - Machine learning tools
  - `sentence-transformers` - Modern embeddings
  - `pandas` - Data manipulation
  - `matplotlib` / `seaborn` - Data visualization
  - `numpy` - Numerical computing

## Prerequisites

- Python 3.7+
- Basic understanding of Python programming
- Familiarity with machine learning concepts (helpful but not required)

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd BBS-AIIM
```

2. Install required packages:
```bash
pip install spacy nltk scikit-learn sentence-transformers pandas matplotlib seaborn
```

3. Download spaCy language models:
```bash
python -m spacy download en_core_web_sm
python -m spacy download it_core_news_sm
```

4. Start with Module 1 notebooks and progress sequentially


## Useful Resources

- [spaCy Documentation](https://spacy.io/)
- [NLTK Documentation](https://www.nltk.org/)
- [Sentence-Transformers Documentation](https://www.sbert.net/)
- [Hugging Face Model Hub](https://huggingface.co/models?library=sentence-transformers)

## Contributing

This is an educational repository. If you find errors or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

Educational materials for learning purposes. Check individual notebooks for specific licensing information.

---

**Note:** All notebooks are designed to run in Google Colab (note the Colab badges), but can also be executed in local Jupyter environments with proper setup.