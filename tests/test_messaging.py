import pytest

from pyfugue.tools.messaging import Message, Publisher


class TestSubscrition:
    @pytest.mark.parametrize("subscriber", [lambda message: print(message.content)])
    def test_register(self, subscriber, capsys):
        publisher = Publisher()
        publisher.subscribe("test", subscriber)
        publisher.publish(Message("test", "content"))

        captured = capsys.readouterr()

        assert captured.out == "content\n"
