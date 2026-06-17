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

similarity = cosine_similarity(
    [embeddings[0]],
    embeddings
)

print(similarity)
