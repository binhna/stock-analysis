# #!/usr/bin/env python

# from bs4 import BeautifulSoup
# import requests

# import asyncio
# import pathlib
# import ssl
# import websockets
# import logging
# import price
# import parser
# logging.basicConfig(level=logging.INFO)


# async def load_price():
#     # url = "wss://price-api.vndirect.com.vn/realtime"
#     # url = "wss://trading.pinetree.vn/socket.io/?EIO=3&transport=websocket&sid=iooMBuzJMPJtyELEbYBL"
#     url = "wss://trading.pinetree.vn/socket.io/?EIO=3&transport=websocket&sid=TGcfLsMTRTdhNQaJnRXd"
#     # url = "wss://trading.pinetree.vn/socket.io/?EIO=3&transport=websocket&sid=zyEaZnQATHnKAZkwlfBO"
#     async with websockets.connect(url, ssl=True) as ws:
#         logging.info(f"Connected")
#         ps = price.Price(ws)
#         await ps.subscribe(parser.BA, ["VND", "PNJ"])
#         await ps.subscribe(parser.SP, ["VND", "PNJ"])
#         await ps.subscribe(parser.DE, ["VN30F1901"])
#         await ps.subscribe(parser.MI, ["10", "11", "12", "13", "02", "03"])
#         while True:
#             msg = await ps.recv()
#             logging.info(f"< {str(msg)}")


# if __name__ == "__main__":
#     logging.info("Start...")
#     asyncio.get_event_loop().run_until_complete(load_price())


# # page = requests.get("https://trading.pinetree.vn/#/home/bang-gia/vn30")

# # soup = BeautifulSoup(page.content, 'html.parser')

# # print(soup.prettify())


#!/usr/bin/env python

# WS client example

import asyncio
import websockets


async def hello():
    uri = "wss://price-api.vndirect.com.vn/realtime"
    async with websockets.connect(uri) as websocket:
        name = "a"
        await websocket.send(name)
        # print(f"> {name}")

        greeting = await websocket.recv()
        # print(f"< {greeting}")
        await websocket.send(name)
        # print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")
        action, data = greeting.split("|", 1)
        if action == "c":
            


asyncio.get_event_loop().run_until_complete(hello())
