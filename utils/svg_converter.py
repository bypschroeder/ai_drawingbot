import cv2
import numpy as np
import svgwrite


def image_to_svg_outline(
    image_path,
    canny_strong=(100, 200),
    canny_soft=(30, 100),
    bilateral_params=(9, 75, 75),
    kernel_size=(2, 2),
    stroke_width=2,
):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smooth = cv2.bilateralFilter(gray, *bilateral_params)

    edges_strong = cv2.Canny(smooth, *canny_strong)
    edges_soft = cv2.Canny(smooth, *canny_soft)
    combined_edges = cv2.bitwise_or(edges_strong, edges_soft)

    kernel = np.ones(kernel_size, np.uint8)
    combined_edges = cv2.dilate(combined_edges, kernel, iterations=1)
    combined_edges = cv2.erode(combined_edges, kernel, iterations=1)

    contours, _ = cv2.findContours(
        combined_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    height, width = combined_edges.shape
    dwg = svgwrite.Drawing(size=(width, height))
    for contour in contours:
        if len(contour) < 2:
            continue
        path_data = "M " + " L ".join(f"{pt[0][0]},{pt[0][1]}" for pt in contour) + " Z"
        dwg.add(
            dwg.path(
                d=path_data, fill="none", stroke="black", stroke_width=stroke_width
            )
        )

    return dwg.tostring()


if __name__ == "__main__":
    result = image_to_svg_outline("output_image.png")
    with open("output_image.svg", "w") as f:
        f.write(result)
    print("SVG file saved as output_image.svg")
