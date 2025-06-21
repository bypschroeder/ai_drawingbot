import time
from svg_to_gcode.svg_parser import parse_string
from svg_to_gcode.compiler import Compiler, interfaces


def convert_svg_to_gcode(input_svg):
    gcode_compiler = Compiler(
        interface_class=interfaces.Gcode,
        movement_speed=3000,  # Rapid move speed (mm/min)
        cutting_speed=500,  # Drawing speed (mm/min)
        pass_depth=0,  # No Z-axis movement
    )

    curves = parse_string(input_svg)
    gcode_compiler.append_curves(curves)

    return gcode_compiler.compile(passes=1)


def clean_coordinate_value(value_str):
    return float(value_str.rstrip(";"))


def scale_gcode(input_gcode, max_x, max_y, margin=4):
    lines = input_gcode.splitlines()
    min_x = min_y = float("inf")
    max_current_x = max_current_y = float("-inf")

    for line in lines:
        if "X" in line and "Y" in line:
            parts = line.split()
            x_val = y_val = None
            for part in parts:
                if part.startswith("X"):
                    x_val = clean_coordinate_value(part[1:])
                elif part.startswith("Y"):
                    y_val = clean_coordinate_value(part[1:])
            if x_val is not None and y_val is not None:
                min_x = min(min_x, x_val)
                min_y = min(min_y, y_val)
                max_current_x = max(max_current_x, x_val)
                max_current_y = max(max_current_y, y_val)

    if min_x == float("inf"):
        raise ValueError("No coordinates found in G-code file")

    width = max_current_x - min_x
    height = max_current_y - min_y

    available_width = max_x - 2 * margin
    available_height = max_y - 2 * margin
    scale_x = available_width / width
    scale_y = available_height / height
    scale_factor = min(scale_x, scale_y)

    scaled_lines = []
    for line in lines:
        if "X" in line or "Y" in line:
            parts = line.split()
            new_parts = []
            for part in parts:
                if part.startswith("X"):
                    raw_val = part[1:]
                    scaled_x = (
                        clean_coordinate_value(raw_val) - min_x
                    ) * scale_factor + margin
                    new_parts.append(f"X{scaled_x:.4f}")
                elif part.startswith("Y"):
                    raw_val = part[1:]
                    scaled_y = (
                        clean_coordinate_value(raw_val) - min_y
                    ) * scale_factor + margin
                    new_parts.append(f"Y{scaled_y:.4f}")
                else:
                    new_parts.append(part)
            scaled_lines.append(" ".join(new_parts))
        else:
            scaled_lines.append(line)

    return "\n".join(scaled_lines)


def stream_gcode(grbl, gcode):
    lines = gcode.splitlines()
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line and not cleaned_line.startswith(";"):
            print(f"Sending: {cleaned_line}")
            grbl.send_immediately(cleaned_line)
            time.sleep(0.1)


if __name__ == "__main__":
    with open("./resources/images/output.svg", "r", encoding="utf-8") as f:
        svg_string = f.read()
    result = convert_svg_to_gcode(svg_string)
    with open("./resources/images/output.gcode", "w", encoding="utf-8") as f:
        f.write(result)
