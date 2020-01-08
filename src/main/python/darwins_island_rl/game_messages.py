import textwrap

import tcod


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        new_message_lines = textwrap.wrap(message.text, self.width)

        for msg in new_message_lines:
            if len(self.messages) == self.height:
                del self.messages[0]

            self.messages.append(Message(msg, message.color))
