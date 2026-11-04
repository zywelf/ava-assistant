from sentence_transformers import SentenceTransformer, util

# Load the model (the "translator" from text to numbers)
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# The four words we want to compare
texts = ["auto", "macchina", "vettura", "autobiografia"]

# Turn each word into a list of 384 numbers
embeddings = model.encode(texts)

# How many lists, and how many numbers in each?
print(embeddings.shape)

# The first 5 numbers of "auto", just to see what they look like
print(embeddings[0][:5])

# How similar is "auto" to each of the four words?
scores = util.cos_sim(embeddings[0], embeddings)
print(scores)