"""
Implementation of the observer pattern.
https://en.wikipedia.org/wiki/Observer_pattern
"""

from abc import abstractmethod


class Observable(object):
    def __init__(self, *args, **kwargs):
        self._observers = []

    def register_observer(self, observer):
        """
        Registers an observer to receive notifications from the observable.
        """

        self._observers.append(observer)

    def deregister_observer(self, observer):
        """
        Deregisters an observer from the observable.
        """

        self._observers.remove(observer)

    def notify_observers(self, event, *args, **kwargs):
        """
        Notifies all observers about a specific event.
        """

        for observer in self._observers:
            observer.notify(self, event, *args, **kwargs)


class Observer(object):
    @abstractmethod
    def notify(self, observable, event, *args, **kwargs):
        """
        Notifies the observer about an event from the observable.
        """

        pass
