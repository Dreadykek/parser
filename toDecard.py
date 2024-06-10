import csv
import math
import random

import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


def get_distance(point_1, point_2):
    if not point_1 or not point_2:
        return -1
    distance = np.sqrt(sum(pow(a - b, 2) for a, b in zip(point_1, point_2)))
    return distance


def get_xy(angel: float, rad: float | str, intensity: float):
    if rad == "inf" or float(intensity) < 40:
        return False
    return [float(rad)*math.cos(angel), float(rad)*math.sin(angel)]


def group_objects_by_len(coordinates):
    group_coordinates = [[]]
    index = 0
    for i, item in enumerate(coordinates):
        if i > 0:
            distance = get_distance(coordinates[i-1], coordinates[i])
            if distance > 0:
                if len(group_coordinates[index]) == 0 or group_coordinates[index][-1][1] == coordinates[i-1]:
                    group_coordinates[index].append([coordinates[i-1], coordinates[i], distance])
                    continue
                group_coordinates.append([])
                index += 1
                group_coordinates[index].append([coordinates[i - 1], coordinates[i], distance])


def generate_color_palette(num_colors):
    color_names = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    color_palette = random.choices(color_names, k=num_colors)

    return color_palette

def parser(data):
    coordinates = []

    for i, angle in enumerate(np.arange(-3.1415927410125732, 3.1415927410125732, 0.005482709966599941)):
        result = get_xy(angle, data['ranges'][i], data['intensities'][i])
        if result:
            coordinates.append(result)
    plt.figure(figsize=(6, 6))  # Создаем новый график

    points = np.array(coordinates)
    x_points = []
    y_points = []
    for coordinate in coordinates:
        x_points.append(coordinate[0])
        y_points.append(coordinate[1])
    dbscan = DBSCAN(eps=0.3, min_samples=5)
    clusters = dbscan.fit_predict(points)

    colors_palette = generate_color_palette(max(clusters) + 1)

    for i, x in enumerate(x_points):
        if clusters[i] == -1:
            plt.scatter(x, y_points[i], color='black', s=1, marker='o')  # Отображаем точки на графике
            continue
        plt.scatter(x, y_points[i], color=colors_palette[clusters[i]], s=1, marker='o')  # Отображаем точки на графике

    plt.xlabel('X')  # Подпись оси X
    plt.ylabel('Y')  # Подпись оси Y
    plt.title('Точки на плоскости')  # Заголовок графика

    plt.grid(True)  # Включаем сетку на графике

    plt.show()  # Показываем график
    with open('myfile.txt', 'w') as f:
        f.write('')
    with open('myfile.txt', 'a') as f:
        for coordinate in coordinates:
            f.write(coordinate.__str__().replace('[', '').replace(']', '') + "\n")

if __name__ == '__main__':
    with open('datalidar.csv', 'r') as file:
        r = csv.reader(file)
        data = {}
        for row in r:
            if any(sub in row[0] for sub in ['ranges', 'intensities']):
                temp = ','.join(row).replace('[', "").replace(']', "").split(':')
                if temp[0] == 'ranges':
                    data['ranges'] = temp[1].lstrip().split(', ')
                if temp[0] == 'intensities':
                    data['intensities'] = temp[1].lstrip().split(', ')
                    parser(data)
                    data = {}

