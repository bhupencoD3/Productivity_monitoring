import os

# Define the directory structure
structure = {
    "TusharKoshti-1-Productivity-Monitoring": [
        "README.md",
        "Dockerfile",
        "LICENSE",
        "docker-compose.yml",
        "requirements.txt",
        ".env",
        {
            "app": [
                "config.py",
                "dependencies.py",
                "exceptions.py",
                "logging_config.py",
                "factory.py",
                "main.py",
                {
                    "api": [
                        "__init__.py",
                        {
                            "controllers": ["__init__.py", "users_controller.py"],
                            "errors": ["__init__.py", "http_exceptions.py"]
                        }
                    ]
                },
                {
                    "client": ["__init__.py", "user_client.py"]
                },
                {
                    "dao": ["__init__.py", "user_dao.py"]
                },
                {
                    "service": ["__init__.py", "user_service.py"]
                },
                {
                    "utils": ["__init__.py", "auth_utils.py"]
                },
                {
                    "face_recognition": [
                        "__init__.py",
                        "detection.py",
                        "alignment.py",
                        "recognition.py",
                        "tracking.py"
                    ]
                },
                {
                    "models": ["__init__.py", "retinaface_model.pth", "facenet_model.pth"]
                },
                {
                    "data": ["__init__.py", "user_embeddings.pkl", "sample_faces/"]
                }
            ]
        },
        {
            "tests": [
                "test_users_controller.py",
                "test_user_service.py",
                "test_user_dao.py",
                "test_auth_utils.py",
                "conftest.py"
            ]
        }
    ]
}

# Recursive function to create directories and files
def create_structure(base_path, struct):
    for item in struct:
        if isinstance(item, dict):
            for folder, contents in item.items():
                folder_path = os.path.join(base_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                create_structure(folder_path, contents)
        else:
            file_path = os.path.join(base_path, item)
            if "." in item:  # Create file
                with open(file_path, "w") as f:
                    pass
            else:  # Create folder
                os.makedirs(file_path, exist_ok=True)

# Base directory
base_dir = "TusharKoshti-1-Productivity-Monitoring"
create_structure(".", [{base_dir: structure[base_dir]}])
