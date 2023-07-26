from telethon import TelegramClient, events
import yaml
import logging
import random
from dbtools import add_doc, find_all_offers, delete_alldocs_by_user, delete_entry, parse_offers
import datetime as dt
from coingecko_ticker import get_btcrates, sats2btcTable, sats_convert
import aiocron

import os
import time
from datetime import datetime
from pyaml_env import parse_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

bot_commands = ["<b>/all</b> \t\t - List Open Offers. \n",
                "<b>/add</b> \t\t - Add an Offer, Ex: /add Buy 0.05 btc, %Coinbase ATM/Cash. \n",
                "<b>/del</b> \t\t - Delete an offer. Ex: /del [offer_number]\n",
                "<b>/rates</b> \t\t - Get latest BTC to Fiat Rates from Coingecko\n",
                "<b>/table</b> \t\t - Sats to BTC conversion table\n",
                "<b>/helpme</b> \t\t - Prints this list. \n\n"]

            
cmds = "".join(bot_commands)
help_msg += "Here are my  commands: \n\n" + cmds
header_msg = '<b>Nostr-Telegram Bridge Bot</b>\n\n'
intro = header_msg + help_msg

path  = "./"
config_file = path + 'config.yml'
config = parse_config(config_file)

############# logfile ############
level = logging.INFO
logger.setLevel(level)
log_path = path + "logfile"
h = logging.handlers.RotatingFileHandler(log_path, encoding='utf-8', maxBytes=5 * 1024 * 1024, backupCount=5)
h.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s:%(message)s"))
h.setLevel(level)
logger.addHandler(h)
###################################

TOKEN = config['bot_token']
logger.info(f'Bot Token: {TOKEN}')

client = TelegramClient(config["session_name"],
                        config["api_id"],
                        config["api_hash"])

allowed_chatrooms = config['chatrooms']
print(f'Allowed Chatrooms {allowed_chatrooms}')

# Default to another parse mode
client.parse_mode = 'html'

admin_list = config['admins']
print(f'Admin List : {admin_list}')


def add_offer(input, username):
    try:
        offer = input.split(' ', 1)[1].strip()
        logger.info(f'Add Offer, username: {username}')
        msg = ''
        if len(offer) > 0:
            post = {
                'username': username,
                'offer': offer,
                'active' : True,
                'initdate': dt.datetime.now()
            }
            result = add_doc(post)
            if result != -1:
                msg = f"Ok I've added your offer message, @{username}"
            elif result == -1:
                msg = f"Error  - Couldn't add, please contact an admin."
        else:
            msg = f"Error - No Content - Please give an offer"
        return msg
    except Exception as e: 
        return 'Invalid content, please try again'
            
def del_offer(input, username):
    try:
        logger.info(f'arguments: {input}')
        id = input.split(" ")[1].strip() # split on whitespace
        count = delete_entry(username, id)
        if count == 1:
            msg = f"Ok I've deleted your offer, @{username}"
            return msg
        else:
            msg = f"Error -  I can't delete this order ID, @{username}. NOTE: You can only delete your own orders, not your friends."
            return msg
    except Exception as e: 
        return 'Invalid OrderID, please try again'



def add_admin(input):
    try:
        username = input.split(" ")[1].strip() # split on whitespace
        if username not in admin_list:
            admin_list.append(username)
            print(admin_list)
            config['admins'] = admin_list
            with open(config_file , 'w') as outfile:
                yaml.dump(config, outfile, default_flow_style=False)
                print(config)
            outfile.close()
            return f"Admin {username} added to config"
        return f'Admin already present in config'
    except Exception as e:
        logger.error(e)
        return "Error with Adding admin" 
    

def del_admin(input):
    try:
        username = input.split(" ")[1].strip() # split on whitespace
        if username in admin_list:
            admin_list.remove(username)
            config['admins'] = admin_list
            print(admin_list)
            with open(config_file, 'w') as outfile:
                yaml.dump(config, outfile, default_flow_style=False)
            return f"Admin {username} removed from config"
        return 'Admin already removed from config'
    except Exception as e:
        logger.error(e)
        return "Error deleting Admin"


# only admins can delete other users orders
# this command will delete all the orders posted by a specific user
def del_user(input, username):
    if username in admin_list:
        user = input.split("/duser")[1].strip()
        count = delete_alldocs_by_user(user)
        msg = ''
        if count:
            msg = f"{count} offers by @{user} deleted\n"
        else:
            msg = f"Couldn't find offers by @{user}\n"
        return msg

def get_all_offers():
    msg = "Here's a current list of Open Offers:\n\n"
    result = find_all_offers()
    offers = parse_offers(result)
    msg = msg + offers
    if len(offers) > 0:
        return msg
    else:
        msg = "<b>Currently, there are No Offers</b>\n"
        return msg


@client.on(events.NewMessage(pattern='(?i)/start', forwards=False, outgoing=False))
async def new_handler(event):
    await event.reply('Hi! Go to /helpme for instructions')


@events.register(events.NewMessage(incoming=True, outgoing=False))
async def handler(event):
    input = str(event.raw_text)
    sender = await event.get_sender()
    username = sender.username
    rawtext = event.raw_text
    chatid = event.chat_id
    logger.info(f"handler: {input}, by @{username} in chatid: {chatid}")
    
    '''
    if chatid != allowed_chatrooms:
        msg = 'Sorry you are not part of the club! Please join the chatroom to use.'
        await event.reply(msg)
        return 1
    '''
    
    if username is None:
        msg = 'Please set a username in telegram in order use the orderbook.'
        await event.reply(msg)
        return 1

    if '/helpme' in rawtext:
        await event.reply(intro)

    if '/rates' in rawtext:
        msg = get_btcrates()
        await event.reply(msg)
    
    if '/table' in rawtext:
        msg = sats2btcTable()
        await event.reply(msg)

    if '/all' in rawtext:
        msg = get_all_offers()
        await event.reply(msg)
 
    if '/add' in rawtext:
        msg = add_offer(rawtext, username)
        await event.reply(msg)
    elif '/del' in rawtext:
        msg = del_offer(rawtext, username)
        await event.reply(msg)

  # hidden admin commands not shown to public. 
    elif '/deluser' in rawtext:
        msg = del_user(rawtext, username)
        await event.reply(msg)
    elif '/addadmin' in rawtext:
        msg = add_admin(rawtext)
        await event.reply(msg)
    elif '/deladmin' in rawtext:
        msg = del_admin(rawtext)
        await event.reply(msg)
    elif '/adminlist' in rawtext:
        await event.reply(str(config['admins']))

    
#### start bot ####

client.start(bot_token=TOKEN)

with client:
    client.add_event_handler(handler)
    logger.info('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
