from typing import Protocol


class PresenterProtocol(Protocol):
    def update_view(self) -> None:
        pass


class Publisher:
    def __init__(self):
        self._selected_node = None
        self._observers = []

    @property
    def selected_node(self):
        return self._selected_node

    @selected_node.setter
    def selected_node(self, new_node):
        if new_node != self._selected_node:
            self._selected_node = new_node
            self.notify_observers()

    def register_observer(self, observer: PresenterProtocol):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer: PresenterProtocol):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observer(self, observer: PresenterProtocol):
        if observer in self._observers:
            observer.update_view()

    def notify_observers(self):
        for observer in self._observers:
            observer.update_view()
