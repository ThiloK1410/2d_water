import numpy as np
from numpy import array
from opensimplex import OpenSimplex
import random


def get_polar_noise_2d(layer_count, layer_dimensions, point_distance, seed=None, detail=10):
    if seed is None:
        seed = random.choice(range(10000))
    layer_dimensions = array(layer_dimensions)
    noise = OpenSimplex(seed)
    points = get_circle_points(point_distance, layer_count, (0.5, 0.5))

    noise_values = np.zeros((layer_count, layer_dimensions[1], layer_dimensions[0])).astype(float)

    for i, circle_point in enumerate(points):
        x_coords = np.arange(layer_dimensions[0]) / (layer_dimensions[0] / detail)
        y_coords = np.arange(layer_dimensions[1]) / (layer_dimensions[1] / detail)
        circle_x = array([circle_point[0]])
        circle_y = array([circle_point[1]])

        layer = noise.noise4array(x_coords, y_coords, circle_x, circle_y)\
            .reshape((1, layer_dimensions[0], layer_dimensions[1]))
        print(f"noise layer {i+1} / {layer_count} loaded")
        noise_values[i] = layer

    return noise_values


def get_circle_points(point_distance, point_count, pos):
    points = []
    radians = np.pi * 2
    step_size = radians / point_count
    # no clue why the (10/9) is needed but only with it all points have desired distance
    radius = point_distance * (10/9) / step_size
    angles = [i * step_size for i in range(point_count)]
    for angle in angles:
        y = np.sin(angle) * radius
        x = np.cos(angle) * radius
        point = array([x + pos[0], y + pos[1]])
        points.append(point)

    return points


if __name__ == "__main__":
    # print(OpenSimplex(1).noise4array(np.arange(5), np.arange(5), np.arange(5), np.arange(5)))
    noise = get_polar_noise_2d(4, (5, 5), 0.01).shape



