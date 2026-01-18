from state_machine.state_base import StateBase
from motion.commands import MotionCommand
from utils import bbox_center_x


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

        id_to_track = ctx.id_to_track
        persons = ctx.perception["persons"]

        # iterate throught persons and return first match of where p.id == id_to_track
        target = next((p for p in persons if p.id == id_to_track), None)
        
        if target is not None:
            target_bbox = target.bbox

            target_center_x = bbox_center_x(target_bbox, ctx.img_height)
            
            x_error = target_center_x - 0.5   # [-0.5, +0.5]

            angular = -x_error * 1.2          # gain, börja här
            linear = 0.3                      # konstant framåt

            ctx.motion_cmd = MotionCommand(
                linear=linear,
                angular=angular
            )

        # If no target, motors stand still
        if target is None:
            ctx.motion_cmd = MotionCommand(0.0, 0.0)
            ctx.target_found = False
            ctx.target_lost = True
            from state_machine.stopped import Stopped

            return Stopped()
        

        # Cooldown before looking for hands again
        if ctx.cooldown:
            if self.cooldown_start_time is None:
                self.cooldown_start_time = timestamp

            elapsed = timestamp - self.cooldown_start_time
            if elapsed > self.COOLDOWN_SECONDS:
                ctx.cooldown = False

        gesture_to_stop = False
        if not ctx.cooldown:
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
                if (
                    hand.owner_id == ctx.id_to_track
                    and hand.gesture_name == "Open_Palm"
                ):
                    matched_this_frame = True
                    if self.gesture_start_time is None:
                        self.gesture_start_time = timestamp
                        print("Open palm detected while tracking, starting timer")

                    elapsed = timestamp - self.gesture_start_time
                    print(f"Open palm held for {elapsed} seconds")
                    if elapsed >= self.GESTURE_HOLD_SECONDS:
                        return True
            if not matched_this_frame:
                self._decay_gesture_timer(timestamp)
        else:
            self._decay_gesture_timer(timestamp)

        return False

