from lcd import lcd
import views

views.welcome()

while 1:

    lcd.clear()

    views.McapSection()
    views.HalvingSection()
    views.XRatesSection()
    views.SatRatesSection()
    views.BlockheightSection()
    views.SupplySection()

