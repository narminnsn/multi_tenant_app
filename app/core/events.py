class EventDispatcher:
    _listeners = {}

    @classmethod
    def register(cls, event_type: str, listener):
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        cls._listeners[event_type].append(listener)

    @classmethod
    def dispatch(cls, event_type: str, data):
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                listener.handle_event(data)


class Event:
    def __init__(self, event_type: str, data):
        self.event_type = event_type
        self.data = data
