class EventAggregator(object):
    """
    Aggregates events and notifies observers.
    See https://martinfowler.com/eaaDev/EventAggregator.html
    """

    _observers = dict()

    @classmethod
    def notify(cls, event, caller=None):
        """
        Notifies all observers about the `event` from `caller`.
        """
        event_cls = type(event)

        if event_cls not in cls._observers:
            print(f'No observer registered to handle {event}')
            return

        for observer in cls._observers[event_cls]:
            observer(event, caller)

    @classmethod
    def register(cls, f, event_cls):
        """
        Registers a method `f` from an observer to handle events of type `event_cls`.
        """

        if event_cls not in cls._observers:
            cls._observers[event_cls] = []

        if f in cls._observers[event_cls]:
            print(f'{f} is already registered')
            return

        cls._observers[event_cls].append(f)

    @classmethod
    def observers(cls, event_cls):
        """
        Returns the observers handling events of type `event_cls`
        """
        if event_cls not in cls._observers:
            return []

        return cls._observers[event_cls]


class Event(object):
    """
    Event which can be handled by an observer.
    """
    pass


class MiningEvent(Event):
    def __init__(self, resource, mining_power, inventory=None):
        self.resource = resource
        self.mining_power = mining_power
        self.inventory = inventory
