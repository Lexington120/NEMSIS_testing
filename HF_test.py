from sentence_transformers import SentenceTransformer, util
import numpy as np
import mysql.connector

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample database of sentence embeddings (you would replace this with your actual database)
database_sentences = [
    "This is a sample sentence for the database.",
    "Another example sentence is included here.",
    "The database contains various sentences."
]
database_embeddings = model.encode(database_sentences, convert_to_tensor=True)

def semantic_similarity_analysis(input_text):
    # Segment input text by sentences
    sentences = input_text.split('. ')  # Simple split by '. ' for demonstration purposes

    # Generate embeddings for each sentence in the input text
    input_embeddings = model.encode(sentences, convert_to_tensor=True)

    # Perform semantic similarity analysis
    similarity_results = []
    for input_embedding in input_embeddings:
        # Compute cosine similarity between the input sentence embedding and the database embeddings
        cosine_scores = util.pytorch_cos_sim(input_embedding, database_embeddings)

        # Find the most similar sentence in the database
        most_similar_idx = np.argmax(cosine_scores.cpu().numpy())
        most_similar_sentence = database_sentences[most_similar_idx]
        similarity_score = cosine_scores[0][most_similar_idx].item()

        # Append the result
        similarity_results.append({
            'input_sentence': sentences[input_embeddings.index(input_embedding)],
            'most_similar_database_sentence': most_similar_sentence,
            'similarity_score': similarity_score
        })

    return similarity_results

# Example usage
input_text = "This is a sample input sentence. It should be compared to the database."
results = semantic_similarity_analysis(input_text)
for result in results:
    print(f"Input Sentence: {result['input_sentence']}")
    print(f"Most Similar Database Sentence: {result['most_similar_database_sentence']}")
    print(f"Similarity Score: {result['similarity_score']}\n")