from time import sleep
from lcd import lcd
from btcexplorer import fetch_from_explorer
import config
from strings import center_string

class Section:

    def __init__(self):
        pass

    def run(self, data):
        self.loading_screen()
        self.data = data
        lcd.clear()

        if not self.has_error():
            self.before_render()
            self.screen1()
            sleep(config.PAUSE_LEN)
            self.screen2()
            self.screen1()
            sleep(config.PAUSE2_LEN)
            lcd.clear()
            sleep(config.PAUSE3_LEN)
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