from core.video_stream import VideoStream
from core.pipeline import Pipeline
from visualization.video_saver import VideoSaver
from visualization.draw_on_video import draw_on_frame
from config.loader import load_detector_config
from detection.person_detector import PersonDetector
from detection.hand_detector import HandDetector
from context import Context
from utils import FPSCounter


def main():
    detector_cfg = load_detector_config("config/detector_config.yaml")
    what_to_detect = "both"

    source = 0
    # source = "visualization/example_videos/example3.mp4"

    fps_counter = FPSCounter()
    stream = VideoStream(source=source)
    saver = VideoSaver(resolution=stream.get_resolution())
    context = Context()
    pipeline = Pipeline(
        person_detector=(
            PersonDetector(**detector_cfg["person_detector"])
            if not what_to_detect == "hands"
            else None
        ),
        hand_detector=(
            HandDetector(**detector_cfg["hand_detector"])
            if not what_to_detect == "persons"
            else None
        ),
    )

    try:
        from state_machine.search import Search

        state = Search()  # Start the system in searching state
        frame_id = 0
        fps_count = []  # For calculating average fps
        while True:
            frame, timestamp = stream.get_frame()
            if frame is None:
                break

            frame_id += 1

            # Ensure states never observe stale perception.
            context.perception = None

            # Inference on the frame, detecting persons and hands
            results = pipeline.process_frame(frame, timestamp, frame_id)

            # For state machine

            context.perception = {
                **results,
                "timestamp": timestamp,
                "frame_id": frame_id,
            }

            state = state.update(context)

            # For visualization
            draw_on_frame(frame, results)
            saver.write_frame(frame, results)

            # For fps
            fps = fps_counter.tick()
            if fps is not None:
                fps_count.append(fps)
                # print(f"FPS: {fps:.1f}")

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        if fps_count:
            print(f"Average fps: {sum(fps_count) / len(fps_count)}")
        stream.release()
        saver.release()
        print("Released resources")


if __name__ == "__main__":
    main()
