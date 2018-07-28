# ensure the right directory is added to the python path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import remaining dependencies
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from flaskr.health_check import HealthCheck
from flaskr.handle_complaint_request import HandleComplaintRequest
from flaskr.handle_sentiment_request import HandleSentimentRequest

from flaskr.setup_env import LOCAL_ENV

# Create the application, and set some Flask defaults
app = Flask(__name__)
api = Api(app)
CORS(app)

# map the resource endpoint url to the recourse class
recourses = {
    "/_health": HealthCheck,
    "/handle_complaint_request": HandleComplaintRequest,
    "/handle_sentiment_request": HandleSentimentRequest
}

for recourse in recourses:
    api.add_resource(recourses[recourse], recourse)

def main():
    """ Application entrypoint

    :return:
    """

    app.run(host="0.0.0.0", port=LOCAL_ENV.APP_PORT)


if __name__ == "__main__":

    # Handle initializations for each endpoint (if necessary)
    for recourse in recourses:
        initializer = getattr(recourses[recourse], "init", None)
        if initializer:
            initializer()

    main()
