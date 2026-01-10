from state_machine.state_base import StateBase

from random import randint

class Track(StateBase):
    def update(self, ctx):
        print(f"Tracking {ctx.id_to_track}..")

        nbr = randint(1, 5)
        if nbr == 1:
            print("Target lost! :O")
            ctx.target_found = False
            ctx.target_lost = True
            from state_machine.stopped import Stopped
            return Stopped()

        return self