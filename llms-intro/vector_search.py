from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example documents
documents = [
    "Machine learning uses data",
    "Python is a programming language",
    "Football is a popular sport"
]

# Convert documents into embeddings
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)


# Add embeddings into the index
index.add(np.array(embeddings).astype('float32'))

query = model.encode(["What programming languages are there?"]).astype('float32')
distances, indices = index.search(query, k=2)

for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
    print(f"{rank + 1}. {documents[idx]!r} (distance: {dist:.4f})")