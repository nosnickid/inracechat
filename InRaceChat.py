##############################################################
# In-race chat for Assetto Corsa.
# Copyright 2015 Steven Dickinson
# Released under the terms of GPLv3
#############################################################

import ac
import acsys
import math


class InRaceChat:
    CHAT_LINE_HEIGHT = 15

    def __init__(self):
        self.messages = []
        self.historySize = 10

        self.unusedLabels = []
        self.labels = []

        self.delayedChat = None

        self.firstLayout = True

        self.appWindow = ac.newApp("In-race Chat")
        self.textInput = ac.addTextInput(self.appWindow, "TEXT_INPUT")
        ac.addOnValidateListener(self.textInput, globalValidateInput)

        self.shrinkButton = ac.addButton(self.appWindow, "-")
        self.expandButton = ac.addButton(self.appWindow, "+")

        ac.addOnClickedListener(self.shrinkButton, globalShrinkButtonClicked)
        ac.addOnClickedListener(self.expandButton, globalExpandButtonClicked)

        ac.addOnChatMessageListener(self.appWindow, globalChat)

        self.initGui()


    def initGui(self):
        width = 400
        height = (self.historySize * self.CHAT_LINE_HEIGHT)
        height += 40  # Title area
        height += 40  # Text input
        height += 10  # Padding between text input and messages

        ac.setSize(self.appWindow, width, height)
        ac.setPosition(self.textInput, 15, height - 40)
        ac.setSize(self.textInput, 360, 30)

        if self.firstLayout:
            ac.setPosition(self.shrinkButton, width - 50, 40)
            ac.setSize(self.shrinkButton, 20, 20)
            ac.setPosition(self.expandButton, width - 25, 40)
            ac.setSize(self.expandButton, 20, 20)
            self.firstLayout = False

        for row in self.labels:
            ac.setVisible(row['author'], 0)
            ac.setVisible(row['message'], 0)

        self.unusedLabels = self.labels

        self.labels = []
        nameX = 10
        nameWidth = 70

        messageX = nameX + nameWidth + 5

        labelY = 40

        for i in range(0, self.historySize):
            row = self.getUnusedRow()
            ac.setPosition(row['author'], nameX, labelY)
            ac.setSize(row['author'], nameWidth, 20)
            ac.setFontColor(row['author'], 1, 1, 0, 1)
            ac.setFontSize(row['author'], 12)
            ac.setFontAlignment(row['author'], "right")

            ac.setPosition(row['message'], messageX, labelY)
            ac.setSize(row['message'], width - messageX, 20)
            ac.setFontSize(row['message'], 12)

            ac.setVisible(row['author'], 1)
            ac.setVisible(row['message'], 1)

            self.labels.append(row)
            labelY += self.CHAT_LINE_HEIGHT

        self.update_messages()

    def getUnusedRow(self):
        if len(self.unusedLabels) > 0:
            return self.unusedLabels.pop()
        else:
            return {
                "author": ac.addLabel(self.appWindow, "author"),
                "message": ac.addLabel(self.appWindow, "message")
            }

    def onValidateInput(self, string):
        text = ac.getText(self.textInput)
        ac.setText(self.textInput, "")
        ac.setFocus(self.textInput, 1)
        if len(text) > 0:
            if ac.sendChatMessage(text) == -1:
                self.delayedChat = text

    def reset_chat_input(self):
        ac.setText(self.textInput, self.delayedChat)
        self.delayedChat = None

    def onChatMessage(self, message, author):
        self.messages.append({'message': message, 'author': author})
        # Save some memory?
        if self.messages.__len__() > self.historySize * 2:
            self.messages = self.messages[-self.historySize:]

        self.update_messages()

    def update_messages(self):
        messages = self.messages[-self.historySize:]
        for i in range(self.historySize - 1, -1, -1):
            if i < len(messages):
                ac.setText(self.labels[i]['author'], messages[i]['author'] + ":")
                ac.setText(self.labels[i]['message'], messages[i]['message'])
            else:
                ac.setText(self.labels[i]['author'], '')
                ac.setText(self.labels[i]['message'], '')

    def change_size(self, by):
        self.historySize = max(1, min(self.historySize + by, 50))

# Init the plugin
def acMain(ac_version):
    global chat
    chat = InRaceChat()
    return "InRaceChat"

def acUpdate(deltaT):
    global chat
    if chat.historySize != len(chat.labels):
        chat.initGui()

    if chat.delayedChat != None:
        chat.reset_chat_input()

# Binding the events into class methods directly doesn't work,
# so use a bunch of shims to call the instance directly :(
def globalValidateInput(string):
    global chat
    chat.onValidateInput(string)

def globalChat(message, author):
    global chat
    chat.onChatMessage(message, author)

def globalShrinkButtonClicked(a, b):
    global chat
    chat.change_size(-1)

def globalExpandButtonClicked(a, b):
    global chat
    chat.change_size(1)