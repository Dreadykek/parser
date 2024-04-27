import json
import math
import numpy as np


def get_xy(angel: float, rad: float | str, intensity: float):
    if rad == "inf" or intensity < 40:
        return False
    return [rad*math.cos(angel), rad*math.sin(angel), 1]


if __name__ == '__main__':
    with open('dd.json') as json_file:
        data = json.load(json_file)

        print(data)

    coordinates = []

    for i, angle in enumerate(np.arange(-3.1415927410125732, 3.1415927410125732, 0.005482709966599941)):
        print(angle, i)
        result = get_xy(angle, data['ranges'][i], data['intensities'][i])
        if result:
            coordinates.append(result)

    print(str(coordinates).replace('[', '{').replace(']', '}'))

