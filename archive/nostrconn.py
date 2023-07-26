## DEPRECATED

from nostr.key import PrivateKey
from nostr.relay_manager import RelayManager
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.filter import Filter, Filters
from nostr.key import PrivateKey

import json
import ssl
import time

def generate_keys():
    private_key = PrivateKey()
    public_key = private_key.public_key
    print(f"Private key: {private_key.bech32()}")
    print(f"Public key: {public_key.bech32()}")
    return {"private_key": private_key.bech32(), "public_key": public_key.bech32()}


def add_relays(relay_list, relay_manager):
    for relay in relay_list:
        relay_manager.add_relay(relay)
    time.sleep(1.25) # allow the connections to open
    return relay_manager  


# TODO
# def publish_event(relay_manager, event):
  
# def receive_events():
