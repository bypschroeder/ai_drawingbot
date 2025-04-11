import cv2
import os
import numpy as np
import svgwrite

image_path = os.path.abspath("./images/02.png")
outline_path = "output/outline.png"
svg_path = "output/vector.svg"

img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

smooth = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

edges_strong = cv2.Canny(smooth, 100, 200)
edges_soft = cv2.Canny(smooth, 30, 100)

combined_edges = cv2.bitwise_or(edges_strong, edges_soft)

kernel = np.ones((2, 2), np.uint8)
combined_edges = cv2.dilate(combined_edges, kernel, iterations=1)
combined_edges = cv2.erode(combined_edges, kernel, iterations=1)

cv2.imwrite(outline_path, combined_edges)

contours, _ = cv2.findContours(combined_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

height, width = combined_edges.shape
dwg = svgwrite.Drawing(svg_path, size=(width, height))

for contour in contours:
    path_data = "M " + " L ".join(f"{pt[0][0]},{pt[0][1]}" for pt in contour) + " Z"
    dwg.add(dwg.path(d=path_data, fill="none", stroke="black", stroke_width=4))

dwg.save()
