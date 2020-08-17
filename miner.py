from tag_mining import mine_tag, get_counts, analyze
from datetime import datetime
import time
import pandas as pd
import numpy as np

class Miner:
    def __init__(self, tag, custom, intervals=60, sets=3):
        self.tag = tag
        self.custom = custom
        self.intervals = intervals
        self.sets = sets
        self.activity_log("Miner Activated",3)
        mine_tag(self.tag, self.custom)

    def activity_log(self, text: str, datetype: int):
        now = datetime.now()
        if datetype == 1:
            time = now.strftime("%d/%m/%Y")
        elif datetype == 2:
            time = now.strftime("%H:%M:%S")
        else:
            time = now.strftime("%d/%m/%Y, %H:%M:%S")
        with open('activity.txt', 'a') as f:
            f.write(f"{time} --------> {text}\n")

    def start_miner(self):
        for attempt in range(self.sets):
            get_counts(f"{self.tag}.csv")
            time.sleep(60*self.intervals)
            self.activity_log(f"{attempt+1}/{self.sets} sets completed",2)
        self.activity_log("Mining Completed!", 3)
        df = pd.read_csv(f"{self.tag}.csv", index_col=0)
        df.set_index('hashtags', inplace=True)
        df = df.transpose()
        df.to_csv(f"{self.tag}_analysis.csv", index=False)
        filename = f"{self.tag}_analysis.csv"
        return filename
    
    def start_analyzer(self, filename):
        analyze(filename)


