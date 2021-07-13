import numpy as np


def separateLanding(data):
    aData = data["BAL1"][0][0][0]
    gData = data["GS"][0][0][0]
    pData = data["PTCH"][0][0][0]
    rData = data["ROLL"][0][0][0]
    hData = data["TH"][0][0][0]
    wData = data["WS"][0][0][0]
    wDData = data["WD"][0][0][0]
    samples = 500
    ctf = 3000 + aData[-1]
    for i in range(len(aData)):
        if aData[-1 - i] > ctf:
            newData = aData[-1 - i - 64 :]
            for z in range(len(newData)):
                if newData[z] < aData[-1]:
                    print("Yay")
                    aArr = aData[-1 - i + z - 64 - samples : -1 - i + z - 64]
                    hArr = hData[-1 - i + z - 64 - samples : -1 - i + z - 64]
                    wDArr = wDData[-1 - i + z - 64 - samples : -1 - i + z - 64]
                    wArr = wData[-1 - i + z - 64 - samples : -1 - i + z - 64]
                    gArr = gData[-1 - i + z - 64 - samples : -1 - i + z - 64]
                    placeholder = []
                    for a in range(samples):
                        temp = aArr[a][0]
                        placeholder.append(float(temp))
                    aArr = placeholder
                    placeholder = []
                    for a in range(samples):
                        temp = hArr[a][0]
                        placeholder.append(temp)
                    hArr = placeholder
                    placeholder = []
                    for a in range(samples):
                        temp = wArr[a][0]
                        placeholder.append(temp)
                    wArr = placeholder
                    placeholder = []
                    for a in range(samples):
                        temp = wDArr[a][0]
                        placeholder.append(temp)
                    wDArr = placeholder
                    placeholder = []
                    for a in range(samples):
                        temp = gArr[a][0]
                        placeholder.append(temp)
                    gArr = placeholder
                    index = len(aData) - 1 - i + z
                    arr = pData[2 * index - 2 * samples : 2 * index]
                    pArr = []
                    for n in range(samples):
                        pArr.append(arr[2 * n - 1])
                    arr = rData[2 * index - 2 * samples : 2 * index]
                    rArr = []
                    for m in range(samples):
                        rArr.append(arr[2 * m - 1])
                    placeholder = []
                    for a in range(samples):
                        temp = rArr[a][0]
                        placeholder.append(temp)
                    rArr = placeholder
                    placeholder = []
                    for a in range(samples):
                        temp = pArr[a][0]
                        placeholder.append(temp)
                    pArr = placeholder
                    returnData = list(zip(aArr, gArr, pArr, rArr, hArr, wArr, wDArr))
                    return returnData


class AltitudeScaler:
    def __init__(self):
        self.groundAlt = 0

    def fit(self, data):
        self.groundAlt = data[len(data) - 1]

    def transform(self, data):
        arr = []
        for i in range(len(data)):
            arr.append((data[i] - self.groundAlt))

        return arr

    def untransform(self, data):
        arr = []
        for i in range(len(arr)):
            arr.append(data[i] + self.groundAlt)
        return arr

    def fit_and_transform(self, data):
        self.fit(data)
        return self.transform(data)


class HeadingScaler:
    def __init__(self):
        self.runwayHeading = 0

    def fix(self, n):
        if (n <= 180.0) and (n >= -180.0):
            return n
        elif n > 180.0:
            return self.fix(n - 360.0)
        elif n < -180.0:
            return self.fix(n + 360.0)

    def fit(self, headingData, windData):
        self.runwayHeading = headingData[len(headingData) - 1]

    def transform(self, headingData, windData):
        arr = []
        for i in range(len(headingData)):
            difference = -(self.runwayHeading - headingData[i])

            difference = self.fix(difference)

            arr.append(difference / 180.0)
        arr2 = []
        for i in range(len(windData)):
            difference = -(self.runwayHeading - windData[i])
            difference = self.fix(difference)
            arr2.append(difference / 180.0)
        return arr, arr2

    def untransform(self, headingData, windData):
        arr = []
        for i in range(len(headingData)):
            difference = headingData[i] * 180.0
            arr.append(difference + self.runwayHeading)
        arr2 = []
        for i in range(len(windData)):
            difference = windData[i] * 180.0
            arr2.append(difference + self.runwayHeading)
        return arr, arr2

    def fit_and_transform(self, headingData, windData):
        self.fit(headingData, windData)
        return self.transform(headingData, windData)


def create_sequences(data, seq_length):
    xs = []
    ys = []

    for i in range(len(data) - seq_length):
        x = data[i : (i + seq_length)]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y[1:2])

    return np.array(xs), np.array(ys)
