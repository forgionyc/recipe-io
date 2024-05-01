from typing import List, Tuple
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet import preprocess_input

seq_model = keras.models.load_model("model/mobilenet_model.keras")
seq_model.metrics_names

from typing import List, Tuple

class_labels = [
    "Bean",
    "Bitter_Gourd",
    "Bottle_Gourd",
    "Brinjal",
    "Broccoli",
    "Cabbage",
    "Capsicum",
    "Carrot",
    "Cauliflower",
    "Cucumber",
    "Papaya",
    "Potato",
    "Pumpkin",
    "Radish",
    "Tomato",
]


def translate_pred(prediction: np.array, class_labels: List[str]) -> Tuple[str, float]:
    """Translate model prediction into human-readable format for multi-class classification.

    Args:
        prediction (np.array): Model prediction array.
        class_labels (List[str]): List of class labels.

    Returns:
        Tuple[str, float]: Tuple containing the predicted class and its corresponding confidence score.
    """
    max_prob_index = np.argmax(prediction)
    predicted_class = class_labels[max_prob_index]
    confidence_score = round(prediction[0][max_prob_index] * 100, 2)
    return predicted_class, confidence_score


def model_predict(image_uri: str):

    # Load the image
    img_width, img_height = 224, 224
    my_image = load_img(image_uri, target_size=(img_width, img_height))

    # Convert the image to an array and preprocess it
    img_arr = img_to_array(my_image)
    img_arr = np.expand_dims(img_arr, axis=0)
    preprocessed_img = preprocess_input(img_arr)

    prediction = seq_model.predict(preprocessed_img)
    # Assuming `prediction` is the output prediction array from your model
    predicted_class, confidence_score = translate_pred(prediction, class_labels)

    # Print the prediction
    print(f"It's a {predicted_class} ({confidence_score:.2f}%)")
    return {"predictedClass": predicted_class, "confidenceScore": confidence_score}


def multiple_model_predict(file_paths):
    data = list()
    for fp in file_paths:
        pred = model_predict(fp)
        data.append(pred)

    return data
