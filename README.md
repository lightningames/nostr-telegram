# nostr-telegram
Nostr public chat to Telegram Bridge

We'll build a telegram bot in python
that can fetch and relay messages between a public Nostr chatroom and a Telegram chatroom. 

## installation and run

how to install

```
poetry install 
```

To run your bot
```
poetry run python tgbot.py
```

## Guidance

For Protocol background please visit the nostr protocol NIPS, 
namely:

- [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md)
- [NIP-28](https://github.com/nostr-protocol/nips/blob/master/28.md)


Lets try using the Aionostr library: 
https://github.com/davestgermain/aionostr


## TODO LIST: 

- trim down requirements.txt (partly done)
- remove unused artifacts from bot template (partly done)
- use poetry for project setup (done)
- testnostr.py, get events from a nostr chat relay (done)

- write class for handling all nostr client activity
- write unit tests for nostr connections class

- Basic Case to read events from nostr chat relay, post to telegram room
- Basic Case to read from telegram chatroom, post to nostr chat. 

- Refactor Above Base Case to allow for any room to read/write tg to nostr relay
- Allow user to register nostrchatroom, telegram chatroom into db
- admin controls for rooms
- Allow reply to messages in telegram from nostr
- Allow reply to messages in nostr from telegram

## Archival Notes

We tested python-nostr, this library is not up to date and neither are the docs. 
We do not recommend using this library. 

- Parent library is [python-nostr](https://github.com/jeffthibault/python-nostr)
- However, we are using the forked version that is modified and updated at [lightingames/python-nostr](https://github.com/lightningames/python-nostr)

