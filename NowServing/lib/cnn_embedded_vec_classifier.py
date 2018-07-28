from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from keras.models import Sequential
from sklearn.externals import joblib
from nltk import word_tokenize
import numpy as np
import embeddings


class CNNEmbeddedVecClassifier:

    def __init__(self,
                 n_gram=1,
                 embedding_vector_length=300,
                 num_filters=100,
                 max_allowable_length=15):
        self.n_gram = n_gram
        self.embedding_vector_length = embedding_vector_length
        self.num_filters = num_filters
        self.max_allowable_length = max_allowable_length
        self.trained = False

        self.model = None

    word_embeddings = embeddings.glove.GloveEmbedding("common_crawl_840", d_emb=300)

    def train(self,
              training_data=None):

        if training_data:
            self.training_data = training_data

        if not self.training_data:
            return

        # convert training_data to training input vectors
        self.labels, training_data_embedded, indices = self.prep_training_data(self.training_data)

        # build the model
        model = self.build_model()

        # train the model
        model.fit(training_data_embedded, indices, epochs=5)

        self.model = model
        self.trained = True

    def predict(self, text):
        if not self.trained:
            pass

        # prep text
        matrix = np.array([self.words_to_matrix(text)])

        # make predictions
        predictions = self.model.predict(matrix)

        # format score
        predictions_and_scores = {}
        for idx, label in zip(range(len(self.labels)), self.labels):
            predictions_and_scores[label] = predictions[0][idx]

        return predictions_and_scores

    def prep_training_data(self, training_data):
        labels = training_data.keys()
        label_idx = dict(zip(labels, range(len(labels))))

        # tokenize the words and encode the labels
        training_examples = []
        indices = []
        for label in labels:
            for example in training_data[label]:
                label_encoding = [0] * len(labels)
                label_encoding[label_idx[label]] = 1
                indices.append(label_encoding)
                training_examples.append(word_tokenize(example))
        indices = np.array(indices, dtype=np.int)

        # create embedded vectors
        training_data_embedded = np.zeros(shape=(len(training_examples), self.max_allowable_length, self.embedding_vector_length))
        for i in range(len(training_examples)):
            for j in range(min(self.max_allowable_length, len(training_examples[i]))):
                training_data_embedded[i, j] = self.word_to_embedding(training_examples[i][j])

        return labels, training_data_embedded, indices

    def build_model(self):
        # build model
        model = Sequential()
        model.add(Conv1D(filters=self.num_filters,
                                kernel_size=self.n_gram,
                                padding='valid',
                                activation='relu',
                                input_shape=(self.max_allowable_length, self.embedding_vector_length)))
        model.add(MaxPooling1D(pool_size=self.max_allowable_length - self.n_gram + 1))
        model.add(Flatten())
        model.add(Dense(len(self.labels), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])

        return model

    def word_to_embedding(self, word):
        return CNNEmbeddedVecClassifier.word_embeddings.emb(word) if word in CNNEmbeddedVecClassifier.word_embeddings else np.zeros(self.embedding_vector_length)

    def words_to_matrix(self, text):
        tokens = word_tokenize(text)
        matrix = np.zeros((self.max_allowable_length, self.embedding_vector_length))
        for i in range(min(self.max_allowable_length, len(tokens))):
            matrix[i] = self.word_to_embedding(tokens[i])

        return matrix

    def to_disk(self,
                fn):

        config = {
            "weights": self.model.get_weights(),
            "labels": list(self.labels)
        }

        joblib.dump(config, fn)

    def from_disk(self,
                  fn):

        config = joblib.load(fn)

        self.labels = config["labels"]

        self.model = self.build_model()
        self.model.set_weights(config["weights"])