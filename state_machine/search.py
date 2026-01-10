from state_machine.state_base import StateBase

from random import randint

class Search(StateBase):
    def update(self, ctx):
        print("Searching..")
        list_of_persons = ctx.perception["persons"]
        list_of_hands = ctx.perception["hands"]
        result = self.start_search_algorithm(list_of_persons, list_of_hands)
        if result:
            print("Target found!")
            ctx.target_found = True
            from state_machine.track import Track
            return Track()

        return self
    
    def start_search_algorithm(self, persons, hands):
        if persons:
            #print(persons)
            #print(hands)
            pass
        