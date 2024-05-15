from strings import animate_title, center_string, write_big
from views.section import Section
from mempool import fetch_from_mempool
from lcd import lcd

class MempoolSection(Section):

    def __init__(self, endpoint):
        super().__init__()
        data = fetch_from_mempool(endpoint=endpoint)
        self.run(data)



class DifficultySection(MempoolSection):

    def __init__(self):
        super().__init__("/api/v1/difficulty-adjustment")

    def loading_screen(self):
        animate_title("DIFFICULTY ADJUSTMENT:")
        center_string("[fetching...]", 2)

    def screen1(self):
        lcd.clear()
        center_string("progress: {:,.1f}%".format(self.data['progressPercent']), 0)
        center_string("change: {:,.2f}%".format(self.data['difficultyChange']), 1)
        center_string("{} blocks to go".format(self.data['remainingBlocks']), 2)
        center_string("average: {:,.1f} mins".format(self.data['timeAvg']/60000), 3)

    def screen2(self):
        write_big("{:,.1f} mins".format(self.data['timeAvg']/60000), "avblocktime")