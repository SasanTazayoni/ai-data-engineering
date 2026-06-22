from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Machine learning is powerful",
    "Artificial intelligence is growing rapidly",
    "Pizza tastes great"
]

embeddings = model.encode(sentences)

# print(embeddings)

similarity_matrix = cosine_similarity(embeddings, embeddings)

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        score = similarity_matrix[i][j]
        print(f"{sentences[i]!r} vs {sentences[j]!r}: {score:.4f}")
