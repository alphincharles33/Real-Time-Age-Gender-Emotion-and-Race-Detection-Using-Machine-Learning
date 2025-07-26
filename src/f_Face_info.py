import cv2
import numpy as np
from deepface import DeepFace
import os  # Import os for path manipulation

# Face Recognition Libraries
import face_recognition
# FIX: Change import to match the actual class name 'rec' in face_recognition_main.py
from .face_recognition_main import rec as FaceRecognition

# Initialize FaceRecognition for known faces
# It will attempt to load faces from data/known_faces/
# This needs to be relative to the project root, assuming f_Face_info.py is in src/
known_faces_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'known_faces'))
face_recognizer = FaceRecognition(known_faces_path)


def bounding_box(out, img):
    """
    Draws bounding boxes and labels on the image based on face analysis output.
    """
    if out is None or not out:  # Handle case where no faces are detected or out is empty
        return img

    for info in out:
        if 'bbx_frontal_face' in info and len(info['bbx_frontal_face']) == 4:
            x, y, w, h = info['bbx_frontal_face']
            x1, y1, x2, y2 = x, y, x + w, y + h

            # Ensure coordinates are within image bounds
            x1, y1, x2, y2 = max(0, x1), max(0, y1), min(img.shape[1], x2), min(img.shape[0], y2)

            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Prepare text for labels
            name_text = f"Name: {info.get('name', 'Unknown')}"
            age_text = f"Age: {info.get('age', 'N/A')}"
            gender_text = f"Gender: {info.get('gender', 'N/A')}"
            race_text = f"Race: {info.get('race', 'N/A')}"
            emotion_text = f"Emotion: {info.get('emotion', 'N/A')}"

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_thickness = 1
            text_color = (255, 255, 255)
            bg_color = (0, 0, 0)

            # Name
            (text_width, text_height), _ = cv2.getTextSize(name_text, font, font_scale, font_thickness)
            cv2.rectangle(img, (x1, y1 - text_height - 10), (x1 + text_width + 10, y1), bg_color, -1)
            cv2.putText(img, name_text, (x1 + 5, y1 - 5), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # Age
            (text_width, text_height), _ = cv2.getTextSize(age_text, font, font_scale, font_thickness)
            cv2.rectangle(img, (x1, y1 - (text_height * 2) - 15), (x1 + text_width + 10, y1 - text_height - 10), bg_color, -1)
            cv2.putText(img, age_text, (x1 + 5, y1 - text_height - 10), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # Gender
            (text_width, text_height), _ = cv2.getTextSize(gender_text, font, font_scale, font_thickness)
            cv2.rectangle(img, (x1, y1 - (text_height * 3) - 20), (x1 + text_width + 10, y1 - (text_height * 2) - 15), bg_color, -1)
            cv2.putText(img, gender_text, (x1 + 5, y1 - (text_height * 2) - 15), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # Race
            (text_width, text_height), _ = cv2.getTextSize(race_text, font, font_scale, font_thickness)
            cv2.rectangle(img, (x1, y1 - (text_height * 4) - 25), (x1 + text_width + 10, y1 - (text_height * 3) - 20), bg_color, -1)
            cv2.putText(img, race_text, (x1 + 5, y1 - (text_height * 3) - 20), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # Emotion
            (text_width, text_height), _ = cv2.getTextSize(emotion_text, font, font_scale, font_thickness)
            cv2.rectangle(img, (x1, y1 - (text_height * 5) - 30), (x1 + text_width + 10, y1 - (text_height * 4) - 25), bg_color, -1)
            cv2.putText(img, emotion_text, (x1 + 5, y1 - (text_height * 4) - 25), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    return img


def get_face_info(img, filename=None):
    """
    Detects faces, analyzes them using DeepFace, and recognizes known faces.
    """
    try:
        obj_list = DeepFace.analyze(
            img,
            actions=['age', 'gender', 'race', 'emotion'],
            enforce_detection=False
        )

        results = []
        if obj_list:
            for obj in obj_list:
                face_info = {}

                if 'region' in obj and obj['region']:
                    x = obj['region']['x']
                    y = obj['region']['y']
                    w = obj['region']['w']
                    h = obj['region']['h']
                    face_info['bbx_frontal_face'] = [x, y, w, h]

                    face_pixels = img[y: y + h, x: x + w]
                    if face_pixels.size > 0:
                        recognized_names_list = face_recognizer.recognize_face2(face_pixels, [[x, y, w, h]])
                        recognized_name = recognized_names_list[0] if recognized_names_list else (filename if filename else "Unknown")
                        face_info['name'] = recognized_name
                    else:
                        face_info['name'] = filename if filename else "Unknown"
                else:
                    face_info['bbx_frontal_face'] = []
                    face_info['name'] = filename if filename else "Unknown"

                face_info['age'] = obj.get('age', 'N/A')

                if 'gender' in obj and isinstance(obj['gender'], dict):
                    gender_prediction = obj['gender']
                    if 'Man' in gender_prediction and 'Woman' in gender_prediction:
                        face_info['gender'] = 'Man' if gender_prediction['Man'] > gender_prediction['Woman'] else 'Woman'
                    else:
                        dominant_gender = max(gender_prediction, key=gender_prediction.get)
                        face_info['gender'] = dominant_gender.capitalize()
                else:
                    face_info['gender'] = 'N/A'

                if 'race' in obj and isinstance(obj['race'], dict):
                    dominant_race = max(obj['race'], key=obj['race'].get)
                    face_info['race'] = dominant_race.capitalize()
                else:
                    face_info['race'] = 'N/A'

                if 'emotion' in obj and isinstance(obj['emotion'], dict):
                    dominant_emotion = max(obj['emotion'], key=obj['emotion'].get)
                    face_info['emotion'] = dominant_emotion.capitalize()
                else:
                    face_info['emotion'] = 'N/A'

                results.append(face_info)
        return results

    except Exception as e:
        print(f"Error during face analysis: {e}")
        return None  # Return None or empty list on error
