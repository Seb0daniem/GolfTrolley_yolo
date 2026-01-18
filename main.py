from core.video_stream import VideoStream
from core.pipeline import Pipeline
from visualization.video_saver import VideoSaver
from visualization.draw_on_video import draw_on_frame
from config.loader import load_detector_config
from detection.person_detector import PersonDetector
from detection.hand_detector import HandDetector
from context import Context
from utils import FPSCounter

from mcu_handler.communication.serial_link import SerialLink
from mcu_handler.hardware.arduino import Arduino

from motion.commands import MotionCommand
from motion.controller import MotionController



def main():
    detector_cfg = load_detector_config("config/detector_config.yaml")
    what_to_detect = "both"

    source = 0
    #source = "visualization/example_videos/example3.mp4"

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

    serial_link = SerialLink(port="/dev/ttyUSB0", baudrate=115200)
    arduino = Arduino(serial_link)
    motion_controller = MotionController(arduino)
    context.motion_controller = motion_controller

    required_keys = {"distance_cm", "estop"}

    try:
        from state_machine.search import Search

        state = Search()  # Start the system in searching state
        frame_id = 0
        fps_count = []  # For calculating average fps
        while True:
            frame, timestamp = stream.get_frame()
            if frame is None:
                break
            
            context.img_height = int(frame.shape[0])
            context.img_width  = int(frame.shape[1])

            arduino_status = arduino.read_status()
            if arduino_status is None:
                continue

            if not required_keys.issubset(arduino_status.keys()):
                continue

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
                "distance": arduino_status["distance_cm"]
            }

            state = state.update(context)

            if context.motion_cmd is not None and context.motion_controller is not None:
                context.motion_controller.update(context.motion_cmd)


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
        serial_link.close()
        print("Released resources")


if __name__ == "__main__":
    main()
