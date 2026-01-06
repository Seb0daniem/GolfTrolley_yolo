from state_machine.state_base import StateBase

from random import randint

class Search(StateBase):
    def update(self, ctx):
        print("Searching..")

        nbr = randint(1, 5)
        if nbr == 1:
            print("Target found!")
            ctx.target_found = True
            from state_machine.track import Track
            return Track()

        return self