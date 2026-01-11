from state_machine.state_base import StateBase

from random import randint

class Search(StateBase):
    def __init__(self):
        self.gesture_start_time = None
        self.last_gesture = None

    def update(self, ctx):
        frame_id = ctx.perception["frame_id"]
        timestamp = ctx.perception["timestamp"]

        if frame_id % 3 == 0:
            #print("Searching..")
            list_of_hands = ctx.perception["hands"]
            tracking_triggered, id_to_track = self.start_search_algorithm(list_of_hands, timestamp)
            if tracking_triggered:
                print("Target found!")
                ctx.target_found = True
                ctx.id_to_track = id_to_track
                from state_machine.track import Track
                return Track()

        return self
    
    def start_search_algorithm(self, hands, timestamp):
        if hands:
            for hand in hands:
                if hand.gesture_name == "Open_Palm":
                    if self.gesture_start_time is None:
                        self.gesture_start_time = timestamp
                        print(f"Open palm detected, starting timer")

                    elapsed = timestamp - self.gesture_start_time

                    print(f"Open palm held for {elapsed} seconds")
                    if elapsed >= 3.0:
                        id_to_track = hand.owner_id
                        
                        return True, id_to_track
                else:
                    self.gesture_start_time = None
        else:
            self.gesture_start_time = None

        return False, None
        