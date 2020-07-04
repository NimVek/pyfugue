from typing import Any, Callable, Dict, Hashable, NamedTuple, Optional, Set


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
    class Entry(NamedTuple):
        subscriber: Subscriber
        priority: float = 1

    def __init__(self, parent: Optional["Publisher"] = None) -> None:
        self.__subscribers: Dict[Hashable, Set[Publisher.Entry]] = {}
        self.__parent = parent

    def subscribe(
        self, topic: Hashable, subscriber: Subscriber, priority: float = 1
    ) -> None:
        subscribers = self.__subscribers.setdefault(topic, set())
        subscribers.add(Publisher.Entry(subscriber, priority))

    def __entrys(self, topic: Hashable, parent: bool) -> Set["Publisher.Entry"]:
        result: Set[Publisher.Entry] = set()
        if self.__parent and parent:
            result.update(self.__parent.__entrys(topic, parent))
        result.update(self.__subscribers.get(topic, set()))
        return result

    def publish(self, message: Message, parent: bool = True) -> None:
        entrys = self.__entrys(message.topic, parent)
        for i in sorted(entrys, key=lambda x: x.priority, reverse=True):
            i.subscriber(message)
            if message.discarded:
                break


_publisher = Publisher(None)
Publisher.__init__.__defaults__ = (_publisher,)  # type: ignore[attr-defined]
subscribe = _publisher.subscribe
publish = _publisher.publish