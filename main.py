import os
from dotenv import load_dotenv
from utils.init_grbl import init_grbl_streamer
from utils.svg import convert_base64_to_svg
from utils.gcode import convert_svg_to_gcode, scale_gcode, stream_gcode
from utils.generate_image import generate_line_art_image

load_dotenv()

# Generate image
print("Please enter what you would like to be drawn:")
keyword = input()
base64 = generate_line_art_image(keyword)

# Convert generated image to svg
svg = convert_base64_to_svg(base64)
# Save svg if wanted
# with open("output/svg.svg", "w") as f:
#     f.write(svg)

# Convert svg to gcode
gcode = convert_svg_to_gcode(svg)
scaled_gcode = scale_gcode(gcode, max_x=50, max_y=50, margin=8)
# Save gcode if wanted
# with open("output/gcode.gcode", "w") as f:
#     f.write(scaled_gcode)

# Init GRBL
grbl = init_grbl_streamer(os.getenv("BAUDRATE"), "./grbl_settings.txt")

# Draw gcode
stream_gcode(grbl, scaled_gcode)

# Disconnect when done
grbl.disconnect()
