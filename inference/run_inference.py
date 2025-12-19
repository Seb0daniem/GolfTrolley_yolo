### IMPORTS ###
from importlib import metadata
from ultralytics import YOLO


class InferenceRunner:
    def __init__(self, model_path, publisher, subscriber, source=0, classes=0, conf=0.7, stream=True):
        self.model = YOLO(model_path)
        self.publisher = publisher
        self.subscriber = subscriber
        self.source = source
        self.project = "recorded" # Just for folder creation
        self.name = "videos" # Just for folder creation
        self.classes = classes
        self.conf = conf
        self.stream = stream

    def run(self):
        try:
            results = self.model.track(
                source=self.source,
                stream=self.stream, 
                save=True,
                conf=self.conf,
                classes=self.classes,
                project=self.project,
                name=self.name,
            )
            for result in results:
                metadata_list = self._get_metadata_from_frame(result)
                if metadata_list:
                    message = self._create_mqtt_message(metadata_list)
                    self._publish_message(str(message))
                else:
                    self._publish_message(None)
        except KeyboardInterrupt:
            print("\nInference interrupted by user. Cleaning up...")
        finally:
            print("Shutting down inference.")
            if hasattr(self.publisher, "close"):
                self.publisher.close()
            if hasattr(self.subscriber, "close"):
                self.subscriber.close()

    def _get_metadata_from_frame(self, result):
        # Extract metadata from the result object
        metadata_list = []
        for box in result.boxes:
            xyxy = [int(v) for v in box.xyxy[0].tolist()] # [x1, y1, x2, y2]
            obj_id = int(box.id[0]) if box.id is not None else -1
            conf = round(float(box.conf[0]), 2)
            metadata_list.append((xyxy, obj_id, conf))

        return metadata_list
    
    def _create_mqtt_message(self, metadata_list):
        # Create message with all detections for this frame
        detections = []
        for xyxy, obj_id, conf in metadata_list:
            detections.append({
                "id": obj_id,
                "xyxy": xyxy,
                "conf": conf,
            })
        
        return {
            "frame_detections": detections,
            "num_objects": len(detections)
        }

    def _publish_message(self, message: str):
        self.publisher.publish(message)