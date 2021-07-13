import pandas as pd
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt
from utilities import separateLanding

amount = 982

counter = 0

for n in range(amount):
    try:
        x = loadmat(dir + f"/Flight{n+1}.mat")
        cleanedAlt = separateLanding(x)
        th = pd.DataFrame(
            cleanedAlt,
            columns=[
                "altitude",
                "groundspeed",
                "pitch",
                "roll",
                "heading",
                "windSpeed",
                "windDirection",
            ],
        )
        if (np.max(th["roll"]) - np.min(th["roll"])) < 8:
            th.to_csv(
                f"/Landings/Train/Flight{counter+1}.csv", index=False, header=True
            )
            counter += 1
    except:
        pass
