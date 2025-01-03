import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import cv2
import numpy as np
from PIL import Image

# Load the FaceNet model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
facenet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Load MTCNN for face detection
mtcnn = MTCNN(keep_all=True, device=device)

# Function to extract embeddings from a face
def get_face_embedding(image, facenet_model):
    """Extract face embedding from a given image using FaceNet."""
    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image)

    # Detect faces and crop
    boxes, _ = mtcnn.detect(image_pil)
    if boxes is None:
        return None  # No face detected

    # Get the first face (assuming one face for simplicity)
    face_image = mtcnn.extract(image_pil, boxes, save_path=None)
    if face_image is None or len(face_image) == 0:
        return None

    # Prepare the face tensor
    face_tensor = face_image[0].to(device)

    # Get embedding from FaceNet
    embedding = facenet_model(face_tensor.unsqueeze(0))
    return embedding.detach().cpu().numpy()

# Function to calculate similarity (cosine similarity)
def cosine_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two embeddings."""
    embedding1 = embedding1 / np.linalg.norm(embedding1)
    embedding2 = embedding2 / np.linalg.norm(embedding2)
    return np.dot(embedding1, embedding2.T)

# Register a face
def register_face(image, facenet_model):
    """Register a face and return its embedding."""
    return get_face_embedding(image, facenet_model)

# Recognize a face
# Recognize a face
def recognize_face(image, facenet_model, known_embeddings, threshold=0.7):
    """
    Recognize a face by comparing with known embeddings.
    Returns the ID of the closest match or None if no match is found.
    """
    face_embedding = get_face_embedding(image, facenet_model)
    if face_embedding is None:
        return None, None  # No face detected

    # Compare with known embeddings
    max_similarity = 0
    best_match = None
    for person_id, embedding in known_embeddings.items():
        similarity = cosine_similarity(face_embedding, embedding)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = person_id

    # Check if the match is above the threshold
    if max_similarity >= threshold:
        return best_match, float(max_similarity)  # Just use float(max_similarity)
    return None, float(max_similarity)  # Use float(max_similarity)

# Main function to demonstrate the workflow
if __name__ == "__main__":
    # Initialize a dictionary to store known embeddings
    known_embeddings = {}

    # Example to add a face to the known database
    print("Registering a new face...")
    img = cv2.imread("Productivity-Monitoring/app/face_recognition/1.png")  # Replace with the path to your image
    person_id = "Person_1"
    embedding = register_face(img, facenet)
    if embedding is not None:
        known_embeddings[person_id] = embedding
        print(f"Face registered for {person_id}!")
    else:
        print("No face detected for registration.")

    # Start capturing the video feed from the webcam
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Process the frame to detect and recognize the face
        match_id, similarity = recognize_face(frame, facenet, known_embeddings)
        
        # Display the frame with recognition results
        if match_id:
            label = f"Face recognized as {match_id} with similarity {similarity:.2f}"
            cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "No matching face found", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Show the live webcam feed
        cv2.imshow("Webcam - Face Recognition", frame)

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
