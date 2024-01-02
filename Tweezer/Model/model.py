import pickle
from pathlib import Path

import numpy as np
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine


class Model:
    vectors = []
    vectors_path = ""

    def __init__(self, vectors_path="TweezerMDL", vector_size=100):
        self.vectors_path = vectors_path

        if Path(vectors_path).is_file():
            self.vectors = self.read_vector_file(vectors_path)

    def learn(self, dict_to_add_to_dataset):
        dict_with_vector = self.process_code_and_append_vector(dict_to_add_to_dataset)
        self.vectors.append(dict_with_vector)
        self.save_vector_file(self.vectors, self.vectors_path)

    def save_vector_file(self, vectors, vectors_path):
        with open(vectors_path, 'wb') as file:
            pickle.dump(vectors, file)

    def read_vector_file(self, vector_path):
        with open(vector_path, 'rb') as file:
            return pickle.load(file)

    def process_code_and_append_vector(self, data):
        """
        Process the given code data using Word2Vec to generate a fixed-size vector and append it to the data dict.

        :param data: A dictionary in the format {"name": <string>, "code": <list of strings>}
        :return: The original dictionary with an added key "vector" containing the Word2Vec vector of the code.
        """
        # Constants
        VECTOR_SIZE = 500

        # Extract code lines from the data
        code_lines = data["code"]

        # Tokenize the code lines
        tokens = [line.split() for line in code_lines]

        # Train a Word2Vec model
        model = Word2Vec(tokens, vector_size=VECTOR_SIZE, window=5, min_count=1, workers=4)

        # Generate vectors for each token and aggregate them
        vectors = np.zeros((VECTOR_SIZE,))
        for token_line in tokens:
            for token in token_line:
                if token in model.wv:
                    vectors += model.wv[token]

        # Average the vectors
        if len(tokens) > 0:
            vectors /= len(tokens)

        # Pad or truncate the vector to ensure it's of size VECTOR_SIZE
        if len(vectors) > VECTOR_SIZE:
            vectors = vectors[:VECTOR_SIZE]
        elif len(vectors) < VECTOR_SIZE:
            vectors = np.pad(vectors, (0, VECTOR_SIZE - len(vectors)), 'constant')

        # Append the vector to the data dictionary
        data["vector"] = vectors

        return data

    def find_closest_code(self, dataset, target):
        """
        Find the code in the dataset closest to the target based on their vectors and add a 'distance' field to each.

        :param dataset: A list of dictionaries, each with a 'vector' key among others.
        :param target: A dictionary with a 'vector' key.
        :return: The dataset with an added 'distance' field in each dictionary indicating closeness to the target.
        """
        target_vector = target.get('vector')

        for data in dataset:
            data_vector = data.get('vector')
            # Calculate cosine distance between vectors, lower means closer
            data['distance'] = cosine(data_vector, target_vector)

        return dataset


if __name__ == '__main__':
    raise Exception("This is not an entrypoint!")
