from time import sleep
from btccore import handle_rpc_call
from strings import animate_title, center_string, write_big
from views.section import Section
from lcd import lcd
import asyncio
import config

class BTCCoreSection(Section):

    def __init__(self, call, *args):
        super().__init__()
        self.loop = asyncio.get_event_loop()

        if isinstance(call, list):
            self.fetch_data_multi(call)
        else:
            self.fetch_data(call, *args)

    def fetch_data_multi(self, items):
        return self.loop.run_until_complete(self.rpc_multi(items))


    def fetch_data(self, call, *args):
        return self.loop.run_until_complete(self.rpc(call, *args))
    
    async def rpc(self, call, *args):
        data = await handle_rpc_call(call, *args)
        self.run(data)

    async def rpc_multi(self, items):
        data = {}
        for item in items:
            data[item[0]] = await handle_rpc_call(item[1], *item[2])
        self.run(data)

class BlockchainInfoSection(BTCCoreSection):

    def __init__(self):
        super().__init__("getblockchaininfo")

    def loading_screen(self):
        animate_title("BLOCKCHAIN INFO:")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("BLOCKCHAIN INFO:", 0)
        center_string(str(self.data), 1)

    def screen2(self):
        write_big("test")


class SmartFeesSection(BTCCoreSection):

    def __init__(self):
        super().__init__(
            [
                ("asap","estimatesmartfee", [1]), 
                ("hour","estimatesmartfee", [6]), 
                ("day","estimatesmartfee", [144])
            ]
        )

    def loading_screen(self):
        animate_title("FEE ESTIMATE:")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("FEE ESTIMATES:", 0)
        center_string("ASAP: {}sats/vB".format(int(self.data['asap']['feerate']*100000)), 1)
        center_string("hour: {}sats/vB".format(int(self.data['hour']['feerate']*100000)), 2)
        center_string("day:  {}sats/vB".format(int(self.data['day']['feerate']*100000)), 3)
        print(self.data)

    def screen2(self):
        write_big("{}sats/vB".format(int(self.data['asap']['feerate']*100000)), "smartfee")

