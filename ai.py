from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

# Read the dataset from a file
file_path = "context_dictionary_matches_1.txt"
with open(file_path, "r", encoding="utf-8") as file:
    dataset = file.readlines()

# Tokenize the dataset
tokenized_dataset = [word_tokenize(text.lower()) for text in dataset]

# Define the Word2Vec model
model = Word2Vec(sentences=tokenized_dataset, vector_size=100, window=5, min_count=1, workers=4)

model.train(tokenized_dataset, total_examples=len(dataset), epochs=10)

model.save("word2vec_model")


loaded_model = Word2Vec.load("word2vec_model")

seed_word = "comic"

words_to_rank_file = "/home/kali/project/output/layer2_santised.txt"
with open(words_to_rank_file, "r", encoding="utf-8") as file:
    unranked_words = [line.strip() for line in file]


similarity_scores = []

for word in unranked_words:
    if word.lower() in model.wv:
        similarity_scores.append((word, model.wv.similarity(seed_word, word.lower())))

similarity_threshold = 0.0

relevant_words = [(word, similarity) for word, similarity in similarity_scores if similarity >= similarity_threshold]
relevant_words_sorted = sorted(relevant_words, key=lambda x: x[1], reverse=True)

print(f"Words similar to '{seed_word}' above the threshold:")

with open("/home/kali/project/layer2_ai.txt", "w") as file1: 
    for word, similarity in relevant_words_sorted:

        file1.write(f"{word}: {similarity}\n")