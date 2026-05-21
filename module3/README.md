# Module 12: BERT - Encoder Models

**Duration**: 2 hours
**Focus**: Fine-tuning BERT for classification and question answering

---

## Overview

This module covers advanced applications with BERT (Bidirectional Encoder Representations from Transformers). Students learn to fine-tune BERT for downstream tasks and evaluate performance with comprehensive metrics.

---

## Notebooks

### NLP12_1_Classification_with_Transformers.ipynb (1.5 hours)

Fine-tuning BERT for sentiment analysis and text classification.

**Topics Covered:**
- Loading pre-trained BERT models
- Tokenization with BERT tokenizer
- Fine-tuning with Hugging Face Trainer API
- Hyperparameter tuning
- Model evaluation

**Metrics Covered:**
- Accuracy: Overall correctness
- Precision: Positive predictive value
- Recall: Sensitivity
- F1 Score: Harmonic mean (macro, micro, weighted)
- Confusion Matrix: Error pattern analysis
- ROC Curves: Threshold analysis
- Per-class Performance: Class-specific metrics

**Learning Outcomes:**
1. Fine-tune BERT for classification tasks
2. Use Hugging Face Trainer API effectively
3. Calculate and interpret classification metrics
4. Visualize model performance
5. Compare different model configurations

---

### NLP12_2_Q&A_with_finetuned_BERT.ipynb (0.5 hours)

Extractive question answering with fine-tuned BERT.

**Topics Covered:**
- Loading fine-tuned BERT for Q&A
- SQuAD dataset and format
- Span prediction (start/end tokens)
- Answer extraction
- Confidence scoring

**Metrics Covered:**
- Exact Match (EM): Binary correctness
- F1 Score: Token-level overlap
- Confidence Scores: Model certainty
- Per-question analysis

**Learning Outcomes:**
1. Understand extractive Q&A task
2. Use BERT for span prediction
3. Calculate EM and F1 metrics
4. Analyze prediction confidence
5. Identify failure cases

---

## Key Concepts

### BERT Architecture
- **Type**: Encoder-only transformer
- **Pre-training**: Masked Language Modeling (MLM) + Next Sentence Prediction (NSP)
- **Bidirectional**: Can see context from both directions
- **Best for**: Understanding tasks (classification, NER, extractive Q&A)
- **Cannot do**: Generate fluent new text

### Fine-tuning vs Feature Extraction
- **Feature Extraction**: Freeze BERT, train only classification head
- **Fine-tuning**: Update all BERT weights end-to-end
- **Fine-tuning typically better** but requires more compute

---

## Learning Outcomes

By completing this module, students will be able to:

1. Fine-tune BERT for classification tasks
2. Implement extractive question answering
3. Calculate comprehensive evaluation metrics
4. Interpret confusion matrices and error patterns
5. Compare model performance quantitatively
6. Understand when to use encoder models

---

## Prerequisites

- Module 11: Transformers architecture
- Module 09: Transfer learning concepts
- Understanding of attention mechanisms
- Basic PyTorch/Transformers library knowledge

---

## Required Packages

```python
pip install transformers datasets torch numpy pandas matplotlib seaborn scikit-learn
```

---

## Connection to Other Modules

**From Module 11 (Transformers):**
- Apply transformer architecture knowledge
- Use Hugging Face library

**From Module 09 (Transfer Learning):**
- Apply transfer learning concepts
- Compare fine-tuning approaches

**To Module 13 (GPT):**
- Contrast encoder-only vs decoder-only
- Compare BERT (understanding) vs GPT (generation)

**To Module 14 (RAG):**
- BERT embeddings for retrieval
- Compare extractive Q&A vs RAG

---

## Instructor Notes

### NLP12_1_Classification

**Preparation:**
- Test notebook in Colab with GPU
- Review metric calculations
- Prepare example datasets
- Check Hugging Face model hub access

**Teaching Tips:**
- Show before/after fine-tuning comparison
- Emphasize metric interpretation
- Discuss real-world applications
- Compare to classical ML (Module 02)

**Common Student Questions:**
- "Why BERT over classical ML?" → Better performance, transfer learning
- "How much data do I need?" → Discuss few-hundred vs thousands
- "Can I use my own data?" → Yes, show tokenization process

### NLP12_2_Question Answering

**Preparation:**
- Test Q&A model loading
- Prepare diverse question examples
- Review EM/F1 calculation
- Have failure cases ready to discuss

**Teaching Tips:**
- Start with simple examples
- Show span prediction visualization
- Discuss when extractive Q&A works/fails
- Bridge to generative approaches (Module 14)

**Common Student Questions:**
- "Can BERT generate answers?" → No, only extract existing spans
- "What if answer isn't in text?" → Discuss unanswerable questions, SQuAD 2.0
- "How is this different from RAG?" → RAG combines retrieval + generation

---

## Comparison: BERT vs Classical ML

| Aspect | Classical ML | BERT |
|--------|--------------|------|
| **Training Data** | ~1000s examples | Can work with hundreds |
| **Features** | Manual feature engineering | Automatic |
| **Accuracy** | Good baseline | State-of-the-art |
| **Speed** | Very fast (<10ms) | Slower (~50-100ms) |
| **Interpretability** | High | Lower |
| **When to Use** | Simple tasks, limited compute | Complex tasks, GPU available |

---

## Real-World Applications

Students will see BERT used in:
- Sentiment analysis (reviews, social media)
- Text classification (spam detection, categorization)
- Named Entity Recognition (NER)
- Question answering systems
- Semantic search
- Document similarity

---

## Additional Resources

### Papers
- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) (Devlin et al., 2018)
- [SQuAD: 100,000+ Questions for Machine Comprehension](https://arxiv.org/abs/1606.05250)

### Documentation
- [Hugging Face BERT Documentation](https://huggingface.co/docs/transformers/model_doc/bert)
- [BERT Fine-tuning Tutorial](https://huggingface.co/docs/transformers/training)
- [Metrics Guide](https://scikit-learn.org/stable/modules/model_evaluation.html)

### Models
- [bert-base-uncased](https://huggingface.co/bert-base-uncased) - 110M parameters
- [bert-large-uncased](https://huggingface.co/bert-large-uncased) - 340M parameters
- [bert-base-multilingual](https://huggingface.co/bert-base-multilingual-uncased) - For multiple languages

---

## Assessment Ideas

**For Classification:**
- Fine-tune BERT on custom dataset
- Compare to classical ML baseline
- Calculate all metrics
- Analyze error cases

**For Q&A:**
- Evaluate on SQuAD subset
- Calculate EM and F1
- Identify question types that fail
- Compare to human performance

---

**Module 12** | Data Visualization and Text Mining
Università Cattolica del Sacro Cuore | Academic Year 2025-2026
