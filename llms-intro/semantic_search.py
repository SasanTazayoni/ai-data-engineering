from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Python is a popular programming language used in data science",
    "Machine learning is a subset of artificial intelligence",
    "FAISS is a library for efficient similarity search",
    "Neural networks are inspired by the human brain",
    "Football is played by two teams of eleven players",
    "Paris is the capital city of France",
    "The Eiffel Tower is one of the most visited monuments in the world",
    "Deep learning models require large amounts of training data",
    "SQL is used to query relational databases",
    "The Amazon rainforest produces 20% of the world's oxygen",
    "React is a JavaScript library for building user interfaces",
    "The human heart beats approximately 100,000 times per day",
    "Docker is a tool for running applications in containers",
    "The Great Wall of China stretches over 13,000 miles",
    "Quantum computing uses qubits instead of classical bits",
    "Shakespeare wrote 37 plays and 154 sonnets",
    "The speed of light is approximately 300,000 kilometres per second",
    "Git is a version control system used by software developers"
]

embeddings = model.encode(documents).astype('float32')

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

query = input("Search: ")

query_embedding = model.encode([query]).astype('float32')
distances, indices = index.search(query_embedding, k=3)

for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
    print(f"{rank + 1}. {documents[idx]!r} (distance: {dist:.4f})")
