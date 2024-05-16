
LCD_ADDRESS = 0x27

# URL of a bitcoin explorer instance. No trailing slash.
EXPLORER_API_URL = 'https://bitcoinexplorer.org'

# URL of a mempool instance. No trailing slash.
# MEMPOOL_API_URL = 'https://mempool.space'

# Bitcoin Core details if required
# BITCOIN_RPC_AUTH = {
#     'user': "",
#     'password': "",
#     'url': "http://192.168.1.99:8332"  
# }

# Enable/disable back light
BACKLIGHT = True 

# Display sats to usd as moscow time
MOSCOWTIME = True

""" 
PAUSE_LEN = int #seconds 

bitticka loops through a number of programs (exchange rates, next halving, ...) 
each of which has 2 views: a details view with small text and a banner view with 
large scrolling text. Each program displays view 1, pauses (holds the view), 
then displays view 2.

eg.
- start program 1 (eg. fetch exchange rates from API)
    - display loading view
    - display info view 1 (details)
    - pause PAUSE_LEN
    - display info view 2 (large text banner)
    - clear the screen
- start program 2
    - ...
    - ...

""" 
PAUSE_LEN = 3


"""
The following 2 settings modify the scrolling effect. It's recommended to only make small adjustments at a
time to these settings.

SCROLL_JUMP = int # no. of pixels to jump each cycle
SCROLL_FREQ = float # time in seconds of each cycle
"""
SCROLL_JUMP = 6
SCROLL_FREQ = 0.3

