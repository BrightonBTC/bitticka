import datetime
from time import mktime, sleep
from lcd import lcd
from chars import big_chars, big_prefix, blk_btm, blk_top, blk_full, blk_empty
import config

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

def map_big_char(n):
    nmap = big_chars[str(n)]
    row_n = 0
    out = ['','','','']
    for row in nmap:
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


def calc_bigtext_len(txt):
    length = 0
    for char in txt:
        length += len(big_chars[char][0]) + 1

    return length


def write_big(txt, prefix=None):

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

    #i = pre_len + 1

    for char in txt:
        p = map_big_char(char)
        for row in range(4):
            lines[row] += p[row] + ' '
        #i += len(big_chars[char][0]) + 1

    if prefix:
        p = map_prefix(prefix)
        for row in range(4):
            lines[row] += p[row] + ' '

    offset = 0

    while offset < total_len + 20:

        segment = ''
        
        for row in range(4):
            segment += lines[row][offset:offset+20] + '\r\n'

        lcd.cursor_pos = (0, 0)
        lcd.write_string(segment)

        offset += config.SCROLL_JUMP
        sleep(config.SCROLL_FREQ)
        lcd.clear()


def animate_title(title, row=0):
    s = ''
    for char in title:
        s += char
        center_string(s, row)
        sleep(0.02)
