# Corrected import for f_Face_info module now directly in src/
from . import f_Face_info
import os  # Import the os module for path operations and directory creation

import cv2
import time
import imutils
import argparse

parser = argparse.ArgumentParser(description="Face Info")
parser.add_argument('--input', type=str, default='webcam',  # Keep default as 'webcam'
                    help="webcam or image")
parser.add_argument('--path_im', type=str, default='data/known_faces/face1.png',
                    help="path of image to process")
args = vars(parser.parse_args())

type_input = args['input']
# args['path_im'] = 'data/known_faces/face1.png' # This line should be commented or removed for webcam mode

# --- Define output directory (still good practice for potential future saving) ---
output_dir = 'output_faces'
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

if type_input == 'image':
    input_image_path = args['path_im']
    frame = cv2.imread(input_image_path)

    if frame is None:
        print(f"Error: Could not load image from {input_image_path}. Please check the path and file integrity.")
    else:
        print(f"📸 Processing image: {input_image_path}")
        out = f_Face_info.get_face_info(frame)

        text_output = []
        text_output.append(f"Analysis Results for: {os.path.basename(input_image_path)}\n")

        if out and len(out) > 0:
            for i, info in enumerate(out):
                if 'bbx_frontal_face' in info and len(info['bbx_frontal_face']) > 0:
                    name = info.get('name', 'N/A')
                    age = info.get('age', 'N/A')
                    gender = info.get('gender', 'N/A')
                    race = info.get('race', 'N/A')
                    emotion = info.get('emotion', 'N/A')

                    result_line = f"  Face {i+1}:\n" \
                                  f"    Name: {name}\n" \
                                  f"    Age: {age}\n" \
                                  f"    Gender: {gender}\n" \
                                  f"    Race: {race}\n" \
                                  f"    Emotion: {emotion}\n"
                    text_output.append(result_line)
                    print(result_line)
                else:
                    text_output.append(f"  Face {i+1}: No detailed analysis (bounding box missing or empty).\n")
                    print(f"  Face {i+1}: No detailed analysis (bounding box missing or empty).")
        else:
            text_output.append("No faces detected in the image.\n")
            print("No faces detected in the image.")

        res_img = f_Face_info.bounding_box(out, frame)

        base_filename = os.path.basename(input_image_path)
        name_without_ext = os.path.splitext(base_filename)[0]
        output_image_path = os.path.join(output_dir, f"{name_without_ext}_processed.png")

        cv2.imwrite(output_image_path, res_img)
        print(f"🖼️ Processed image saved to: {output_image_path}")

        output_text_path = os.path.join(output_dir, f"{name_without_ext}_analysis.txt")
        with open(output_text_path, 'w') as f:
            f.writelines(text_output)
        print(f"📝 Analysis results saved to: {output_text_path}")

        # cv2.imshow('Face info',res_img) # Still commented if not needed for image mode
        # cv2.waitKey(0) # Still commented if not needed for image mode

elif type_input == 'webcam':
    # --- UNCOMMENT THESE LINES FOR LIVE WEBCAM DISPLAY ---
    cv2.namedWindow("Face info")  # UNCOMMENT THIS
    cam = cv2.VideoCapture(0)  # 0 is typically the default webcam

    if not cam.isOpened():
        print("Error: Could not open video stream. Check webcam connection or permissions.")
        exit()  # Exit if webcam cannot be opened

    print("Webcam opened successfully. Displaying live feed. Press 'q' to quit.")

    frame_count = 0
    while True:
        star_time = time.time()
        ret, frame = cam.read()

        if not ret or frame is None:
            print("Failed to grab frame, exiting...")
            break

        frame = imutils.resize(frame, width=720)

        out = f_Face_info.get_face_info(frame)

        if out and len(out) > 0 and 'bbx_frontal_face' in out[0] and len(out[0]['bbx_frontal_face']) > 0:
            info = out[0]
            name = info.get('name', 'N/A')
            age = info.get('age', 'N/A')
            gender = info.get('gender', 'N/A')
            race = info.get('race', 'N/A')
            emotion = info.get('emotion', 'N/A')

            # You can choose to print to console or just rely on display
            # print(f"Frame {frame_count}: Detected Face - Name: {name}, Age: {age}, Gender: {gender}, Race: {race}, Emotion: {emotion}")
        else:
            pass

        res_img = f_Face_info.bounding_box(out, frame)  # UNCOMMENT THIS

        end_time = time.time() - star_time
        FPS = 1 / end_time
        cv2.putText(res_img, f"FPS: {round(FPS, 3)}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)  # UNCOMMENT THIS
        cv2.imshow('Face info', res_img)  # UNCOMMENT THIS
        if cv2.waitKey(1) & 0xFF == ord('q'):  # UNCOMMENT THIS
            break

        frame_count += 1

    cam.release()
    cv2.destroyAllWindows()  # UNCOMMENT THIS
    print("Webcam released. Exiting.")
