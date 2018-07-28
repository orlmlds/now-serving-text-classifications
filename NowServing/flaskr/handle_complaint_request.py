from flask import jsonify
from flask_restful import Resource, reqparse

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer

from flaskr.setup_env import LOCAL_ENV

class HandleComplaintRequest(Resource):

    # The model used to make predictions
    bow_model = None

    # Used to generate the count vectorizer
    count_vectorizer = None

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument("narrative", required=True, type=str)

    def post(self):

        args = self.reqparse.parse_args()
        narrative = args["narrative"]

        if not HandleComplaintRequest.bow_model and not HandleComplaintRequest.count_vectorizer:
            raise AssertionError("No models are loaded!")

        # Prep the data!
        vectorized_narrative = HandleComplaintRequest.count_vectorizer.transform([narrative])

        # Create a prediction !
        prediction = HandleComplaintRequest.bow_model.predict(vectorized_narrative)[0]


        # Return a result in json!
        return jsonify({"prediction": prediction})

    @staticmethod
    def init():

        # Load in the model from the pkl file
        HandleComplaintRequest.bow_model = joblib.load(LOCAL_ENV.COMPLAINTS_MODEL_FN)

        # Load in Count Vectorizers vocabulary
        HandleComplaintRequest.count_vectorizer = CountVectorizer(stop_words=LOCAL_ENV.APP_LANG,
                                                                  max_features=500)

        HandleComplaintRequest.count_vectorizer.vocabulary = joblib.load(LOCAL_ENV.COMPLAINTS_MODEL_VOCAB_FN)
