import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Translation API Configuration
TRANSLATION_API_KEY = os.getenv("TRANSLATION_API_KEY")
TRANSLATION_API_URL = os.getenv("TRANSLATION_API_URL", "https://translation.googleapis.com/language/translate/v2")
DETECTION_API_URL = os.getenv("DETECTION_API_URL", "https://translation.googleapis.com/language/translate/v2/detect")

# Rate Limiting Configuration
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # in seconds (1 hour)

# Character Limit Configuration
CHARACTER_LIMIT = int(os.getenv("CHARACTER_LIMIT", "1000"))

# Supported Languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = [
    "en", "es", "fr", "de", "zh", "ja", "ko", "ru", "pt", "ar"
]

# Technical Terms Preservation
TECHNICAL_TERMS_LIST = [
    "SLAM", "ROS", "Gazebo", "Isaac", "VLA", "AI", "ML", "NN", "CNN", "RNN",
    "LSTM", "Transformer", "PID", "PID controller", "kinematics", "dynamics",
    "forward kinematics", "inverse kinematics", "end-effector", "workspace",
    "degrees of freedom", "DOF", "actuator", "sensor", "lidar", "imu",
    "computer vision", "path planning", "motion planning", "control theory",
    "feedback control", "state estimation", "Kalman filter", "particle filter",
    "reinforcement learning", "deep learning", "neural network", "robotics",
    "embodied AI", "physical AI", "humanoid", "manipulation", "locomotion",
    "navigation", "localization", "mapping", "autonomous", "autonomy"
]