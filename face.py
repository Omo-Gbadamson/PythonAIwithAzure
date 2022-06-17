from io import BytesIO
import os
from PIL import Image, ImageDraw
import requests

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials


# This key will serve all examples in this document.
KEY = '48f6ea3d5c27430d96ca7c06e4b6c93c'

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = 'https://moshfacecompare.cognitiveservices.azure.com/'

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

face1_url = 'https://happydami.com/wp-content/uploads/2021/05/56272025-1C08-4B79-ABD9-E54522A6FCE0-225x300.jpeg'
face1_name = os.path.basename(face1_url)
face2_url = 'https://happydami.com/wp-content/uploads/2021/01/20201228_132732-300x225.jpg'
face2_name = os.path.basename(face2_url)

# List of url images
url_images = [face1_url, face2_url]

# Attributes you want returned with the API call, a list of FaceAttributeType enum (string format)
face_attributes = ['age', 'gender', 'headPose', 'smile', 'facialHair', 'glasses', 'emotion']

# Detect a face with attributes, returns a list[DetectedFace]
for image in url_images:
    detected_faces = face_client.face.detect_with_url(url=image, return_face_attributes=face_attributes)
    if not detected_faces:
        raise Exception(
        'No face detected from image {}'.format(os.path.basename(image)))

'''
Display the detected face with attributes and bounding box
'''
# Face IDs are used for comparison to faces (their IDs) detected in other images.
for face in detected_faces:
    print()
    print('Detected face ID from', os.path.basename(image), ':')
    # ID of detected face
    print(face.face_id)
    # Show all facial attributes from the results
    print()
    print('Facial attributes detected:')
    print('Age: ', face.face_attributes.age)
    print('Gender: ', face.face_attributes.gender)
    print('Head pose: ', face.face_attributes.head_pose)
    print('Smile: ', face.face_attributes.smile)
    print('Facial hair: ', face.face_attributes.facial_hair)
    print('Glasses: ', face.face_attributes.glasses)
    print('Emotion: ')
    print('\tAnger: ', face.face_attributes.emotion.anger)
    print('\tContempt: ', face.face_attributes.emotion.contempt)
    print('\tDisgust: ', face.face_attributes.emotion.disgust)
    print('\tFear: ', face.face_attributes.emotion.fear)
    print('\tHappiness: ', face.face_attributes.emotion.happiness)
    print('\tNeutral: ', face.face_attributes.emotion.neutral)
    print('\tSadness: ', face.face_attributes.emotion.sadness)
    print('\tSurprise: ', face.face_attributes.emotion.surprise)
    print()

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return ((left, top), (right, bottom))

# Download the image from the url, so can display it in popup/browser
response = requests.get(image)
img = Image.open(BytesIO(response.content))

# For each face returned use the face rectangle and draw a red box.
print('Drawing rectangle around face... see popup for results.')
print()
draw = ImageDraw.Draw(img)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')

# Display the image in the users default image browser.
img.show()