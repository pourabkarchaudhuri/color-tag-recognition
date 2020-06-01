from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

# image = cv2.imread('sample_image2.jpg')
# print("The type of this input is {}".format(type(image)))
# print("Shape: {}".format(image.shape))
# plt.imshow(image)
# print("Step1")

# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# plt.show()

# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# plt.imshow(gray_image, cmap='gray')

# resized_image = cv2.resize(image, (1200, 600))
# plt.imshow(resized_image)

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(image, number_of_colors, show_chart):
    result = list()
    colorElements = dict()
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    
    
    labels = clf.fit_predict(modified_image)
    
    # print(labels)
    counts = Counter(labels)
    # print("========")
    # print( dict(sorted(counts.items())))
    counts = dict(sorted(counts.items()))
    # print("========")
    center_colors = clf.cluster_centers_
    # print("+++++")
    # print(center_colors)
    # print("+++++")
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i]/255 for i in counts.keys()]
    hex_colors = [RGB2HEX(center_colors[i]) for i in counts.keys()]
    rgb_colors = [center_colors[i] for i in counts.keys()]
    # print("HEX " + str(hex_colors))
    # print("RGB-ORDERED " + str(ordered_colors))
    # print("RBG " + str(rgb_colors))
    totalWeightage = sum(counts.values())
    for x in counts.keys():
        # print(str(counts[x]) + str(hex_colors[x]) + str(rgb_colors[x]))
        percentage = round((counts[x]/totalWeightage)*100, 2)
        result.append({
            "hex_code": hex_colors[x],
            "rgb_Value": str(rgb_colors[x]),
            "percentage": percentage
        })

    # if (show_chart):
    #     plt.figure(figsize = (10, 10))
    #     print(counts.values())
    #     wedges, texts = plt.pie(counts.values(), colors=ordered_colors, labels = hex_colors)
    #     plt.legend(wedges, hex_colors, title="Color Pallate", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    #     plt.show()
    
    # return rgb_colors
    return result

# get_colors(get_image('sample_image8.jpg'), 8, True)