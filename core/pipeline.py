### The pipeline for the project ###

class Pipeline:
    def __init__(self, person_detector):
        self.person_detector = person_detector

    def process_frame(self, frame, timestamp):
        
        persons_detected = self.person_detector.detect(frame)

        return {
            "persons": persons_detected,
            "hands": [],
            "gestures": []
        }
