import base64
from io import BytesIO
from PIL import Image, ImageFile
import potrace

ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_bounding_box(path):
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for curve in path:
        points = [curve.start_point]
        for segment in curve.segments:
            if segment.is_corner:
                points.append(segment.c)
                points.append(segment.end_point)
            else:
                points.append(segment.c1)
                points.append(segment.c2)
                points.append(segment.end_point)

        for point in points:
            if point.x < min_x:
                min_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y

    return min_x, min_y, max_x, max_y


def convert_base64_to_svg(base64_str):
    img_bytes = base64.b64decode(base64_str)
    img = Image.open(BytesIO(img_bytes)).convert("L")

    img = img.point(lambda x: 0 if x < 128 else 255, "1")

    bitmap = potrace.Bitmap(img, blacklevel=0.5)
    path = bitmap.trace()

    min_x, min_y, max_x, max_y = get_bounding_box(path)
    width = max_x - min_x
    height = max_y - min_y

    svg_content = [
        f'<svg width="{width}mm" height="{height}mm" '
        f'viewBox="{min_x} {min_y} {width} {height}" '
        'xmlns="http://www.w3.org/2000/svg">',
        '<path fill="black" fill-rule="evenodd" d="',
    ]

    for curve in path:
        path_data = [f"M{curve.start_point.x} {curve.start_point.y}"]

        for segment in curve.segments:
            if segment.is_corner:
                path_data.append(f"L{segment.c.x} {segment.c.y}")
                path_data.append(f"L{segment.end_point.x} {segment.end_point.y}")
            else:
                path_data.append(
                    f"C{segment.c1.x} {segment.c1.y} "
                    f"{segment.c2.x} {segment.c2.y} "
                    f"{segment.end_point.x} {segment.end_point.y}"
                )
        path_data.append("Z")
        svg_content.append(" ".join(path_data))

    svg_content.append('"/>')
    svg_content.append("</svg>")

    return "".join(svg_content)
