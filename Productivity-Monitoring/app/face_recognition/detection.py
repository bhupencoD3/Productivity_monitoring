import cv2
import numpy as np
from retinaface import RetinaFace

def draw_landmarks(frame, landmarks, color=(0, 255, 0)):
    """
    Draw facial landmarks on the frame.
    """
    for point in landmarks:
        cv2.circle(frame, tuple(map(int, point)), 2, color, -1)

def process_frame(frame):
    """
    Detect face and landmarks using RetinaFace.
    """
    # Convert frame to RGB as RetinaFace expects RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform face detection with landmarks
    faces = RetinaFace.detect_faces(rgb_frame)

    if isinstance(faces, dict):  # If faces are detected
        for key, face_info in faces.items():
            # Get the bounding box
            x1, y1, x2, y2 = map(int, face_info['facial_area'])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Get landmarks (eyes, nose, and mouth corners)
            landmarks = face_info['landmarks'].values()
            draw_landmarks(frame, landmarks)

    return frame

def main():
    # Open a video capture (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Process the frame to detect faces and landmarks
        processed_frame = process_frame(frame)

        try:
            # Display the frame (this will work only if GUI support is available)
            cv2.imshow("Face and Eye Detection", processed_frame)
        except cv2.error:
            # Save frames to disk as a fallback
            print("GUI support is not available. Saving frames to disk.")
            cv2.imwrite("output_frame.jpg", processed_frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
