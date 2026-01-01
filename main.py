from core.video_stream import VideoStream
from core.pipeline import Pipeline
from visualization.video_saver import VideoSaver
from config.loader import load_detector_config
from detection.person_detector import PersonDetector


def main():
    detector_cfg = load_detector_config("config/detector_config.yaml")
    
    #source = 0
    source = "visualization/example_videos/example2.mp4"

    stream = VideoStream(source=source)
    pipeline = Pipeline(person_detector=PersonDetector(**detector_cfg["person_detector"]))
    
    saver = VideoSaver(resolution=stream.get_resolution())

    try:
        while True:
            frame, timestamp = stream.get_frame()
            if frame is None:
                break

            results = pipeline.process_frame(frame, timestamp)
            print(results)
            saver.write_frame(frame, results)

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        stream.release()
        saver.release()
        print("Released resources")
    



if __name__ == "__main__":
    main()
