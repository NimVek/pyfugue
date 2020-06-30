import pytest

from pyfugue.contrib.messaging import Message, Publisher, publish, subscribe


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
            message.discard()

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


class TestPropagation:
    @pytest.mark.parametrize(
        "topic, propagate, output",
        [("propagate", True, "global\nlocal\n"), ("nopropagate", False, "local\n")],
    )
    def test_propagate(self, topic, propagate, output, capsys):
        subscribe(topic, lambda x: print("global"), 50)
        publisher = Publisher()
        publisher.subscribe(topic, lambda x: print("local"), 25)
        publisher.publish(Message(topic), propagate)

        captured = capsys.readouterr()

        assert captured.out == output


class TestComplex:
    def test_register_global(self, capsys):
        subscribe("complex", lambda x: print("complex_global"), 50)
        p1 = Publisher()
        p1.subscribe("complex", lambda x: print("complex_p1"), 25)
        p2 = Publisher()
        p2.subscribe("complex", lambda x: print("complex_p2"), 20)

        p1.publish(Message("complex", "complex"))
        print(":next:")
        p2.publish(Message("complex", "complex"))
        print(":next:")
        p1.publish(Message("complex", "complex"), False)

        captured = capsys.readouterr()

        assert (
            captured.out == "complex_global\ncomplex_p1\n:next:\n"
            "complex_global\ncomplex_p2\n:next:\n"
            "complex_p1\n"
        )
