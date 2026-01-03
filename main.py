from core.video_stream import VideoStream
from core.pipeline import Pipeline
from visualization.video_saver import VideoSaver
from visualization.draw_on_video import draw_on_frame
from config.loader import load_detector_config
from detection.person_detector import PersonDetector
from detection.hand_detector import HandDetector


def main():
    detector_cfg = load_detector_config("config/detector_config.yaml")
    
    #source = 0
    source = "visualization/example_videos/example3.mp4"

    stream = VideoStream(source=source)
    pipeline = Pipeline(person_detector=None,
                        hand_detector=HandDetector(**detector_cfg["hand_detector"])
                        )
    #pipeline = Pipeline(person_detector=PersonDetector(**detector_cfg["person_detector"]),
     #                   hand_detector=None
      #                  )
    
    saver = VideoSaver(resolution=stream.get_resolution())

    try:
        while True:
            frame, timestamp = stream.get_frame()
            if frame is None:
                break

            results = pipeline.process_frame(frame, timestamp)
            
            draw_on_frame(frame, results)
            saver.write_frame(frame, results)

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        stream.release()
        saver.release()
        print("Released resources")
    



if __name__ == "__main__":
    main()
