import pandas as pd
import numpy as np
import os
import ast
import json
import main as rag_pipeline
from dotenv import load_dotenv
from ragas import EvaluationDataset, evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)
from ragas.run_config import RunConfig
from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper
import argparse

def generate_evaluation_set(df, retriever, generator):
    dataset = df.copy()
    for index, query in enumerate(df['user_input']):
        retrieved_data = retriever.retrieve(query, n_results = 5)
        outputs = generator.generate(retrieved_data, query)
        try:
            outputs = json.loads(outputs)
        except json.JSONDecodeError:
            print(f'JSON Decode Error at index {index+1}. Skipping.') 
            print(outputs)
            continue 
        
        if 'answer' not in outputs.keys():
            outputs['answer'] = ''
        dataset.loc[index, 'retrieved_contexts'] = retrieved_data
        dataset.loc[index, 'response'] = outputs['answer']
        print(f'progress : {index+1}/{len(df)}')
    return dataset

def _process_contexts(x):
    if x is None or (isinstance(x, float) and pd.isna(x)) or x == "":
        return []
    if isinstance(x, str):
        x_stripped = x.strip()
        if x_stripped.startswith("[") and x_stripped.endswith("]"):
            try:
                return ast.literal_eval(x_stripped)
            except (ValueError, SyntaxError):
                return [x]
        else:
            return [x]
    if isinstance(x, list):
        return x
    return [x]

def _process_reference(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    if isinstance(x, str):
        return x
    try:
        return "\n\n".join(map(str, x))
    except TypeError:
        return str(x)
    
def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    dataset = df.copy()
    if "retrieved_contexts" in dataset.columns:
        dataset["retrieved_contexts"] = dataset["retrieved_contexts"].apply(_process_contexts)
    if "reference" in dataset.columns:
        dataset["reference"] = dataset["reference"].apply(_process_reference)
    dataset = dataset.fillna('')
    return dataset
def run_ragas_evaluation(dataset, llm):
   
    metrics = [
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ]
    
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=llm,
    )
    return result

def main(retriever_type: str):
    PDFPATH = '/home/wagyu0923/project/Document_Analyzer/pdf_files/[세토피아][정정]반기보고서(2025.09.09).pdf'
    EVALUATIONPATH = '/home/wagyu0923/project/Document_Analyzer/evaluation_data.csv'

    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    df = pd.read_csv(EVALUATIONPATH)
    chunker, embedder, vector_retriever, bm25_retriever, generator = rag_pipeline.setup_pipeline()
    rag_pipeline.run_indexing(PDFPATH, chunker, embedder, vector_retriever, bm25_retriever)

    base_llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    evaluator_llm = LangchainLLMWrapper(base_llm)

    if retriever_type == 'vector' or retriever_type == 'all':
        print("Starting Vector Retriever Evaluation")
        vector_retriever_data = generate_evaluation_set(df, vector_retriever, generator)
        vector_retriever_data = preprocess_dataset(vector_retriever_data)
        vector_evaluation = EvaluationDataset.from_pandas(vector_retriever_data)
        result_vector = run_ragas_evaluation(vector_evaluation, evaluator_llm)
        print(f'score : {result_vector}')
        result_vector.to_pandas().to_csv('result_vector.csv')

    if retriever_type == 'bm25' or retriever_type == 'all':
        print("Starting BM25 Retriever Evaluation")
        bm25_retriever_data = generate_evaluation_set(df, bm25_retriever, generator)
        bm25_retriever_data = preprocess_dataset(bm25_retriever_data)
        bm25_evaluation = EvaluationDataset.from_pandas(bm25_retriever_data)
        result_bm25 = run_ragas_evaluation(bm25_evaluation, evaluator_llm)
        print(f'score : {result_bm25}')
        result_bm25 = result_bm25.to_pandas().to_csv('result_bm25.csv')
        
    if retriever_type not in ['vector', 'bm25', 'all']:
        print(f"Error: Unknown retriever type '{retriever_type}'. Please use 'vector', 'bm25', or 'all'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAG evaluation pipeline.")
    parser.add_argument(
        "--retriever",  
        type=str,
        choices=['vector', 'bm25', 'all'], 
        required=True, 
        help="Type of retriever to evaluate: 'vector', 'bm25', or 'all'."
    )
    args = parser.parse_args()
    main(args.retriever)