import argparse
from utils.init_grbl import init_grbl_streamer
from utils.svg_converter import image_to_svg_outline
from utils.gcode import convert_svg_to_gcode, scale_gcode, stream_gcode

BAUDRATE = 115200
INPUT_IMG = "resources/images/01.png"

parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--input", type=str)
args = parser.parse_args()

# Init GRBL
grbl = init_grbl_streamer(BAUDRATE)

# Set GRBL home
grbl.send_immediately("G92.1")  # 1. Clear any G92 offsets
grbl.send_immediately("G10 P0 L2 X0 Y0")  # 2. Reset work offset to machine zero
grbl.send_immediately("G54")  # 3. Select default coordinate system
grbl.send_immediately("G90")  # 4. Absolute positioning

# Convert input image to gcode
svg = image_to_svg_outline(INPUT_IMG)
gcode = convert_svg_to_gcode(svg)
scaled_gcode = scale_gcode(gcode, max_x=150, max_y=100, margin=12)

# Draw gcode
stream_gcode(grbl, scaled_gcode)

# Send plotter back to home
grbl.send_immediately("G0 X0 Y0")

# Disconnect when done
grbl.disconnect()
