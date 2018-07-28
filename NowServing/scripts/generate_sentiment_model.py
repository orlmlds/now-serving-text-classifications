from lib.cnn_embedded_vec_classifier import CNNEmbeddedVecClassifier
from flaskr.setup_env import LOCAL_ENV



def main():
    lucas_phone_text_messages = {
        "positive": [
            "i love you",
            "you are great",
            "wonderful"
        ],
        "negative": [
            "hate you",
            "you are mean",
            "awful person"
        ],
        "neutral": [
            "pizza?",
            "what's up"
        ]
    }

    model = CNNEmbeddedVecClassifier()
    model.train(lucas_phone_text_messages)
    model.to_disk(LOCAL_ENV.SENTIMENT_MODEL_FN)

def memory_leak():
    import time
    import psutil
    import os

    process = psutil.Process(os.getpid())

    # Constant for converting bytes to MB (in base 2)
    BYTES_TO_MIB = 9.53674316e-7

    while True:

        time.sleep(0.05)
        main()

        print(process.memory_info().rss * BYTES_TO_MIB)

if __name__ == "__main__":
    main()


