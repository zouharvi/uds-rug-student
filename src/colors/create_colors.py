#!/usr/bin/env python3

import math
from PIL import Image, ImageDraw

COLOR_BINS = [
    ['00FF00', 'FFFF00', 'FF0000'],
    ['00FF00', 'FFFFFF', 'FF0000'],
    ['0000FF', 'FFFFFF', 'FF0000'],
    ['0000FF', 'FFFF00', 'FF0000'],
]
BIN_COUNT = 9
IMG_WIDTH = 400
IMG_HEIGHT = 120

data_buckets = []
for bin_i, bins in enumerate(COLOR_BINS):
    bins = [
        (int(x[0:2], 16), int(x[2:4], 16), int(x[4:6], 16))
        for x in bins
    ]
    waypoints_x = [
        IMG_WIDTH * i / (len(bins)-1)
        for i, _ in enumerate(bins)
    ]
    print(waypoints_x)

    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT))
    drawer = ImageDraw.Draw(img)
    colors = []
    for x in range(IMG_WIDTH):
        for i, waypoint_x in enumerate(waypoints_x):
            if x <= waypoint_x:
                break
        i = max(i-1, 0)
        i = min(i, len(bins) - 2)
        color_a, point_a = bins[i], waypoints_x[i]
        color_b, point_b = bins[i + 1], waypoints_x[i + 1]
        weight_a = (point_b - x) / (point_b - point_a)
        color_x = (
            int(color_a[0] * weight_a + color_b[0] * (1 - weight_a)),
            int(color_a[1] * weight_a + color_b[1] * (1 - weight_a)),
            int(color_a[2] * weight_a + color_b[2] * (1 - weight_a)),
        )
        print(weight_a)
        colors.append(color_x)
        drawer.line((x, 0, x, IMG_HEIGHT - 1), fill=color_x, width=1)

    # create interpolated buckets
    data_bucket = []
    step_width = IMG_WIDTH/BIN_COUNT
    for bin_step in range(BIN_COUNT):
        color_x = colors[math.ceil((bin_step+0.5)*step_width)]
        data_bucket.append(color_x)
        drawer.rectangle(
            (math.ceil(bin_step*step_width), IMG_HEIGHT//2, math.ceil((bin_step+1)*step_width), IMG_HEIGHT),
            fill=color_x
        )

    data_buckets.append(data_bucket)
    img.show()
    img.save(f"palette_{bin_i}.png")

with open("palettes.out", "w") as f:
    f.write(str(data_buckets))