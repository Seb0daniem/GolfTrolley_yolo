### The pipeline for the project ###

class Pipeline:
    def __init__(self, person_detector, hand_detector):
        self.person_detector = person_detector
        self.hand_detector = hand_detector

    def process_frame(self, frame, timestamp):
        
        #persons_detected = self.person_detector.detect(frame)
        hands_results = self.hand_detector.detect(frame)
        

        return {
            "persons": [],
            "hands": hands_results
        }
