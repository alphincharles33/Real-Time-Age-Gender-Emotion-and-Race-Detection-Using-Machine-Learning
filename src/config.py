import os

# Configuration for model paths and image database
# Paths are relative to the 'src' directory where this config.py resides.

# Get the absolute directory of the current file (config.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the emotion detection model
# Assumes emotion_model.hdf5 is in the 'models' directory, which is one level up from 'src'
# Constructed using os.path.join for cross-platform compatibility
path_model = os.path.join(current_dir, '..', 'models', 'emotion_model.hdf5')

# Image dimensions for emotion detection preprocessing
w, h = 48, 48
rgb = False  # Specifies if the emotion model expects RGB or Grayscale images

# Labels for emotion prediction results
labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Path to the directory containing known face images for recognition
# Assumes known_faces directory is in 'data' directory, which is one level up from 'src'
# Constructed using os.path.join for cross-platform compatibility
path_images = os.path.join(current_dir, '..', 'data', 'known_faces')
