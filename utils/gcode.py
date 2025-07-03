import time
import subprocess
import tempfile
import re


# https://github.com/bdring/Grbl_Pen_Servo
def convert_svg_to_gcode(svg_string):
    with tempfile.NamedTemporaryFile(
        suffix=".svg", delete=True
    ) as svg_temp, tempfile.NamedTemporaryFile(
        suffix=".gcode", delete=True
    ) as gcode_temp:
        svg_temp.write(svg_string.encode("utf-8"))
        svg_temp.flush()

        cmd = [
            "vpype",
            "--config",
            "vpype.toml",
            "read",
            svg_temp.name,
            "linemerge",
            "linesort",
            "reloop",
            "linesimplify",
            # "write",
            # "output/optimized.svg",
            "gwrite",
            "--profile",
            "custom_plotter",
            gcode_temp.name,
        ]

        subprocess.run(cmd, check=True)

        gcode_temp.seek(0)
        gcode_string = gcode_temp.read().decode("utf-8")

    return gcode_string


def scale_gcode(gcode_str, max_x, max_y, margin=8):
    x_coords = []
    y_coords = []
    for line in gcode_str.splitlines():
        match_x = re.search(r"X([0-9.]+)", line)
        match_y = re.search(r"Y([0-9.]+)", line)
        if match_x:
            x_coords.append(float(match_x.group(1)))
        if match_y:
            y_coords.append(float(match_y.group(1)))

    if not x_coords or not y_coords:
        return gcode_str

    min_x, max_x_gcode = min(x_coords), max(x_coords)
    min_y, max_y_gcode = min(y_coords), max(y_coords)
    width = max_x_gcode - min_x
    height = max_y_gcode - min_y

    available_width = max_x - 2 * margin
    available_height = max_y - 2 * margin

    scale = (
        min(available_width / width, available_height / height)
        if (width > 0 and height > 0)
        else 1.0
    )

    def transform_coord(x, y):
        new_x = (x - min_x) * scale + margin
        new_y = (y - min_y) * scale + margin
        return new_x, new_y

    scaled_lines = []
    for line in gcode_str.splitlines():
        match_x = re.search(r"X([0-9.]+)", line)
        match_y = re.search(r"Y([0-9.]+)", line)
        if match_x or match_y:
            x = float(match_x.group(1)) if match_x else None
            y = float(match_y.group(1)) if match_y else None
            if x is not None and y is not None:
                new_x, new_y = transform_coord(x, y)
                line = re.sub(r"X[0-9.]+", f"X{new_x:.6f}", line)
                line = re.sub(r"Y[0-9.]+", f"Y{new_y:.6f}", line)
            elif x is not None:
                new_x, _ = transform_coord(x, min_y)
                line = re.sub(r"X[0-9.]+", f"X{new_x:.6f}", line)
            elif y is not None:
                _, new_y = transform_coord(min_x, y)
                line = re.sub(r"Y[0-9.]+", f"Y{new_y:.6f}", line)
        scaled_lines.append(line)

    return "\n".join(scaled_lines)


def stream_gcode(grbl, gcode):
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".gcode") as tmp:
        tmp.write(gcode)
        tmp.flush()
        temp_filename = tmp.name

    grbl.load_file(temp_filename)
    grbl.job_run()
    while not grbl.job_finished:
        time.sleep(0.5)
