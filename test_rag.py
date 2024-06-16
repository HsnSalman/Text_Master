from embeddings import generate_embeddings_open_ai, generate_text
from SimplerVectors import VectorDatabase


db = VectorDatabase('data')

db.load_from_disk("rag.db")

# Example query
query = "how to define the functions for agent?"

# Embed the query using the same method as the documents
query_embedding = generate_embeddings_open_ai(query)
query_embedding = db.normalize_vector(query_embedding)  # Normalizing the query vector

# Retrieving the top similar document
results = db.top_cosine_similarity(query_embedding, top_n=1)

results_text= []
for doc, score in results:
     results_text.append(doc['vector'])


prompt = f"Answer the following question: {query} \n Based on this context only: \n" + results_text[0]

answer = generate_text(prompt)

print(answer)

