class Event(object):
    pass


class MiningEvent(Event):
    def __init__(self, resource, mining_power, inventory=None):
        self.resource = resource
        self.mining_power = mining_power
        self.inventory = inventory
