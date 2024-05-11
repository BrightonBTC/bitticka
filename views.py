from btcexplorer import fetch_from_api
from time import sleep
from lcd import lcd
from chars import gbp

import config
from strings import animate_title, center_string, days_till, minutes_since, write_big

def welcome():
    write_big('bitticka', 'welcome')
    animate_title('***** BITTICKA *****')
    sleep(.5)
    center_string('********************', 1)
    sleep(.5)
    center_string('Bitcoin Ticker', 2)
    sleep(.5)
    center_string('by Kailash', 3)
    sleep(2)

class Section:

    def __init__(self, endpoint):
        self.loading_screen()
        self.data = fetch_from_api(endpoint=endpoint)
        lcd.clear()

        if not self.has_error():
            self.before_render()
            self.screen1()
            sleep(config.PAUSE_LEN)
            self.screen2()
            sleep(1)


        else:
            self.error()


    def loading_screen(self):
        lcd.cursor_pos = (1, 5)
        center_string("Fetching...", 1)

    def before_render(self):
        pass

    def screen1(self):
        pass

    def screen2(self):
        pass

    def has_error(self):
        if not self.data or 'error' in self.data:
            return True
        return False

    def error(self):
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Error connecting to API")
        sleep(config.PAUSE_LEN)


class BlockheightSection(Section):

    def __init__(self):
        super().__init__("/api/blocks/tip")

    def before_render(self):
        self.block_details = fetch_from_api(endpoint="/api/block/{}".format(self.data["height"]))

    def loading_screen(self):
        animate_title("LATEST BLOCK:")
        center_string("[fetching...]", 2)

    def screen1(self):
        center_string("LATEST BLOCK:", 0)
        center_string("height: {:,}".format(self.data["height"]), 2)

        if self.block_details and 'error' not in self.block_details:
            block_details = fetch_from_api(endpoint="/api/block/{}".format(self.data["height"]))
            center_string("{} mins ago".format(minutes_since(block_details["time"])), 3)

    def screen2(self):
        write_big("{:,}".format(int(self.data["height"])), "block_height")


class HalvingSection(Section):

    def __init__(self):
        super().__init__("/api/blockchain/next-halving")  

    def before_render(self):
        self.countdown_days = days_till(self.data["nextHalvingEstimatedDate"].split(".")[0])


    def loading_screen(self):
        animate_title("NEXT HALVING:")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("NEXT HALVING:", 0)
        center_string("{:,} days".format(self.countdown_days), 1)
        center_string("{:,} blocks".format(self.data["blocksUntilNextHalving"]), 2)
        center_string("Subsidy: {} ".format(self.data["nextHalvingSubsidy"]), 3)
        sleep(config.PAUSE_LEN)
        lcd.clear()
        animate_title("NEXT HALVING:")
        parts = self.data["timeUntilNextHalving"].split(',')
        for x in range(len(parts)):
            lcd.cursor_pos = (x+1, 7)
            lcd.write_string(parts[x].strip())
            #center_string(parts[x].strip(' \t\n\r'), x+1)


    def screen2(self):
        write_big("{:,}days".format(self.countdown_days), "days_till_halving")


class SupplySection(Section):

    def __init__(self):
        super().__init__("/api/blockchain/coins")  

    
    def loading_screen(self):
        animate_title("SUPPLY:")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("SUPPLY:", 0)
        center_string("{:,.2f} BTC".format(float(self.data["supply"])), 1)
        center_string("mined to date ", 2)
        center_string("[ {:.2f}% ]".format(100 * float(self.data["supply"])/float(21000000)), 3)

    def screen2(self):
        write_big("{:,.2f}".format(float(self.data["supply"])), "current_supply")


class McapSection(Section):

    def __init__(self):
        super().__init__("/api/price/marketcap")  

    def loading_screen(self):
        
        animate_title("MARKET CAP:")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("MARKET CAP:", 0)
        center_string("${:,}".format(int(self.data["usd"])), 2)
        center_string("{}{:,}".format(gbp, int(self.data["gbp"])), 3)

    def screen2(self):
        write_big("${:.2f}Trillion".format(int(self.data["usd"]) / 1000000000000), "marketcap")


class XRatesSection(Section):

    def __init__(self):
        super().__init__("/api/price")  

    def loading_screen(self):
        animate_title("FIAT EXCHANGE RATES")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("FIAT EXCHANGE RATES", 0)
        center_string("USD {:,.2f}".format(float(self.data["usd"])), 1)
        center_string("GBP {:,.2f}".format(float(self.data["gbp"])), 2)
        center_string("EUR {:,.2f}".format(float(self.data["eur"])), 3)
        # lcd.cursor_pos = (3, 0)
        # lcd.write_string("XAU {}".format(self.data["xau"]))
        
    def screen2(self):
        write_big("${:,.2f}".format(float(self.data["usd"])), "usdbtc")
        write_big("£{:,.2f}".format(float(self.data["gbp"])), "gbpbtc")


class SatRatesSection(Section):

    def __init__(self):
        super().__init__("/api/price/sats")  

    def loading_screen(self):
        animate_title("SATS TO FIAT")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("SATS TO FIAT", 0)
        center_string("1 GBP = {:,} sats".format(int(self.data["gbp"])), 2)
        center_string("1 USD = {:,} sats".format(int(self.data["usd"])), 3)

    def screen2(self):
        write_big("{:,}".format(int(self.data["usd"])), "satsusd")
        write_big("{:,}".format(int(self.data["gbp"])), "satsgbp")
