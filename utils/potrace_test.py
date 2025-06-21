from PIL import Image
import subprocess
import os

img = Image.open(os.path.abspath("output_image.png")).convert("L")
bw = img.point(lambda x: 0 if x < 128 else 255, "1")
bw.save("./resources/images/input.pbm")

subprocess.run(
    [
        "E:\Projects\Potrace\potrace.exe",
        "./resources/images/input.pbm",
        "-s",
        "-o",
        "output.svg",
        "--color",
        "#ff0000",
    ],
    check=True,
)

print("SVG outline saved as output.svg")
