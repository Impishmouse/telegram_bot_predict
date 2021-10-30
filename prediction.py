import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np


def model_init():
    classes = ['Christmas Sweeper 3', 'Crystal Crunch', 'Other game']
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # Load the model
    model = tensorflow.keras.models.load_model('./data/keras_model.h5', compile=False)
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    return classes, data, model


classes, data, model = model_init()


def predict_game(image_path):
    # Replace this with the path to your image
    image = Image.open(image_path)
    converted_image = image.convert("RGB")
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(converted_image, size, Image.ANTIALIAS)
    # turn the image into a numpy array
    image_array = np.asarray(image)
    # display the resized image
    image.show()
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    # run the inference
    prediction = model.predict(data)
    print(prediction[0])
    prediction = np.argmax(prediction)
    print(f'Class number:{prediction}')
    text_prediction = f'Game name: {classes[prediction]}'
    return text_prediction


if __name__ == "__main__":
    model_init()