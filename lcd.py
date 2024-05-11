from RPLCD.i2c import CharLCD
from chars import custom_chars
import config

lcd = CharLCD("PCF8574", config.LCD_ADDRESS, auto_linebreaks=False)
lcd.backlight_enabled = bool(config.BACKLIGHT)

lcd.create_char(0, custom_chars[0])
lcd.create_char(1, custom_chars[1])
lcd.create_char(2, custom_chars[2])
lcd.create_char(3, custom_chars[3])
lcd.create_char(4, custom_chars[4])