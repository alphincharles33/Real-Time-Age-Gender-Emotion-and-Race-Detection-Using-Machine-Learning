import face_recognition 
import numpy as np
def detect_face(image):  
    Output = face_recognition.face_locations(image)
    return Output
def get_features(img,box): 
    features = face_recognition.face_encodings(img,box)
    return features
def compare_faces(face_encodings,db_features,db_names):
    match_name = []
    names_temp = db_names
    Feats_temp = db_features           
    for face_encoding in face_encodings:
        try:
            dist = face_recognition.face_distance(Feats_temp,face_encoding)
        except:
            dist = face_recognition.face_distance([Feats_temp],face_encoding)
        index = np.argmin(dist)
        if dist[index] <= 0.6:
            match_name = match_name + [names_temp[index]]
        else:
            match_name = match_name + ["unknow"]
    return match_name
