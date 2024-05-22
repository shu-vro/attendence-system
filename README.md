# FACE RECOGNITION ATTENDANCE SYSTEM

## Requirements

-   Python 3.6
-   [requirements.txt](./requirements.txt)

## Setup

### Virtual Environment

```sh
cd path/to/cloned/folder
python3.6 -m venv .
source ./bin/activate
```

### Arduino setup

-   Connect the Arduino to the computer
-   Upload the [Arduino code](./firmata-config-arduino/firmata-config-arduino.ino) to the Arduino

## Installation

```sh
pip install -r requirements.txt
```

## Circuit Diagram

![Circuit Diagram](./fritzing/visual.png)
![Circuit Diagram](./fritzing/scheme.png)

## Running

```sh
python -u main.py # after activating the virtual environment
```
