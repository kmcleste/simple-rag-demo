from fastapi import FastAPI, UploadFile, HTTPException
from typing import List
import uuid

from src.embeddings import EmbeddingModel
from src.db import VectorStore
from src.llm import LLMBackend

app = FastAPI()
embedding_model = EmbeddingModel()
vector_store = VectorStore()
llm_backend = LLMBackend()


@app.post("/upload")
async def upload_documents(files: List[UploadFile]):
    try:
        for file in files:
            content = await file.read()
            text = content.decode("utf-8")
            doc_id = str(uuid.uuid4())

            vector_store.add_documents(
                texts=[text], metadatas=[{"filename": file.filename}], ids=[doc_id]
            )
        return {"message": f"Successfully uploaded {len(files)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/retrieve")
async def retrieve_documents(query: str, k: int = 3):
    try:
        results = vector_store.query(query, n_results=k)
        return {
            "documents": results["documents"],
            "metadatas": results["metadatas"],
            "distances": results["distances"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


SYSTEM_PROMPT = """You are a helpful AI assistant. Answer questions based on the provided context.
If the answer cannot be found in the context, say so. Do not hallucinate or make up information."""


@app.post("/query")
async def query_with_context(query: str, k: int = 3):
    try:
        # Retrieve relevant documents
        results = vector_store.query(query, n_results=k)

        # Construct prompt with context
        context = "\n".join(results["documents"][0])
        prompt = f"""Context information is below:
---
{context}
---
Given the context above, please answer the following question: {query}"""

        # Generate response using OpenAI
        response = await llm_backend.generate(
            prompt=prompt, system_prompt=SYSTEM_PROMPT
        )

        return {
            "response": response,
            "retrieved_documents": results["documents"],
            "metadatas": results["metadatas"],
            "distances": results["distances"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
