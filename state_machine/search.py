from state_machine.state_base import StateBase

from random import randint

class Search(StateBase):
    def update(self, ctx):
        print("Searching..")
        print(f"ctx perception: {ctx.perception}")
        if ctx.perception["hands"]:
            print("Händer finns")
            if ctx.perception["hands"][0].gesture_name is not None:
                print("Target found!")
                ctx.target_found = True
                from state_machine.track import Track
                return Track()

        return self
    
    def start_search_algorithm(self, persons, hands):
        pass