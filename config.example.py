
LCD_ADDRESS = 0x27

# URL of a bitcoin explorer instance. No trailing slash.
EXPLORER_API_URL = 'https://bitcoinexplorer.org'

# URL of a mempool instance. No trailing slash.
# MEMPOOL_API_URL = 'https://mempool.space'

# Enable/disable back light
BACKLIGHT = True 

# Display sats to usd as moscow time
MOSCOWTIME = True

""" 
PAUSE_LEN = int #seconds 
PAUSE2_LEN = int #seconds  

bitticka loops through a number of programs (exchange rates, next halving, ...) 
each of which has 2 views: a details view with small text and a banner view with 
large scrolling text. Each program shows view1, then view2, and finally view1 
again. A pause is inserted after each display of view 1.

- display view 1
- pause PAUSE_LEN
- display view 2
- display view 1
- pause PAUSE2_LEN
- clear display
- pause PAUSE3_LEN

"""
PAUSE_LEN = 2 
PAUSE2_LEN = 1 
PAUSE3_LEN = 1 

"""
The following 2 settings modify the scrolling effect. It's recommended to only make small adjustments at a
time to these settings.

SCROLL_JUMP = int # no. of pixels to jump each cycle
SCROLL_FREQ = float # time in seconds of each cycle
"""
SCROLL_JUMP = 6
SCROLL_FREQ = 0.3

