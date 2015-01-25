##############################################################
# In-race chat for Assetto Corsa.
# Copyright 2015 Steven Dickinson
# Released under the terms of GPLv3
#############################################################

import ac
import acsys
import math

class InRaceChat:
    MESSAGES_LIMIT = 15

    CHAT_LINE_HEIGHT = 15

    def __init__(self):
        self.messages = []
        self.messageCount = 0

        width = 400
        height = (self.MESSAGES_LIMIT * self.CHAT_LINE_HEIGHT)
        height += 40 # Title area
        height += 40 # Text input
        height += 10 # Padding between text input and messages

        self.appWindow = ac.newApp("In-race Chat")
        ac.setSize(self.appWindow, width, height)

        self.textInput = ac.addTextInput(self.appWindow, "TEXT_INPUT")
        ac.setPosition(self.textInput, 15, height - 40)
        ac.setSize(self.textInput, 360, 30)
        ac.addOnValidateListener(self.textInput, globalValidateInput)

        self.labels = []
        nameX = 10
        nameWidth = 70

        messageX = nameX + nameWidth + 5

        labelY = 40

        for i in range(0, self.MESSAGES_LIMIT):
            row = {
                "author": ac.addLabel(self.appWindow, "author " + repr(i)),
                "message": ac.addLabel(self.appWindow, "message " + repr(i))
            }
            ac.setPosition(row['author'], nameX, labelY)
            ac.setSize(row['author'], nameWidth, 20)
            ac.setFontColor(row['author'], 1, 1, 0, 1)
            ac.setFontSize(row['author'], 12)
            ac.setFontAlignment(row['author'], "right")

            ac.setPosition(row['message'], messageX, labelY)
            ac.setSize(row['message'], width - messageX, 20)
            ac.setFontSize(row['message'], 12)

            self.labels.append(row)
            labelY += self.CHAT_LINE_HEIGHT

        ac.addOnChatMessageListener(self.appWindow, globalChat)

        self.update_messages()

    def onValidateInput(self, string):
        text = ac.getText(self.textInput)
        ac.setText(self.textInput, "")
        ac.setFocus(self.textInput, 1)
        ac.sendChatMessage(text)

    def onChatMessage(self, message, author):
        self.messages.append({'message': message, 'author': author})
        # Save some memory? Later we could have an expandable window?
        if self.messages.__len__() > self.MESSAGES_LIMIT * 2:
            self.messages = self.messages[-self.MESSAGES_LIMIT:]

        self.update_messages()

    def update_messages(self):
        messages = self.messages[-self.MESSAGES_LIMIT:]
        for i in range(self.MESSAGES_LIMIT - 1, -1, -1):
            if i < messages.__len__():
                ac.setText(self.labels[i]['author'], messages[i]['author'] + ":")
                ac.setText(self.labels[i]['message'], messages[i]['message'])
            else:
                ac.setText(self.labels[i]['author'], '')
                ac.setText(self.labels[i]['message'], '')


# Init the plugin
def acMain(ac_version):
    global chat
    chat = InRaceChat()
    return "In-race Chat"

# Binding the events into class methods directly doesn't seem to work,
# so put a bunch of shims in for now. :(.
def globalValidateInput(string):
    global chat
    chat.onValidateInput(string)

def globalChat(message, author):
    global chat
    chat.onChatMessage(message, author)
