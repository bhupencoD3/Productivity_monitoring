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
        return best_match, max_similarity
    return None, max_similarity

# Main function to demonstrate the workflow
if __name__ == "__main__":
    # Initialize a dictionary to store known embeddings
    known_embeddings = {}

    # Example to add a face to the known database
    print("Registering a new face...")
    img = cv2.imread("path_to_image.jpg")  # Replace with the path to your image
    person_id = "Person_1"
    embedding = register_face(img, facenet)
    if embedding is not None:
        known_embeddings[person_id] = embedding
        print(f"Face registered for {person_id}!")
    else:
        print("No face detected for registration.")

    # Example to recognize a face
    print("Recognizing a face...")
    test_img = cv2.imread("path_to_test_image.jpg")  # Replace with a test image path
    match_id, similarity = recognize_face(test_img, facenet, known_embeddings)
    if match_id:
        print(f"Face recognized as {match_id} with similarity {similarity:.2f}")
    else:
        print("No matching face found.")
