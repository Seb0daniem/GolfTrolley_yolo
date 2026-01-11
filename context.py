class Context:
    def __init__(self):
        self.target_found = False
        self.target_lost = False
        self.should_stop = False
        self.id_to_track = None
        self.cooldown = False

        # Per-tick perception snapshot (set by main loop). Either a dict (fresh for
        # the current tick) or None.
        self.perception = None


