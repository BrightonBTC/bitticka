# *:::-: b:t-t:cka :-:::*
#### *bitcoin ticker/block clock with a raspi + 20x4 alphanumeric lcd*

This simple ticker connects to a [BitcoinExplorer](https://bitcoinexplorer.org) instance and displays some stats about the bitcoin network such as exchange rates, halving countdown, latest block, etc.

![bitticka](img/20240512_124431.gif)
![bitticka](img/20240512_132118.gif) 

_**TODO**_ (at some point if I get around to it): Setup connection to BTC Core node and use RPC data to add a few extra info screens to the LCD.

## Required Components

- **Raspberry pi + raspi OS installed** (I used an old 3b I had kicking around but most pi's should work so long as they have internet capabilities. ie.pi3/4/5,zero w, etc.)
- **20x4 alphanumeric LCD** with **PCF8574 I2C expander** (or you could do it without the expander but instructions for the extra wiring are not included here)
- **4 jumper cables** to go from pi to the display
- A **BitcoinExplorer instance** to connect to (self hosted and connected to your own BTC Core node is recommended)

## Connect the display

Connecting a pi to a PCF8574 expander is simple and there are many tutorials online if the following basic outline is insufficient (eg. [here](https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/) or [here](https://circuitdigest.com/microcontroller-projects/interfacing-lcd-with-raspberry-pi-4-to-create-custom-character-and-scrolling-text) )

There are only 4 pins on the LCD expander, each one needs to be connected to the pi in the following manor:

- SDA -> SDA
- SCL -> SCL
- GND -> GND
- VCC -> 5v

![pi to lcd wiring](img/20240512_115027.jpg)

## Enable I2C
1) open raspi-config:
```
sudo raspi-config
```
2) Select `Interface Options` from the list
3) Make sure `I2c` is enabled


## Install i2c-tools and get LCD address

1) install tools:
```
sudo apt-get install i2c-tools
```
2) reboot pi
3) find the address:
```
sudo apt-get install i2c-tools
```
You should now see a table similar to below in which one cell contains a number. **Note this number down.**

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --  
```

## Install other dependencies

```
sudo pip install RPLCD
```
```
sudo apt install python-smbus
```

## Clone this repo
```
git clone https://github.com/BrightonBTC/bitticka.git
cd bitticka
```

## Configure

Copy `config.example.py` to `config.py` and open it for editing
```
sudo cp config.example.py config.py
sudo nano config.py
```
Change the LCD_ADDRESS to the one you noted down earlier, and change API_URL to your self hosted or preferred instance.
```
LCD_ADDRESS = 0x27

# URL of a bitcoin explorer instance. No trailing slash.
API_URL = 'https://bitcoinexplorer.org'
```

## Test run
Whilst still in the bitticka dir run the script to make sure it's working.
```
python3 ./btcticker.py
```
You should now see the welcome screen appear

![bitticka welcome screen](img/20240512_123642.gif)

## Run as a service

If you want to run it as a service so that it will always run after a reboot etc., then:

```
sudo nano /etc/systemd/system/btcticker.service
```

Enter the following making sure to make the appropriate change to the `.../bitticka/btcticker.py` path

```
[Unit]
Description=BTC Ticker/BlockClock
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/[user]/bitticka/btcticker.py
[Install]
WantedBy=multi-user.target
```

And run the service:

```
sudo systemctl daemon-reload
sudo systemctl enable btcticker.service
sudo systemctl restart btcticker.service
```

## Further Configuration

See the `config.py` file for a few other params that can be adjusted.

The various screens that are displayed on the LCD are grouped in to sections, you can adjust the order and selection of sections be changing the order in `btcticker.py` 

```python
# btcticker.py
import views

views.welcome()

while 1:
    views.lfg()
    views.McapSection()
    views.HalvingSection()
    views.XRatesSection()
    views.SatRatesSection()
    views.BlockheightSection()
    views.SupplySection()
```

any views before the while loop play once when bitticka first loads. Anything inside the while loop will loop continuously.

If you're comfortable writing a bit of Python code it would be fairly trivial to add extra views. You can refer to `views.py`. If you use the `write_big()` function in your view just be aware that it only handles a limited set of chars (0-9 and lowercase alphanumeric are safe) and any additional ones would need to be mapped and added to the `big_chars` array in `chars.py`.

If you create anything cool that other might want to use then consider putting in a pull request.

![LFG!](img/20240512_145837.gif)