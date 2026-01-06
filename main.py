from core.video_stream import VideoStream
from core.pipeline import Pipeline
from visualization.video_saver import VideoSaver
from visualization.draw_on_video import draw_on_frame
from config.loader import load_detector_config
from detection.person_detector import PersonDetector
from detection.hand_detector import HandDetector
from context import Context


def main():
    detector_cfg = load_detector_config("config/detector_config.yaml")
    what_to_detect = "hands"
    
    #source = 0
    source = "visualization/example_videos/example3.mp4"

    stream = VideoStream(source=source)
    context = Context()
    pipeline = Pipeline(
        person_detector=PersonDetector(**detector_cfg["person_detector"]) if not what_to_detect == "hands" else None,
        hand_detector=HandDetector(**detector_cfg["hand_detector"]) if not what_to_detect == "persons" else None
    )
    
    saver = VideoSaver(resolution=stream.get_resolution())

    try:
        from state_machine.search import Search
        state = Search() # Start the system in searching state
        frame_id = 0
        while True:
            frame, timestamp = stream.get_frame()
            if frame is None:
                break

            # Ensure states never observe stale perception.
            context.perception = None

            results = pipeline.process_frame(frame, timestamp)
            frame_id += 1
            context.perception = {
                **results,
                "timestamp": timestamp,
                "frame_id": frame_id,
            }
            
            state = state.update(context)

            # For visualization
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
