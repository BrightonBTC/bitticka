import views.fun as fun
import views.explorer as explorer
import views.mempool as mempool

fun.welcome()

while 1:
    
    fun.lfg()
    explorer.McapSection()
    explorer.HalvingSection()
    explorer.XRatesSection()
    explorer.SatRatesSection()
    explorer.BlockheightSection()
    explorer.SupplySection()
    mempool.DifficultySection()
