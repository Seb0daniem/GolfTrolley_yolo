import time


class FPSCounter:
    def __init__(self):
        self.prev_time = None

    def tick(self):
        now = time.perf_counter()  # högupplöst klocka
        if self.prev_time is None:
            self.prev_time = now
            return None  # fps okänt första gången

        dt = now - self.prev_time
        self.prev_time = now
        return 1.0 / dt if dt > 0 else 0.0
    

def bbox_center_x(bbox, img_w):
    x1, _, x2, _ = bbox
    return ((x1 + x2) / 2) / img_w

