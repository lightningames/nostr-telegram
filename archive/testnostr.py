## DEPRECATED DO NOT USE

import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind

from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey

# To try this channel visit
# https://www.nostrchat.io/channel/09f6099a502bd0204949e3b2e48bd30ae2f1712e5d15231ed7f6f8daae4c5b97

channel_id = "09f6099a502bd0204949e3b2e48bd30ae2f1712e5d15231ed7f6f8daae4c5b97"

'''
Example message info:

content:  chat relay testing content
tags:  [['e', '09f6099a502bd0204949e3b2e48bd30ae2f1712e5d15231ed7f6f8daae4c5b97', 'wss://relay.damus.io/', 'root']]
public_key: 3878d95db7b854c3a0d3b2d6b7bf9bf28b36162be64326f5521ba71cf3b45a69
created_at: 1690097464

Channel ID is in the 'e' tag, so we only listen for this channel on the specified relay

'''

chatrelay = "wss://relay2.nostrchat.io"
damusrelay = "wss://relay.damus.io"
satsrelay = "wss://sats.lnaddy.com/nostrrelay/satsrelay"

currentrelay = chatrelay
#nostr_authors = ["npub18pudjhdhhp2v8gxnkttt00um729nv93tuepjda2jrwn3eua5tf5s80a699"]

# Modified Event kinds in python-nostr fork, on lightningames repo only
# the parent repo is not up to date with all Nostr Kinds and docs are out of date as well.

# Nostr Kinds supported on lightningames fork:
    # SET_METADATA = 0
    # TEXT_NOTE = 1
    # RECOMMEND_RELAY = 2
    # CONTACTS = 3
    # ENCRYPTED_DIRECT_MESSAGE = 4
    # DELETE = 5
    # CHANNEL_CREATE = 40
    # CHANNEL_METADATA = 41
    # CHANNEL_MESSAGE = 42
    # HIDE_MESSAGE = 43
    # MUTE_USER = 44


filters = Filters([  # enter filter condition
    Filter(
        #authors=nostr_authors,
        since=int(time.time()),
        kinds=[EventKind.TEXT_NOTE,
               EventKind.CHANNEL_METADATA,
               EventKind.CHANNEL_MESSAGE, 
               EventKind.CHANNEL_CREATE], 
        event_refs=[channel_id] # filter by channel id 
    )
])
subscription_id = 'poiuoupuopiou87987987'  # any string as per NIP-01 subscription

relay_manager = RelayManager()
relay_manager.add_relay(currentrelay)
relay_manager.add_subscription_on_relay(currentrelay, subscription_id, filters)
time.sleep(1.25) # allow the connections to open
print("-- end initialize relay manager --")

request = [ClientMessageType.REQUEST, subscription_id]
request.extend(filters.to_json_array())
message = json.dumps(request)
print("message", message)

private_key = PrivateKey()
event = Event(content="Hello Nostr")
private_key.sign_event(event)
relay_manager.publish_event(event)
time.sleep(1) # allow the messages to send


print("--- End setting up relay manager ---")

# TODO: refactor this to work with aiohttp
while 1:
  while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    print("content: ", event_msg.event.content)
    print("tags: ", str(event_msg.event.tags))
    print("public_key:", event_msg.event.public_key)
    print("created_at:", event_msg.event.created_at)
    print("------")

  
relay_manager.close_all_relay_connections()

