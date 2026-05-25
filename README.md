# BBS-AIIM - Natural Language Processing and AI Course Materials

This repository contains comprehensive materials for a Natural Language Processing and AI course, organized into progressive modules covering classical NLP techniques through modern AI applications. The content spans from basic text processing to advanced multi-agent systems and fine-tuning techniques.

## Repository Structure

### Module 1: Text Preprocessing and Fundamentals
- **[01_Text_Preprocessing_Pipeline.ipynb](module1/01_Text_Preprocessing_Pipeline.ipynb)** - Complete preprocessing pipeline using spaCy and NLTK
- **[02_Modern_Tokenization_Comparison.ipynb](module1/02_Modern_Tokenization_Comparison.ipynb)** - Modern tokenization techniques  
- **[03_Advanced_spaCy_Features.ipynb](module1/03_Advanced_spaCy_Features.ipynb)** - Advanced spaCy functionalities

### Module 2: Traditional NLP and Embeddings
- **[01-N-grams.ipynb](module2/01-N-grams.ipynb)** - N-gram language models
- **[02-Bag-of-Words.ipynb](module2/02-Bag-of-Words.ipynb)** - BoW implementation with sklearn
- **[03-Text-Classification-Project.ipynb](module2/03-Text-Classification-Project.ipynb)** - Practical text classification
- **[04_Feature_Engineering_Text_Data.ipynb](module2/04_Feature_Engineering_Text_Data.ipynb)** - Feature engineering techniques
- **[05_Word-Vectors.ipynb](module2/05_Word-Vectors.ipynb)** - Word2Vec embeddings
- **[06_Word-Vectors-GloVe.ipynb](module2/06_Word-Vectors-GloVe.ipynb)** - GloVe embeddings
- **[07_Sentence-Transformers-Embeddings.ipynb](module2/07_Sentence-Transformers-Embeddings.ipynb)** - Modern transformer embeddings

### Module 3: Deep Learning and Transformers
- **[01-LSTM_for_Classification.ipynb](module3/01-LSTM_for_Classification.ipynb)** - LSTM text classification
- **[02-Classification with Transformers.ipynb](module3/02-Classification%20with%20Transformers.ipynb)** - Transformer-based classification
- **[03-Huggingface_intro.ipynb](module3/03-Huggingface_intro.ipynb)** - Hugging Face ecosystem introduction
- **[04-Q&A with finetuned BERT.ipynb](module3/04-Q%26A%20with%20finetuned%20BERT%20.ipynb)** - BERT fine-tuning for question answering

### Module 4: Language Models and Generation
- **[01_Text_Generation.ipynb](module4/01_Text_Generation.ipynb)** - GPT-based text generation with sampling strategies
- **[02_Exploring_Modern_LLMs_with_Gemini.ipynb](module4/02_Exploring_Modern_LLMs_with_Gemini.ipynb)** - Google Gemini integration
- **[03_RAG_Pipeline.ipynb](module4/03_RAG_Pipeline.ipynb)** - Retrieval-Augmented Generation implementation

### Module 5: Agentic AI and Miscellanea
- **[01-multi-agent_system/](module5/01-multi-agent_system/)** - Production-ready travel assistant with vector search
- **[02_LoRA_Fine_Tuning.ipynb](module5/02_LoRA_Fine_Tuning.ipynb)** - Low-Rank Adaptation fine-tuning techniques
- **[03_Quantization_Comparison.ipynb](module5/03_Quantization_Comparison.ipynb)** - Model quantization and optimization methods

## Key Learning Outcomes

* **Traditional NLP**: Text preprocessing, feature engineering, n-grams, bag-of-words, TF-IDF
* **Modern Embeddings**: Word2Vec, GloVe, sentence transformers, semantic search
* **Deep Learning**: LSTM networks, attention mechanisms, transformer architectures
* **Language Models**: GPT text generation, BERT classification, fine-tuning strategies
* **Agentic AI**: Multi-agent systems, production deployment, retrieval-augmented generation, model optimization

## Technologies Used

* **Core Libraries**: spaCy, NLTK, scikit-learn, transformers, sentence-transformers
* **Deep Learning**: torch, tensorflow, huggingface ecosystem
* **Advanced Tools**: langchain, langgraph, peft (LoRA), datasets
* **Production Systems**: chromadb, vector search, multi-agent deployment
* **Visualization**: matplotlib, seaborn, plotly
* **Data**: pandas, numpy


## Prerequisites

- Python 3.8+
- Basic Python programming knowledge
- Understanding of machine learning concepts
- Familiarity with neural networks (for advanced modules)

## Setup Instructions

1. Clone repository:
```bash
git clone <repository-url>
cd BBS-AIIM
```

2. Install base dependencies:
```bash
pip install torch transformers datasets pandas numpy matplotlib seaborn
```

3. Install specialized packages per module:
```bash
# Module 1-2: Traditional NLP
pip install spacy nltk scikit-learn sentence-transformers

# Module 3-4: Deep Learning
pip install accelerate evaluate

# Module 5: Advanced Systems  
pip install langchain langgraph peft openai chromadb
```

4. Download language models:
```bash
python -m spacy download en_core_web_sm
python -m spacy download it_core_news_sm
```

## Resources

- [Hugging Face Documentation](https://huggingface.co/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [spaCy Documentation](https://spacy.io/)
- [PyTorch Documentation](https://pytorch.org/docs/)

## Contributing

Educational repository for learning purposes. Issues and improvements welcome.

## License

Educational materials for academic and learning purposes.