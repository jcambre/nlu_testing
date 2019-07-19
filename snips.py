#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import json
import sys
import struct
from snips_nlu import SnipsNLUEngine

nlu_engine = SnipsNLUEngine.from_path("trained_engine")

def getMessage():
    rawLength = sys.stdin.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.read(messageLength)
    return json.loads(message)

# Encode a message for transmission,
# given its content.
def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent)
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}

# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.write(encodedMessage['length'])
    sys.stdout.write(encodedMessage['content'])
    sys.stdout.flush()

while True:
    receivedMessage = getMessage()
    loaded_engine = SnipsNLUEngine.from_path("trained_engine")
    intent = loaded_engine.parse(receivedMessage)
    sendMessage(encodeMessage(intent))