from collections import defaultdict
from threading import Thread


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type, handler):
        self._subscribers[event_type].append(handler)

    def publish(self, event_type, data):
        for handler in self._subscribers[event_type]:
            Thread(target=handler, args=(event_type, data), daemon=True).start()

    def publish_sync(self, event_type, data):
        for handler in self._subscribers[event_type]:
            handler(event_type, data)
