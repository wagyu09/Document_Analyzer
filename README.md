# Document_Analyzer

This project is a pipeline that implements **RAG (Retrieval-Augmented Generation)**, adding PDF document-based response capabilities to a Large Language Model (LLM).
As this is a project for learning purposes, the core pipeline was implemented manually without using high-abstraction libraries like LangChain, which simplify RAG implementation.

The project's goal is to compare the performance of two primary retriever methods, **BM25 (keyword-based)** and **Vector (semantic-based)**, using the `Ragas` library.

---

## 1. Core Philosophy and Architecture

The core pipeline... intentionally avoids LangChain, a high-abstraction framework that simplifies RAG implementation, in order to manually build and understand each component from the ground up.  
LangChain was only used as a helper tool in the evaluation.py script. Its only job was to use the LangchainLLMWrapper to connect Ragas to the evaluation LLM.

---

## 2. Evaluation Results

Based on an evaluation using the `[세토피아][정정]반기보고서(2025.09.09).pdf`[정정]반기보고서(2025.09.09).pdf] and a 30-question QA dataset (`evaluation_data.csv`), the **BM25 retriever showed superior performance** over the Vector retriever for financial reports where specific keywords and figures are critical.
However, it must be noted that this evaluation was conducted using only a single dataset with 30 questions, so it is not a statistically significant validation.

The Generator model used was `gemma2:9b` via `ollama`, and the Evaluation model was `gpt-4o-mini`.

### Performance Summary

| Metric (Evaluation Index) | **BM25 (Keyword)** | **Vector (Semantic)** |
| :--- | :---: | :---: |
| **`context_precision`** | **0.967** | 0.900 |
| **`context_recall`** | 0.783 | 0.783 |
| **`faithfulness`** | 0.706 | **0.724** |
| **`answer_relevancy`** | **0.521** | 0.448 |

### Performance Comparison Chart

<img width="800" alt="RAG Retriever Performance Comparison Chart" src="https://github.com/user-attachments/assets/d457ab82-4292-4dc9-81cf-176e8ae5bec9" />

---

## 3. Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/wagyu09/Document_Analyzer.git](https://github.com/wagyu0923/Document_Analyzer.git)
cd Document_Analyzer
```

### 2. Install Dependencies
```bash
# PyMuPDF, OpenAI, Ragas, ChromaDB, Rank-BM25, etc.
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and enter your OpenAI API key.
```
OPENAI_API_KEY="sk-..."
```

---

## 4. Usage

### 1. Prepare PDF and Evaluation Data
* Place the PDF file to be analyzed in the `pdf_files/` directory. (e.g., `[세토피아][정정]반기보고서(2025.09.09).pdf`[정정]반기보고서(2025.09.09).pdf])
* Prepare the evaluation queries (`user_input`) and ground truth answers (`reference`) in the `evaluation_data.csv` file.

### 2. Run the Evaluation Script
Run the evaluation using the `evaluation.py` script. You can select the retriever to evaluate using the `--retriever` argument.

```bash
# Evaluate only the BM25 retriever
python evaluation.py --retriever bm25

# Evaluate only the Vector retriever
python evaluation.py --retriever vector

# Evaluate both retrievers
python evaluation.py --retriever all
```

### 3. Check Results
After execution is complete, you can find detailed Ragas evaluation scores in `result_bm25.csv` and `result_vector.csv`.

---

## 5. Project Structure

```text
Document_Analyzer/
│
├── .env                  # (Must be created manually) Environment variables (API Key)
├── .gitignore            # Git ignore file
├── main.py               # RAG pipeline setup and indexing execution
├── evaluation.py         # Evaluation script (CLI)
├── config.py             # Configuration management (model names, paths, etc.)
├── prompts.py            # Prompt management for LLM Generator
├── evaluation_data.csv   # QA dataset for evaluation
├── requirements.txt      # List of dependencies
│
├── pipeline/             # Core RAG modules (LangChain independent)
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── bm25_retriever.py
│   ├── vector_retriever.py
│   └── generator.py
│
├── tests/                # ipynb files containing code implementation and tests before modularization
│
├── pdf_files/            # Original PDF documents
│   ├── [세토피아][정정]반기보고서(2025.09.09).pdf[정정]반기보고서(2025.09.09).pdf]
│
├── chroma_db/            # (Generated) ChromaDB vector store
│
├── rag_performance_comparison.png # (Generated) Evaluation score comparison graph
├── result_bm25.csv       # (Generated) BM25 Ragas evaluation results
└── result_vector.csv     # (Generated) Vector Ragas evaluation results
```

## 6. Retrospective

By manually implementing the entire RAG pipeline without a high-abstraction library like LangChain, I was able to gain a solid understanding of RAG's architecture.

The evaluation results helped me realize that for structured, domain-specific documents like business reports, BM25 can show better performance.

In the future, I would like to implement and compare the performance of a hybrid approach that uses both the BM25 and Vector retrievers.
