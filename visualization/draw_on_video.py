import cv2

### Module to draw on the frame ###

def draw_on_frame(frame, results):
    """
    Draw all detected objects (persons, hands, etc.) on the frame.
    """
    if results["persons"] is not None:
        draw_persons(frame, results["persons"])
    
    #if results["hands"] is not None:
     #   draw_hands(frame, results["hands"])

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

    HAND_CONNECTIONS = [
        (0,1),(1,2),(2,3),(3,4),        # Thumb
        (0,5),(5,6),(6,7),(7,8),        # Index
        (5,9),(9,10),(10,11),(11,12),   # Middle
        (9,13),(13,14),(14,15),(15,16), # Ring
        (13,17),(17,18),(18,19),(19,20),# Pinky
        (0,17)                          # Palm base connection
    ]

    for hand in hands:
        h, w = frame.shape[:2]

        pts = [(int(x * w), int(y * h)) for (x, y, _) in hand.landmarks]

        for a, b in HAND_CONNECTIONS:
            if a < len(pts) and b < len(pts):
                cv2.line(frame, pts[a], pts[b], (0, 0, 0), 5, cv2.LINE_AA)
                cv2.line(frame, pts[a], pts[b], (0, 255, 0), 3, cv2.LINE_AA)

        for (x_px, y_px) in pts:
            cv2.circle(frame, (x_px, y_px), 2, (0, 0, 0), -1)
            cv2.circle(frame, (x_px, y_px), 1, (0, 0, 255), -1)
        
        if hand.gesture_name != "None":
            cv2.putText(frame, hand.gesture_name, (x_px, y_px - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)