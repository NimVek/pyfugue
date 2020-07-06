from functools import total_ordering
from typing import Any, Callable, Dict, Hashable, Optional, Set

from sortedcontainers import SortedList


__all__ = ["Message", "Publisher", "publish", "subscribe"]


class Message:
    def __init__(self, topic: Hashable, content: Optional[Any] = None) -> None:
        self.topic = topic
        self.content = content
        self.__discarded: bool = False

    def discard(self):
        self.__discarded = True

    @property
    def discarded(self):
        return self.__discarded


Subscriber = Callable[[Message], None]


class Publisher:
    @total_ordering
    class Entry:
        def __init__(self, subscriber: Subscriber, priority: float = 1):
            self.subscriber = subscriber
            self.priority = priority

        def __eq__(self, other):
            if not isinstance(other, Publisher.Entry):
                return False
            else:
                return self.subscriber == other.subscriber

        def __le__(self, other):
            if not isinstance(other, Publisher.Entry):
                return NotImplemented
            elif self.priority > other.priority:
                return True
            elif self.priority == other.priority:
                try:
                    return self.subscriber < other.subscriber  # type: ignore[operator]
                except TypeError:
                    return False
            return False

    def __init__(self, parent: Optional["Publisher"] = None) -> None:
        self.__subscribers: Dict[Hashable, SortedList[Publisher.Entry]] = {}
        self.__parent = parent

    def subscribe(
        self, topic: Hashable, subscriber: Subscriber, priority: float = 1
    ) -> None:
        subscribers = self.__subscribers.setdefault(topic, SortedList())
        subscribers.add(Publisher.Entry(subscriber, priority))

    def __entrys(self, topic: Hashable, parent: bool) -> Set["Publisher.Entry"]:
        result: Set[Publisher.Entry] = SortedList()
        if self.__parent and parent:
            result.update(self.__parent.__entrys(topic, parent))
        result.update(self.__subscribers.get(topic, set()))
        return result

    def publish(self, message: Message, parent: bool = True) -> None:
        for i in self.__entrys(message.topic, parent):
            i.subscriber(message)
            if message.discarded:
                break


_publisher = Publisher(None)
Publisher.__init__.__defaults__ = (_publisher,)  # type: ignore[attr-defined]
subscribe = _publisher.subscribe
publish = _publisher.publish
