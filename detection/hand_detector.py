import mediapipe as mp
import cv2
from core.data_types import Hand

class HandDetector:
    def __init__(self, model_path):

        # === SHORTCUTS TO THE TASKS API (Just makes things more readable) ===
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        RunningMode = mp.tasks.vision.RunningMode
        GestureRecognizer = mp.tasks.vision.GestureRecognizer

        options = GestureRecognizerOptions(
                    base_options=BaseOptions(model_asset_path=model_path),
                    running_mode=RunningMode.IMAGE,
                    num_hands=2,
                    )

        self.recognizer = GestureRecognizer.create_from_options(options)

        print("HandDetector initialized")

    def detect(self, frame):
        hands = []

        # MediaPipe expects RGB images. OpenCV gives BGR.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        results = self.recognizer.recognize(mp_image)

        # Length of hand_landmarks is the amount of hands in the image
        for hand_idx in range(len(results.hand_landmarks)):
            # ---- Gesture ----
            gesture_name = None
            confidence = None

            if results.gestures:
                best_gesture = results.gestures[hand_idx][0]
                gesture_name = best_gesture.category_name
                confidence = best_gesture.score

            # ---- Landmarks ----
            landmarks = results.hand_landmarks[hand_idx]
            landmarks_list = [[lm.x, lm.y, lm.z] for lm in landmarks]

            hand = Hand(
                gesture_name=gesture_name,
                landmarks=landmarks_list,
                confidence=confidence
            )

            hands.append(hand)

        return hands

            




    

        