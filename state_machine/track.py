from state_machine.state_base import StateBase

class Track(StateBase):
    GESTURE_HOLD_SECONDS = 3.0
    GESTURE_DECAY_SECONDS = 0.5
    COOLDOWN_SECONDS = 3.0

    def __init__(self):
        self.gesture_start_time = None
        self.cooldown_start_time = None

    def update(self, ctx):
        frame_id = ctx.perception["frame_id"]
        timestamp = ctx.perception["timestamp"]

        self.move_motors(ctx)

        # Cooldown before looking for hands again
        if ctx.cooldown == True:
            if self.cooldown_start_time is None:
                self.cooldown_start_time = timestamp

            elapsed = timestamp - self.cooldown_start_time
            if elapsed > self.COOLDOWN_SECONDS:
                ctx.cooldown = False

        gesture_to_stop = False
        if ctx.cooldown == False:
            if frame_id % 3 == 0:
                gesture_to_stop = self.search_for_gesture(ctx, timestamp)

            if gesture_to_stop:
                ctx.target_found = False
                ctx.target_lost = True
                from state_machine.stopped import Stopped
                return Stopped()

        return self

    def _decay_gesture_timer(self, timestamp):
        if self.gesture_start_time is None:
            return

        elapsed = timestamp - self.gesture_start_time
        elapsed_after_decay = elapsed - self.GESTURE_DECAY_SECONDS
        if elapsed_after_decay <= 0.0:
            self.gesture_start_time = None
            return

        # Shift start time forward so remaining elapsed is reduced (decay)
        self.gesture_start_time = timestamp - elapsed_after_decay
    
    def search_for_gesture(self, ctx, timestamp):
        list_of_hands = ctx.perception["hands"]
        if list_of_hands:
            matched_this_frame = False
            for hand in list_of_hands:
                if hand.owner_id == ctx.id_to_track and hand.gesture_name == "Open_Palm":
                    matched_this_frame = True
                    if self.gesture_start_time is None:
                        self.gesture_start_time = timestamp
                        print(f"Open palm detected while tracking, starting timer")

                    elapsed = timestamp - self.gesture_start_time
                    print(f"Open palm held for {elapsed} seconds")
                    if elapsed >= self.GESTURE_HOLD_SECONDS:
                        return True
            if not matched_this_frame:
                self._decay_gesture_timer(timestamp)
        else:
            self._decay_gesture_timer(timestamp)

        return False

    def move_motors(self, ctx):
        pass