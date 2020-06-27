import collections

from typing import (
    Any,
    Callable,
    DefaultDict,
    Hashable,
    NamedTuple,
    NoReturn,
    Optional,
    Set,
)


__all__ = ["Message", "Publisher"]


class Message:
    def __init__(self, topic: Hashable, content: Optional[Any] = None):
        self.topic = topic
        self.content = content
        self.discard: bool = False


Subscriber = Callable[[Message], NoReturn]


class Publisher:
    class Entry(NamedTuple):
        subscriber: Subscriber
        priority: float = 1

    def __init__(self, parent: Optional["Publisher"] = None):
        self.__subscribers: DefaultDict[
            Hashable, Set[Publisher.Entry]
        ] = collections.defaultdict(
            set
        )  # type: ignore[assignment]
        self.parent = parent

    def subscribe(self, topic: Hashable, subscriber: Subscriber, priority: float = 1):
        self.__subscribers[topic].add(Publisher.Entry(subscriber, priority))

    def publish(self, message: Message, to_parent: bool = True):
        for i in self.__subscribers[message.topic]:
            i.subscriber(message)
