import views.fun as fun
import views.explorer as explorer
import views.mempool as mempool
import views.btccore as btccore

explorer.SatRatesSection()
fun.welcome()

while 1:
    
    fun.lfg()

    mempool.DifficultySection()

    explorer.McapSection()
    explorer.HalvingSection()
    explorer.XRatesSection()
    explorer.SatRatesSection()
    explorer.BlockheightSection()
    explorer.SupplySection()

    btccore.SmartFeesSection()

