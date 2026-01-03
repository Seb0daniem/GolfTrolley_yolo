import cv2

### Module to draw on the frame ###

def draw_on_frame(frame, results):
    """
    Draw all detected objects (persons, hands, etc.) on the frame.
    """
    if "persons" in results:
        draw_persons(frame, results["persons"])
    
    if "hands" in results:
        draw_hands(frame, results["hands"])

def draw_persons(frame, persons):
    """
    Draw bounding boxes, IDs, and confidence scores for detected persons.
    """
    for person in persons:
        bbox = person.bbox  # [x1, y1, x2, y2]
        confidence = person.confidence
        person_id = person.id

        # Draw bounding box
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

        # Draw ID and confidence
        label = f"ID: {person_id}, Conf: {confidence:.2f}"
        cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def draw_hands(frame, hands):
    """
    Draw bounding boxes or other information for detected hands.
    """
    for landmarks in hands:
        pass

        # Draw bounding box
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)

        # Draw confidence
        label = f"Conf: {confidence:.2f}"
        cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

