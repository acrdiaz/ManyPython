import google.generativeai as genai
import chromadb
#import os

api_key = os.getenv("GEMINI_API_KEY")
model_name = "gemini-2.0-flash" # 'gemini-pro' or 'gemini-ultra' if you have access.
n_results = 2

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

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
    {"name": "Jack", "birthday": "August 25, 2000"},
    {"name": "Alicia", "birthday": "September 15, 1990"},
    {"name": "Jackeline", "birthday": "February 25, 2000"},
    {"name": "Bobby", "birthday": "September 22, 1985"},
]

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="people_birthdays")

for person in people_data:
    text = f"{person['name']}'s birthday is {person['birthday']}."
    embedding = genai.embed_content(model='models/embedding-001', content=text)['embedding']
    collection.add(embeddings=[embedding], documents=[text], ids=[person['name']])

def retrieve_context(query, collection):
    query_embedding = genai.embed_content(model='models/embedding-001', content=query)['embedding']
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results

def rag_gemini(query, collection):
    # context = retrieve_context(query, collection)
    # prompt = f"Answer the question based on the following context: {context}. Question: {query}"
    # response = model.generate_content(prompt)
    # return response.text

    results = retrieve_context(query, collection)
    context = " ".join(results['documents'][0])
    similarity_score = results['distances'][0][0] #get the first distance.

    # you will need to test what distance means out of context.
    # if similarity_score > 0.5:
    #    prompt = f"Answer the question based on the following context: {context}. Question: {query}"
    #    response = model.generate_content(prompt)
    #    return response.text
    # else:
    #     response = model.generate_content(query)
    #     return f"This question is outside the scope of my current knowledge base :). Here is a general answer: {response.text}"
    return similarity_score

question = "When was Bob born?"
print(question)
answer = rag_gemini(question, collection)
print(answer)

question = "Who were born on September?"
print(question)
answer = rag_gemini(question, collection)
print(answer)

question = "List of the female names?"
print(question)
answer = rag_gemini(question, collection)
print(answer)

question = "What countries start with the letter 'A'?"
print(question)
answer = rag_gemini(question, collection)
print(answer)