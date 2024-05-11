from RPLCD import *
from time import sleep, mktime
import datetime
from RPLCD.i2c import CharLCD

from btcexplorer import fetch_from_api
from chars import custom_chars, big_chars, big_prefix

lcd = CharLCD("PCF8574", 0x27, auto_linebreaks=False)
lcd.backlight_enabled = True

PAUSE_LEN = 3  # seconds

lcd.create_char(0, custom_chars[0])
lcd.create_char(1, custom_chars[1])
lcd.create_char(2, custom_chars[2])
lcd.create_char(3, custom_chars[3])
lcd.create_char(4, custom_chars[4])

gbp = "\x04"
blk_top = "\x03"
blk_btm = "\x02"
blk_full = "\x01"
blk_empty = "\x00"


def minutes_since(ts):
    now = datetime.datetime.now()
    now_ts = mktime(now.timetuple())
    return int((now_ts - ts) / 60)


def days_till(date):
    now = datetime.datetime.now()
    d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    delta = d - now
    return delta.days

def center_string(s, row):
    if len(s) >= 20:
        lcd.cursor_pos = (row, 0)
        lcd.write_string(s[:19])
    else:
        x = round(10 - len(s)/2)
        lcd.cursor_pos = (row, x)
        lcd.write_string(s)

def map_big_char(n, pos):
    nmap = big_chars[str(n)]
    row_n = 0
    out = ['','','','']
    for row in nmap:
        char_n = pos
        out[row_n] = ''
        for blk in row:
            if blk == 0:
                out[row_n] += blk_empty
            if blk == 1:
                out[row_n] += blk_full
            if blk == 2:
                out[row_n] += blk_btm
            if blk == 3:
                out[row_n] += blk_top
        row_n += 1
    return out



def write_big_char(n, pos, offset):
    nmap = big_chars[str(n)]
    row_n = 0
    for row in nmap:
        char_n = pos + offset
        for blk in row:
            char_n += 1
            if char_n < 20 and char_n >= 0:
                lcd.cursor_pos = (row_n, char_n)
                if blk == 0:
                    lcd.write_string(blk_empty)
                if blk == 1:
                    lcd.write_string(blk_full)
                if blk == 2:
                    lcd.write_string(blk_btm)
                if blk == 3:
                    lcd.write_string(blk_top)
                if blk == 4:
                    lcd.write_string("\x04")
        row_n += 1


def map_prefix(prefix):
    pmap = big_prefix[prefix]
    row_n = 0
    out = ['','','','']
    for row in pmap:
        char_n = 0
        out[row_n] = ''
        for blk in row:
            lcd.cursor_pos = (row_n, char_n)
            if blk == 0:
                out[row_n] += blk_empty
            else:
                out[row_n] += blk
            char_n += 1
        row_n += 1
    return out

def write_prefix(prefix, offset):
    pmap = big_prefix[prefix]
    row_n = 0
    for row in pmap:
        char_n = offset
        for blk in row:
            if char_n < 20 and char_n >= 0:
                lcd.cursor_pos = (row_n, char_n)
                if blk == 0:
                    lcd.write_string("\x00")
                else:
                    lcd.write_string(blk)
            char_n += 1
        row_n += 1


def calc_bigtext_len(txt):
    length = 0
    for char in txt:
        length += len(big_chars[char][0]) + 1

    return length


def write_big2(txt, prefix=None):
    lcd.clear()

    pre_len = 0
    if prefix:
        pre_len = len(big_prefix[prefix][0])

    total_len = pre_len + calc_bigtext_len(txt)

    lines = [
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ]
    

    if prefix:
        p = map_prefix(prefix)
        for row in range(4):
            lines[row] += p[row] + ' '

    i = pre_len + 1

    for char in txt:
        p = map_big_char(char, i)
        for row in range(4):
            lines[row] += p[row] + ' '
        i += len(big_chars[char][0]) + 1

    if prefix:
        p = map_prefix(prefix)
        for row in range(4):
            lines[row] += p[row] + ' '

    #print(lines)

    offset = 10

    while offset < total_len + 20:

        segment = ''
        
        
        for row in range(4):
            #lcd.cursor_pos = (row, 0)
            # print(lines[row][offset:20])
            segment += lines[row][offset:offset+20] + '\r\n'
            #lcd.write_string(lines[row][offset:offset+20])

        lcd.cursor_pos = (0, 0)
        lcd.write_string(segment)

        offset += 6
        sleep(0.3)
        lcd.clear()
        # lcd.cursor_pos = (0, 0)
        # lcd.write_string('   ')
        # lcd.cursor_pos = (1, 0)
        # lcd.write_string('   ')
        # lcd.cursor_pos = (2, 0)
        # lcd.write_string('   ')
        # lcd.cursor_pos = (3, 0)
        # lcd.write_string('   ')
        # lcd.shift_display(-3)

def write_big(txt, prefix=None):
    write_big2(txt, prefix=prefix)
    lcd.clear()
    
    # offset = 20

    # pre_len = 0
    # if prefix:
    #     pre_len = len(big_prefix[prefix][0])

    # total_len = pre_len + calc_bigtext_len(txt)


    # while offset > -total_len:

    #     if prefix:
    #         write_prefix(prefix, offset)

    #     i = pre_len + 1

    #     for char in txt:
    #         write_big_char(char, i, offset)
    #         i += len(big_chars[char][0]) + 1

    #     if(offset == 0):
    #         sleep(1)
    #     offset -= 2
    #     sleep(0.1)
    #     lcd.clear()



class Section:

    def __init__(self, endpoint):
        self.loading_screen()
        self.data = fetch_from_api(endpoint=endpoint)
        lcd.clear()

        if not self.has_error():
            self.before_render()
            self.screen1()
            sleep(PAUSE_LEN)
            # for x in range(10):
            #     lcd.shift_display(-2)
            #     sleep(0.1)
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
        sleep(PAUSE_LEN)


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
        sleep(PAUSE_LEN)
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


def animate_title(title):
    s = ''
    for char in title:
        s += char
        center_string(s, 0)
        sleep(0.02)

# write_big2('abcdefghijklmnopqrstuvwxyz')
# sleep(99)
while 1:

    lcd.clear()

    McapSection()
    HalvingSection()
    XRatesSection()
    SatRatesSection()
    BlockheightSection()
    SupplySection()

