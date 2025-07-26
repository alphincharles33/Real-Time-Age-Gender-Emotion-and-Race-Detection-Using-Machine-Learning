# Corrected imports for modules now directly in src/
# We import specific functions instead of aliasing whole modules
from .face_recognition_core import detect_face, get_features, compare_faces
from .face_recognition_storage import load_images_to_database, insert_new_user

import traceback
import numpy as np
import cv2
import time  # Assuming time is needed, based on typical usage


class rec():
    def __init__(self, known_faces_dir):  # FIX: Add known_faces_dir parameter
        '''
        - known_faces_dir: Path to the directory containing known faces.
        - db_names: [name1,name2,...,namen] lista de strings
        - db_features: array(array,array,...,array) cada array representa las caracteriticas de un usuario
        '''
        # Use the directly imported function load_images_to_database
        # FIX: Pass the known_faces_dir to load_images_to_database
        self.db_names, self.db_features = load_images_to_database(known_faces_dir)

    def recognize_face(self, im):
        '''
        Input:
            -im: image (cv2 format)
        Output:
            res:{'status': si todo sale bien es 'ok' en otro caso devuelve el erroe encontrado
                 'faces': [(y0,x1,y1,x0),(y0,x1,y1,x0),...,(y0,x1,y1,x0)] ,cada tupla representa un rostro detectado
                 'names': ['name', 'unknow'] lista con los nombres que hizo match}
        '''
        try:
            # detectar rostro
            box_faces = detect_face(im)  # Use direct function call
            # condiconal para el caso de que no se detecte rostro
            if not box_faces:
                res = {
                    'status': 'ok',
                    'faces': [],
                    'names': []
                }
                return res
            else:
                if not self.db_names:
                    res = {
                        'status': 'ok',
                        'faces': box_faces,
                        'names': ['unknow'] * len(box_faces)
                    }
                    return res
                else:
                    # (continua) extraer features
                    actual_features = get_features(im, box_faces)  # Use direct function call
                    # comparar actual_features con las que estan almacenadas en la base de datos
                    match_names = compare_faces(actual_features, self.db_features, self.db_names)  # Use direct function call
                    # guardar
                    res = {
                        'status': 'ok',
                        'faces': box_faces,
                        'names': match_names
                    }
                    return res
        except Exception as ex:
            error = ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
            res = {
                'status': 'error: ' + str(error),
                'faces': [],
                'names': []
            }
            return res

    def recognize_face2(self, im, box_faces):  # This is the method called by f_Face_info
        try:
            if not self.db_names:
                res = ['unknow']  # Ensure this returns a list to match expected output in f_Face_info
                return res
            else:
                # (continua) extraer features
                actual_features = get_features(im, box_faces)  # Use direct function call
                # comparar actual_features con las que estan almacenadas en la base de datos
                match_names = compare_faces(actual_features, self.db_features, self.db_names)  # Use direct function call
                # guardar
                res = match_names
                return res
        except Exception:  # Catch broader exception to print more info if needed
            res = ['error_in_recognition']  # Provide a default for error cases
            traceback.print_exc()  # Print the full traceback for debugging
            return res


# This bounding_box function should ideally be in f_Face_info.py or a utility file.
# Keeping it here for now if it's called by main_detector or other parts.
def bounding_box(img, box, match_name=[]):
    for i in np.arange(len(box)):
        x0, y0, x1, y1 = box[i]
        img = cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 3)
        if not match_name:
            continue
        else:
            cv2.putText(img, match_name[i], (x0, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return img


if __name__ == "__main__":
    # This __main__ block is for standalone testing of face_recognition_main.py, not the main app.
    # It will use relative paths from src/.
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument("-im", "--path_im", help="path image")
    parse = parse.parse_args()
    path_im = parse.path_im

    if path_im:
        im = cv2.imread(path_im)
        if im is None:
            print(f"Error: Could not load image from {path_im}")
        else:
            # instancio detector
            # NOTE: When running this __main__ block, it assumes 'data/known_faces' is in the current working directory.
            # For robust standalone testing, a path should be passed or hardcoded relative to this script.
            # For simplicity for this __main__ block, we'll initialize with a default for direct execution.
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            default_known_faces_path = os.path.abspath(os.path.join(current_script_dir, '..', 'data', 'known_faces'))
            recognizer = rec(default_known_faces_path)  # Pass the path here for standalone testing
            res = recognizer.recognize_face(im)
            im = bounding_box(im, res["faces"], res["names"])
            cv2.imshow("face recognition", im)
            cv2.waitKey(0)
            print(res)
    else:
        print("Please provide an image path using --path_im argument.")
