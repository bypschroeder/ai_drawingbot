# AI-Drawingbot

The AI-Drawingbot is an interactive system that transforms text prompts into physical line drawings. It uses the LUIS image generation API from Hof University to create images based on user input. These images are then converted into vector-friendly line art and plotted onto paper using a custom-built XY-plotter made from 3D-printed parts and controlled by an Arduino.

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

4. **Create a `.env` file in the project root and add the following variables**

```
API_URL="https://your-ai-model-api-endpoint"
BAUDRATE=115200  # Adjust this value if your hardware requires a different baud rate
```

5. **Flash the Arduino with the customized Firmware**

- Copy the `grbl` folder from this repository to your Arduino libraries directory (typically located at `Documents/Arduino/libraries`)
- Open the Arduino IDE
- In the IDE, open the `grblUpload` sketch from `File > Examples > grbl`
- Connect the Arduino to your computer
- Select the correct board type and port in the Arduino IDE
- Click the Upload button to flash the firmware onto the Arduino

## Plotter

The plotter itself was built following this [tutorial](https://test3dprints.com/arduino/homework-writing-machine/).

Some adjustments needed to be made, for example increasing the diameter of some holes.

The firmware for this specific plotter was customized by enabling CoreXY kinematics and adding support for Z-axis control using a servo motor. This functionality was integrated with the help of the [Grbl_Pen_Servo repository](https://github.com/bdring/Grbl_Pen_Servo).

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
