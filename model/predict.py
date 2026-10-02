import pickle
import pandas as pd

#import the ML model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# generallly MLflow fetches the version by model registry and it tracks which version you have
MODEL_VERSION = '2.1.14'

#get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    df = pd.DataFrame([user_input])

    #predict the class
    predicted_class = model.predict(df)[0]

    # get the probabilities for all classses
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    # creat mapping: {'class_name': probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": confidence,
        'class_probabilities': class_probs
    }

    