from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from prompts import get_assistant_prompt_tips
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

import os

_ = load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
FILTER_THRESHOLD = 0.35
MAX_RESULTS_SIMILARITY_SEARCH = 10

def search(vectordb, query: str = None):
    results = vectordb.similarity_search_with_score(query, k=MAX_RESULTS_SIMILARITY_SEARCH)
    filtered_results = [r for r in results if r[1] <= FILTER_THRESHOLD]
    docs = list(map(lambda result: result[0], filtered_results))
    
    prompt = get_assistant_prompt_tips()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    chain = load_qa_chain(llm, chain_type="stuff",
                          prompt=prompt, verbose=False)
    answer = chain(
        {"input_documents": docs, "question": query}, return_only_outputs=True)
    return build_response(answer, docs)

def build_response(answer, docs):
    if not "output_text" in answer:
        return {"answer": "No se encontró una respuesta", "sources": "No se encontró una fuente"}
    answer = answer.get("output_text")
    return {"answer": answer, "sources": build_sources(docs)}

def build_sources(docs):
    sources = []
    for doc in docs:
        metadata = doc.metadata
        if metadata is not None:
            link = metadata.get("link")
            source = {
                "name": metadata.get("name"),
                "link": link,
                "text": doc.page_content
            }
            sources.append(source)
    return sources