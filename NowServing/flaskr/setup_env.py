import os
import dotenv


dot_env_path = dotenv.find_dotenv()
dotenv.load_dotenv(dot_env_path)

class LOCAL_ENV:
    """
        Stores environment variables and system level configurations
    """

    # The port to run the application on
    APP_PORT = int(os.environ.get("APP_PORT", 3001))
    # The current language of the application
    APP_LANG = os.environ.get("APP_LANG", "english")


    # Complaints Endpoint Configurations

    # Where the model is stored
    COMPLAINTS_MODEL_FN = "models/complaints_model.pkl"
    # Where the vocab is stored
    COMPLAINTS_MODEL_VOCAB_FN = "models/complaints_model_vocab.pkl"


    # Sentiment Endpoint Configurations

    # Where the model is stored
    SENTIMENT_MODEL_FN = "models/sentiment_model.pkl"
