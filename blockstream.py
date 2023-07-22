import requests
from requests.api import get
import json
from constants import block_explorer

url  = 'https://blockstream.info/api/'
block = 'blocks/tip/height'
mempool = 'mempool'
fee_url = 'fee-estimates'
tx = 'tx/'


# get block height
def get_height():
    response = requests.get(url+block)
    height = response.text
    return height


def get_mempoolfees():
    response = requests.get("https://mempool.space/api/v1/fees/recommended")
    return response.json()

'''    
Get an object where the key is the confirmation target (in number of blocks) 
and the value is the estimated feerate (in sat/vB). The available confirmation
targets are 1-25, 144, 504 and 1008 blocks.
'''
def get_fee(rawtext):
    try:
        response = requests.get(url+fee_url)
        info = response.json()

        #print(rawtext)
        val = rawtext.split(' ', 1)[1]
        if not val.isdigit():
            return 'Please give an integer'
                
        fee_info = 'No value found for integer. Must be 1-25, 144, 504 or 1008 Blocks'
        if 1 <= int(val) <= 25:
            # print(info[val])
            fee_info = str(info[val]) + " sat/vB\n"
        elif int(val) in [144, 504, 1008]:
            fee_info = str(info[val]) + " sat/vB\n"
            
        result = fee_info 
        return result
        
    except Exception as e: 
        # print(f'get fee exception: {e}')
        return "Error in query, " + fee_info
        
'''
Get mempool backlog statistics. Returns an object with:
    count: the number of transactions in the mempool
    vsize: the total size of mempool transactions in virtual bytes
    total_fee: the total fee paid by mempool transactions in satoshis
    fee_histogram: mempool fee-rate distribution histogram
'''
def get_mempool_stats():
    response = requests.get(url+mempool)
    info = response.json()
    status = 'Count: ' + str(info['count']) + "\n"
    status += 'Vsize: ' + str(info['vsize']) + "\n"
    status += 'Total Fee: ' + str(info['total_fee']) + "\n"
    return status

'''
Get transaction status, give tx id as input
'''
def get_transaction_status(rawtext):
    try:
        inbound = rawtext.split(' ', 1)[1].strip()
        id = str(inbound)

        response = requests.get(url+tx+id)
        if response.text == 'Invalid hex string':
            return response.text

        info = response.json()
        content = info['status']
        status = "Confirmed: False \n Check back later! \n"
        
        if content['confirmed'] == True:     
            status = "Confirmed: True \n"
            status += "Block Height: " + str(content['block_height']) + "\n"
            status += "Block Time: " + str(content['block_time']) + "\n"
            status += "Block Hash: " + str(content['block_hash']) + "\n" 
        
        status += "\n\n" + block_explorer + id + " \n"   
        return status
    
    except Exception as e:
        print(f'transaction exception as {e}')
        return 'Invalid hex string, please input a valid string'

    
if __name__ == "__main__":
    
    # real simple 'unit' test
    height = get_height()
    print(height)

    info = get_mempool_stats()
    print(info)

    rawtext = '/fee_estimates 25'
    feeinfo = get_fee(rawtext)
    print(feeinfo)

    rawtext = '/fee_estimates 144'
    feeinfo = get_fee(rawtext)
    print(feeinfo)

    rawtext = '/fee_estimates 100'
    feeinfo = get_fee(rawtext)
    print(feeinfo)

    rawtext = '/fee_estimates asdflkj'
    feeinfo = get_fee(rawtext)
    print(feeinfo)

    print("======== \n")

    # test get transaction status
    prefix = '/get_transaction_status '
    unconfirmed = prefix + 'd8c093b9280d9650302b835d177e383903802854cae2efc19f5d141f33e9601c'
    confirmed = prefix + 'd4271246793cb362cc5e1c08deae8479594a2e613d7ef32ab48589f785f08595'
    fakeid = prefix + '4905sldfkjsdkflsdlfj'
    
    print(confirmed)
    txinfo = get_transaction_status(confirmed)
    print(txinfo)

    print(unconfirmed)
    txinfo = get_transaction_status(unconfirmed)
    print(txinfo)

    print(fakeid)
    txinfo = get_transaction_status(fakeid)
    print(txinfo)