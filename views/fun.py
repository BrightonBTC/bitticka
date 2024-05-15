from time import sleep
from lcd import lcd
from strings import animate_title, center_string, days_till, minutes_since, write_big

def welcome():
    write_big('bitticka')
    animate_title('***** BITTICKA *****')
    sleep(.5)
    center_string('********************', 1)
    sleep(.5)
    center_string('Bitcoin Ticker', 2)
    sleep(.5)
    center_string('by Carlito', 3)
    sleep(2)


def lfg():
    lcd.clear()
    animate_title('LET\'S', 1)
    sleep(.5)
    lcd.clear()
    animate_title('F**#!NG', 2)
    sleep(.5)
    lcd.clear()
    animate_title('>>> GO <<<', 3)
    sleep(.3)
    lcd.clear()
    animate_title('>>> GO <<<', 3)
    sleep(.1)
    center_string('LET\'S', 1)
    center_string('F**#!NG', 2)
    center_string('>>> GO <<<', 3)
    sleep(1)
    for x in range(3):

        lcd.cursor_pos = (2, 6)
        lcd.write_string('#')
        lcd.cursor_pos = (2, 14)
        lcd.write_string('#')
        lcd.cursor_pos = (1, 4)
        lcd.write_string('#')
        lcd.cursor_pos = (1, 16)
        lcd.write_string('#')
        lcd.cursor_pos = (0, 8)
        lcd.write_string('#')
        lcd.cursor_pos = (0, 12)
        lcd.write_string('#')

        sleep(0.01)

        lcd.cursor_pos = (2, 5)
        lcd.write_string('# ')
        lcd.cursor_pos = (2, 14)
        lcd.write_string(' #')
        lcd.cursor_pos = (1, 2)
        lcd.write_string('#  ')
        lcd.cursor_pos = (1, 16)
        lcd.write_string('  #')
        lcd.cursor_pos = (0, 5)
        lcd.write_string('#   ')
        lcd.cursor_pos = (0, 12)
        lcd.write_string('   #')

        sleep(0.01)

        lcd.cursor_pos = (2, 5)
        lcd.write_string('  ')
        lcd.cursor_pos = (2, 14)
        lcd.write_string('  ')
        lcd.cursor_pos = (1, 2)
        lcd.write_string('   ')
        lcd.cursor_pos = (1, 16)
        lcd.write_string('   ')
        lcd.cursor_pos = (0, 5)
        lcd.write_string('    ')
        lcd.cursor_pos = (0, 12)
        lcd.write_string('    ')

        sleep(0.01)


    sleep(1)
    lcd.clear()