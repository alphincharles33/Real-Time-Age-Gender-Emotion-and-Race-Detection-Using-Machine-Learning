'''
cargo las imagenes que estan en el folder database_images
'''
# Changed import from 'config' to relative import from '.config'
# and aliased as cfg_storage to avoid potential clashes.
import os
# from . import config as cfg_storage  # We will no longer use cfg_storage.path_images directly here
# REMOVED: from .face_recognition_main import rec # THIS WAS THE CIRCULAR IMPORT
from .face_recognition_core import detect_face, get_features  # Explicitly import functions
import cv2
import numpy as np
import traceback


# FIX: Add known_faces_dir parameter to load_images_to_database
def load_images_to_database(known_faces_dir):
    # Use known_faces_dir directly instead of cfg_storage.path_images
    print(f"DEBUG: Attempting to list directory: {known_faces_dir}")
    
    # Ensure the directory exists before trying to list it
    if not os.path.isdir(known_faces_dir):
        print(f"WARNING: Known faces directory not found: {known_faces_dir}. Returning empty database.")
        return [], np.array([])  # Return empty lists if directory doesn't exist

    list_images = os.listdir(known_faces_dir)
    # filto los archivos que no son imagenes
    list_images = [File for File in list_images if File.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]  # Added .png and .bmp, lower() for robustness

    # FIX: Add print to confirm images found
    print(f"DEBUG: Found {len(list_images)} image files in {known_faces_dir}")

    # inicalizo variables
    name = []
    Feats = []
    # ingesta de imagenes
    for file_name in list_images:
        full_path = os.path.join(known_faces_dir, file_name)  # Use known_faces_dir for robustness
        im = cv2.imread(full_path)  # Use full_path to load image

        # --- ADD THIS DEBUG CHECK ---
        if im is None:
            print(f"ERROR: Failed to load image: {full_path}. Skipping this file.")
            continue  # Skip to the next file if image loading fails
        # --- END DEBUG CHECK ---

        # obtengo las caracteristicas del rostro
        box_face = detect_face(im)  # Use direct function import

        # FIX: Ensure feat is a list (even if empty) before trying to get feat[0]
        feat = []
        if box_face:  # Only get features if a face was detected
            feat = get_features(im, box_face)  # Use direct function import

        if len(feat) != 1:
            '''
            esto significa que no hay rostros o hay mas de un rostro
            '''
            print(f"WARNING: Face detection issue in {file_name}: Found {len(feat)} features (expected 1). Skipping.")
            continue
        else:
            # inserto las nuevas caracteristicas en la base de datos
            new_name = os.path.splitext(file_name)[0]  # Use os.path.splitext for robust filename extraction
            if new_name == "":
                print(f"WARNING: File name '{file_name}' resulted in empty user name. Skipping.")
                continue
            name.append(new_name)
            if len(Feats) == 0:
                Feats = np.frombuffer(feat[0], dtype=np.float64)  # Assuming feat[0] is bytes, convert to numpy array
            else:
                Feats = np.vstack((Feats, np.frombuffer(feat[0], dtype=np.float64)))  # Assuming feat[0] is bytes

    # FIX: Add final print to confirm number of loaded faces
    print(f"DEBUG: Successfully loaded {len(name)} known faces into database.")

    if not name:  # If no faces were loaded successfully
        return [], np.array([])
    return name, Feats


# The insert_new_user function is not called in the current main_detector.py flow
# but keeping it here for completeness. If it was to be used for adding new faces,
# it would also need the path_images from config, or a specific directory to save to.
def insert_new_user(rec_face, name, feat, im):
    # 'rec_face' object is passed as an argument, so no import of 'rec' class is needed here.
    # Note: this function previously used cfg_storage.path_images.
    # If this function is intended for adding new users and saving their images,
    # it needs to know where to save them. For now, it's left as is, assuming it
    # might be updated if adding new user functionality is built.
    try:
        rec_face.db_names.append(name)
        if len(rec_face.db_features) == 0:
            rec_face.db_features = np.frombuffer(feat[0], dtype=np.float64)
        else:
            rec_face.db_features = np.vstack((rec_face.db_features, np.frombuffer(feat[0], dtype=np.float64)))
        # guardo la imagen
        # You'll need to define where to save the image if you use this function later.
        # For now, let's assume cfg_storage still provides path_images.
        # If config is removed, this line will cause an error.
        # For now, commenting it out to prevent errors if config is removed.
        # cv2.imwrite(cfg_storage.path_images + os.sep + name + ".jpg", im)
        return 'ok'
    except Exception as ex:
        error = ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
        return error
