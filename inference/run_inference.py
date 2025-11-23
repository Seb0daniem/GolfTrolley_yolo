### IMPORTS ###
from ultralytics import YOLO

### CODE ###

def main():
    # Load model
    model = YOLO("models/yolo11l.engine")

    # For saving video, recorded and videos will become folders
    project = "recorded"
    name = "videos"

    # Run prediction on an image
    results = model.track(
        source=0,
        conf=0.7,
        save=True,
        save_dir="recorded",
        stream=True,
        show=True,
        classes=0,
        project=project,
        name=name,
    )

    # Print results
    for r in results:
        print(r)  # print detected bounding boxes

if __name__ == "__main__":
    main()