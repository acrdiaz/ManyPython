# pip install google-generativeai chromadb

import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
import os

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key) #Replace with your key
model_name = "gemini-2.0-flash" # 'gemini-pro' or 'gemini-ultra' if you have access.
model = genai.GenerativeModel(model_name)

# 1. Data Preparation
people_data = [
    {"name": "Alice", "birthday": "January 15, 1990"},
    {"name": "Bob", "birthday": "March 22, 1985"},
    {"name": "Charlie", "birthday": "July 4, 2001"},
    {"name": "David", "birthday": "November 10, 1978"},
    {"name": "Eve", "birthday": "May 30, 1995"},
    {"name": "Frank", "birthday": "September 18, 1982"},
    {"name": "Grace", "birthday": "February 28, 2003"},
    {"name": "Henry", "birthday": "December 5, 1998"},
    {"name": "Ivy", "birthday": "April 12, 1975"},
    {"name": "Jack", "birthday": "August 25, 2000"}
]

# 2. Embedding and Vector Database Setup (ChromaDB)
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="people_birthdays")

for person in people_data:
    text = f"{person['name']}'s birthday is {person['birthday']}."
    embedding = genai.embed_content(model='models/embedding-001', content=text)['embedding'] #Corrected line
    collection.add(
        embeddings=[embedding],
        documents=[text],
        ids=[person['name']]
    )

# 3. Retrieval Function
def retrieve_context(query, collection):
    query_embedding = genai.embed_content(model='models/embedding-001', content=query)['embedding'] #Corrected line
    results = collection.query(query_embeddings=[query_embedding], n_results=2)
    return " ".join(results['documents'][0])

# 4. RAG Function
def rag_gemini(query, collection):
    context = retrieve_context(query, collection)
    prompt = f"Answer the question based on the following context: {context}. Question: {query}"
    response = model.generate_content(prompt)
    return response.text

# Example Usage
question = "When was Bob born?"
answer = rag_gemini(question, collection)
print(answer)

question2 = "Tell me about Grace's birthday"
answer2 = rag_gemini(question2, collection)
print(answer2)