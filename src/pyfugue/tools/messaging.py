from typing import Any, Callable, Dict, Hashable, NamedTuple, Optional, Set


__all__ = ["Message", "Publisher", "publish", "subscribe"]


class Message:
    def __init__(self, topic: Hashable, content: Optional[Any] = None) -> None:
        self.topic = topic
        self.content = content
        self.discard: bool = False


Subscriber = Callable[[Message], None]

_publisher: Optional["Publisher"] = None


class Publisher:
    class Entry(NamedTuple):
        subscriber: Subscriber
        priority: float = 1

    def __init__(self, parent: Optional["Publisher"] = _publisher) -> None:
        self.__subscribers: Dict[Hashable, Set[Publisher.Entry]] = {}
        self.__parent = parent

    def subscribe(
        self, topic: Hashable, subscriber: Subscriber, priority: float = 1
    ) -> None:
        if topic not in self.__subscribers:
            self.__subscribers[topic] = set()
        self.__subscribers[topic].add(Publisher.Entry(subscriber, priority))

    def __entrys(self, topic: Hashable, parent: bool) -> Set["Publisher.Entry"]:
        result: Set[Publisher.Entry] = self.__subscribers.get(topic, set())
        if self.__parent and parent:
            result.update(self.__parent.__entrys(topic, parent))
        return result

    def publish(self, message: Message, parent: bool = True) -> None:
        entrys = self.__entrys(message.topic, parent)
        for i in sorted(entrys, key=lambda x: x.priority, reverse=True):
            i.subscriber(message)
            if message.discard:
                break


_publisher = Publisher(None)
subscribe = _publisher.subscribe
publish = _publisher.publish
