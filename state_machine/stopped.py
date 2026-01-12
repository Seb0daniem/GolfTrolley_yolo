from state_machine.state_base import StateBase
import time


class Stopped(StateBase):
    def update(self, ctx):
        print("Stopped! Searching in 3 seconds..")

        time.sleep(3)
        from state_machine.search import Search

        return Search()
