import base64
import cv2
from deepface import DeepFace
import numpy as np


def detect_emotion(base64_image_string):
    """Decodes a base64 frame from the webcam and uses DeepFace to analyze mood.

    Handles edge cases like missing face or corrupted frames gracefully.
    """
    try:
        if not base64_image_string:
            return "neutral", {}

        # 1. Parse base64 header and decode image
        header, encoded = base64_image_string.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        # 2. Convert bytes to OpenCV frame
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return "neutral", {}

        # 3. Analyze emotion with DeepFace
        analysis = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)

        # Handle edge case where no face is detected
        if not analysis or len(analysis) == 0:
            return "neutral", {}

        first_face = analysis[0]
        dominant_mood = str(first_face.get("dominant_emotion", "neutral"))

        # 4. CONVERT NUMPY FLOAT32 -> PYTHON FLOAT (Fixes JSON error!)
        raw_scores = first_face.get("emotion", {})
        all_scores = {k: float(v) for k, v in raw_scores.items()}

        return dominant_mood, all_scores

    except Exception as e:
        print(f"[Error in mood_detector]: {str(e)}")
        return "neutral", {}