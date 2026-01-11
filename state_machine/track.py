from state_machine.state_base import StateBase

class Track(StateBase):
    def __init__(self):
        self.gesture_start_time = None

    def update(self, ctx):
        frame_id = ctx.perception["frame_id"]
        timestamp = ctx.perception["timestamp"]

        print(f"Tracking ID: {ctx.id_to_track}..")

        self.move_motors(ctx)

        gesture_to_stop = False
        if frame_id % 3 == 0:
            gesture_to_stop = self.search_for_gesture(ctx, timestamp)

        if gesture_to_stop:
            ctx.target_found = False
            ctx.target_lost = True
            from state_machine.stopped import Stopped
            return Stopped()

        return self
    
    def search_for_gesture(self, ctx, timestamp):
        print("Looking for gestures")
        list_of_hands = ctx.perception["hands"]
        if list_of_hands:
            for hand in list_of_hands:
                if hand.owner_id == ctx.id_to_track and hand.gesture_name == "Open_Palm":
                    if self.gesture_start_time is None:
                        self.gesture_start_time = timestamp
                        print(f"Open palm detected while tracking, starting timer")

                    elapsed = timestamp - self.gesture_start_time
                    print(f"Open palm held for {elapsed} seconds")
                    if elapsed >= 0.1:
                        return True
                
                else:
                    self.gesture_start_time = None
        else:
            self.gesture_start_time = None

    def move_motors(self, ctx):
        print(f"Moving motors to follow ID: {ctx.id_to_track}")