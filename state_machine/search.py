from state_machine.state_base import StateBase

from random import randint


class Search(StateBase):
    GESTURE_HOLD_SECONDS = 3.0
    GESTURE_DECAY_SECONDS = 0.5

    def __init__(self):
        self.gesture_start_time = None

    def update(self, ctx):
        frame_id = ctx.perception["frame_id"]
        timestamp = ctx.perception["timestamp"]

        if frame_id % 3 == 0:
            list_of_hands = ctx.perception["hands"]
            tracking_triggered, id_to_track = self.start_search_algorithm(
                list_of_hands, timestamp
            )
            if tracking_triggered:
                print("Target found!")
                ctx.target_found = True
                ctx.id_to_track = id_to_track
                ctx.cooldown = True  # Cooldown before looking for hands again
                from state_machine.track import Track

                return Track()

        return self

    def _decay_gesture_timer(self, timestamp):
        if self.gesture_start_time is None:
            return

        elapsed = timestamp - self.gesture_start_time
        elapsed_after_decay = elapsed - self.GESTURE_DECAY_SECONDS
        if elapsed_after_decay <= 0.0:
            self.gesture_start_time = None
            return

        self.gesture_start_time = timestamp - elapsed_after_decay

    def start_search_algorithm(self, hands, timestamp):
        if hands:
            matched_this_frame = False
            for hand in hands:
                if hand.gesture_name == "Open_Palm":
                    matched_this_frame = True
                    if self.gesture_start_time is None:
                        self.gesture_start_time = timestamp
                        print(f"Open palm detected, starting timer")

                    elapsed = timestamp - self.gesture_start_time

                    print(f"Open palm held for {elapsed} seconds")
                    if elapsed >= self.GESTURE_HOLD_SECONDS:
                        id_to_track = hand.owner_id

                        return True, id_to_track
            if not matched_this_frame:
                self._decay_gesture_timer(timestamp)
        else:
            self._decay_gesture_timer(timestamp)

        return False, None
