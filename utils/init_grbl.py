import serial
import serial.tools.list_ports
import time
from grbl_streamer import GrblStreamer


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Found port: {port.device} - {port.description}")
    return [port.device for port in ports]


def my_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print(
        "MY CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args))
    )


def set_grbl_settings(file_path, grbl):
    with open(file_path) as f:
        settings_lines = [
            line.strip() for line in f if line.strip() and line.startswith("$")
        ]

    for setting in settings_lines:
        grbl.send_immediately(setting)
        time.sleep(0.1)


def init_grbl_streamer(baudrate, settings_path):
    available_ports = list_serial_ports()
    if not available_ports:
        print("No serial ports found!")
        exit()

    grbl = GrblStreamer(my_callback)
    grbl.setup_logging()

    set_grbl_settings(settings_path, grbl)

    port = available_ports[-1]
    grbl.cnect(port, baudrate)

    grbl.poll_start()

    return grbl
