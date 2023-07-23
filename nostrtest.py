import aionostr
import aiohttp
import asyncio
import json
import os

profile = 'nprofile1qqsv0knzz56gtm8mrdjhjtreecl7dl8xa47caafkevfp67svwvhf9hcpz3mhxue69uhkgetnvd5x7mmvd9hxwtn4wvspak3h'
kindinfo = {"kinds": [1], "limit":10}
relaylist = ['wss://relay.damus.io']

pvtkey = os.environ['PVTKEY']
pubkey = 'npub1lrpxldhxjln976q3lqn8w2g46rhgqmsjcn8klm5sdse9g523jq5srvmncm'

async def main():
    response = await aionostr.get_anything(profile, private_key=pvtkey, verbose=True, relays=relaylist)
    if isinstance(response, str):
        print(response)
        return
    elif isinstance(response, asyncio.Queue):
        async def iterator():
            while True:
                event = await response.get()
                yield event
    else:
        async def iterator():
            for event in response:
                yield event
    async for event in iterator():
            print(json.dumps(event.to_json_object(), indent=4))



asyncio.run(main())

