import pytest

from pyfugue.tools.messaging import Message, Publisher, publish, subscribe


class TestSubscrition:
    @pytest.mark.parametrize("subscriber", [lambda message: print(message.content)])
    def test_register(self, subscriber, capsys):
        publisher = Publisher(None)
        publisher.subscribe("test", subscriber)
        publisher.publish(Message("test", "local"))

        captured = capsys.readouterr()

        assert captured.out == "local\n"

    @pytest.mark.parametrize(
        "topic, output", [("subscribed", "subscribed\n"), ("notsubscribed", "")]
    )
    def test_topic(self, topic, output, capsys):
        publisher = Publisher(None)
        publisher.subscribe("subscribed", lambda message: print(message.topic))
        publisher.publish(Message(topic, topic))

        captured = capsys.readouterr()

        assert captured.out == output


class TestPriorityDiscard:
    @pytest.mark.parametrize(
        "subscriber, output",
        [
            (
                (
                    (lambda message: print("first"), 100),
                    (lambda message: print("second"), 0),
                ),
                "first\nsecond\n",
            ),
            (
                (
                    (lambda message: print("first"), -100),
                    (lambda message: print("second"), 0),
                ),
                "second\nfirst\n",
            ),
        ],
    )
    def test_order(self, subscriber, output, capsys):
        publisher = Publisher(None)
        for i in subscriber:
            publisher.subscribe("test", i[0], i[1])
        publisher.publish(Message("test", "order"))

        captured = capsys.readouterr()

        assert captured.out == output

    def test_discard(self, capsys):
        def discard(message):
            message.discard = True

        publisher = Publisher(None)
        publisher.subscribe("test", lambda x: print("first"), 100)
        publisher.subscribe("test", discard, 50)
        publisher.subscribe("test", lambda x: print("second"))
        publisher.publish(Message("test", "discard"))

        captured = capsys.readouterr()

        assert captured.out == "first\n"


class TestGlobal:
    @pytest.mark.parametrize("subscriber", [lambda message: print(message.content)])
    def test_register_global(self, subscriber, capsys):
        subscribe("test", subscriber)
        publish(Message("test", "global"))

        captured = capsys.readouterr()

        assert captured.out == "global\n"
