from flask import jsonify
from flask_restful import Resource, reqparse

from lib.cnn_embedded_vec_classifier import CNNEmbeddedVecClassifier
from flaskr.setup_env import LOCAL_ENV

class HandleSentimentRequest(Resource):

    # The model used to make predictions
    cnn_model = None

    # Used to generate the count vectorizer
    count_vectorizer = None

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument("txt", required=True, type=str)

    def post(self):

        args = self.reqparse.parse_args()
        text_message = args["txt"]

        if not HandleSentimentRequest.cnn_model:
            raise AssertionError("No models are loaded!")

        # Create a prediction !
        prediction = HandleSentimentRequest.cnn_model.predict(text_message)

        # format results
        for dp in prediction:
            prediction[dp] = float(prediction[dp])

        # Return a result in json!
        return jsonify({"prediction": prediction})

    @staticmethod
    def init():

        # Load in the model from the pkl file
        HandleSentimentRequest.cnn_model = CNNEmbeddedVecClassifier(n_gram=1)
        HandleSentimentRequest.cnn_model.from_disk(LOCAL_ENV.SENTIMENT_MODEL_FN)
