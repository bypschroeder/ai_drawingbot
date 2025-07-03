# AI-Drawingbot

The AI-Drawingbot is an interactive system that transforms user prompts into physical artworks. Users describe what they want to be drawn, and the system leverages advanced AI models to generate a corresponding image. This image is then processed—optimized for vector drawing and converted into line art suitable for plotting. Finally, a custom-built XY-plotter, constructed with 3D-printed parts and Arduino-based controls, physically draws the generated artwork onto paper.

## Installation

Follow these steps to install and set up the project:

1. **Create a Python Virtual Environment**

```
python -m venv venv
```

2. **Activate the virtual environment**

On Linux/MacOS:

```
source venv/bin/activate
```

On Windows:

```
venv/Scripts/activate
```

3. **Install Python Dependencies**

```
pip install -r requirements.txt
```

4. **Flash the Arduino with the customized Firmware**

- Copy the `grbl` folder from this repository to your Arduino libraries directory (typically located at `~/Arduino/libraries` on Linux/macOS or `Documents\Arduino\libraries\ on Window`)
- Open the Arduino IDE
- In the IDE, open the `grblUpload` sketch from `File > Examples > grbl`
- Connect the Arduino to your computer
- Select the correct board type and port in the Arduino IDE
- Click the Upload button to flash the firmware onto the Arduino

## Plotter

The plotter itself was built following this [tutorial](https://test3dprints.com/arduino/homework-writing-machine/).

Some adjustments needed to be made, for example increasing the diameter of some holes.

## Usage

To use the project, simply execute the `main.py` file:

```
python main.py
```

After running the script, you will be prompted to enter what you want the robot to draw. Once you confirm your input, the system will automatically handle all necessary processing and stream the drawing instructions to the plotter.

No further manual intervention is required.

## Demo

Here is a short video demonstrating the software and the drawing with the plotter.

Some more results we have drawn with the built plotter.
