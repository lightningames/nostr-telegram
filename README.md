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


Nostr python library, this isn't really up to date, so it needs a pretty hard refactor
There is an aiohttp library but will need to investigate
- [python-nostr](https://github.com/jeffthibault/python-nostr)


## TODO LIST: 

- trim down requirements.txt (partly done)
- remove unused artifacts from bot template (done)
- use poetry for project setup (done)
- testnostr.py, get events from a nostr chat relay (done)

- refactor python-nostr to update it properly for group chat Kinds
- refactor to make python-nostr work with aiohttp
- write class for handling all nostr client activity
- write unit tests for nostr connections class

- Interop Base Case
- Basic Case to read events from nostr chat relay, post to telegram room
- Basic Case to read from telegram chatroom, post to nostr chat. 

- Refactor Above Base Case to allow for any room to read/write tg to nostr relay
- Allow user to register nostrchatroom, telegram chatroom into db
- admin controls for rooms
- Allow reply to messages in telegram from nostr
- Allow reply to messages in nostr from telegram
