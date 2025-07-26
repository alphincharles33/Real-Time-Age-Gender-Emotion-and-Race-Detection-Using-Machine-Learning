# Changed import from 'config' to relative import from '.config'
# and aliased as cfg_emotion to avoid potential clashes.
from . import config as cfg_emotion 
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

class predict_emotions():
    def __init__(self):        
        # Use cfg_emotion for path_model
        self.model = load_model(cfg_emotion.path_model)
    
    def preprocess_img(self,face_image,rgb=True,w=48,h=48):
        face_image = cv2.resize(face_image, (w,h))
        # Use cfg_emotion for rgb, w, h
        if cfg_emotion.rgb == False:
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = face_image.astype("float") / 255.0
        face_image= img_to_array(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        return face_image
    
    def get_emotion(self,img,boxes_face):
        emotions = []
        if len(boxes_face)!=0:
            for box in boxes_face:
                y0,x0,y1,x1 = box
                face_image = img[x0:x1,y0:y1]
                # preprocesar data
                # Use cfg_emotion for rgb, w, h
                face_image = self.preprocess_img(face_image ,cfg_emotion.rgb, cfg_emotion.w, cfg_emotion.h)
                # predecir imagen
                prediction = self.model.predict(face_image)
                # Use cfg_emotion for labels
                emotion = cfg_emotion.labels[prediction.argmax()]
                emotions.append(emotion)
        else:
            emotions = []
            boxes_face = []
        return boxes_face,emotions
