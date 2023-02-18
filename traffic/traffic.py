import cv2
print("please")
import numpy as np
import os
import sys
import tensorflow as tf
print("test")
from sklearn.model_selection import train_test_split
from time import sleep

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    print("in the main")
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    """print("label:")
    print(labels)
    print("images")
    print(images)"""
    #labels = [1,1,1,1,1,1,1,1,1,1,1]
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    directories = os.listdir(data_dir)
    for directory in directories:
        #print(directory)
        innerdirectory = os.path.join(data_dir, directory)
        #
        try:
            dir_image = os.listdir(innerdirectory)
            #print(dir_image)
            
            for image in dir_image:
                
                final_dir = os.path.join(data_dir, directory, image)
                img = cv2.imread(final_dir, cv2.IMREAD_ANYCOLOR)
                #print(img)
                #resized_image = np.resize(img,(IMG_WIDTH,IMG_HEIGHT))
                resized_image = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                if np.shape(resized_image) != (30,30,3):
                    print(np.shape(resized_image))
                    sleep(2)
                #print('appending')
                images.append(resized_image)
                labels.append(directory)
        except NotADirectoryError:
                pass #is it just exiting loop when this happens? how exactly does try work?
    """print(images)
    print(labels)"""
    return (images, labels)
  


    images = []
    labels = []
    for label in data_dir:
        for image in label:
            resized_image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            images.append(image.converttoarray)
            labels.append(label)
    return (images, labels)
    raise NotImplementedError


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    
    model =  tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
        32,(3,3), activation= 'relu', input_shape= (IMG_WIDTH, IMG_HEIGHT, 3)
        ), 

        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        tf.keras.layers.Conv2D(
        32,(3,3), activation= 'relu', input_shape= (14, 14, 32)
        ), 

        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(200, activation = 'relu'),

        tf.keras.layers.Dropout(0.1),

        tf.keras.layers.Dense(NUM_CATEGORIES, activation= 'softmax')
    ])
    model.summary()
    
    model.compile(
        optimizer= 'adam',
        loss= 'categorical_crossentropy',
        metrics= ['accuracy']
    )
    return model
    raise NotImplementedError


if __name__ == "__main__":
    main()
