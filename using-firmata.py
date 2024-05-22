import pyfirmata
import time

if __name__ == '__main__':
    board = pyfirmata.Arduino('/dev/ttyUSB0')
    print("Communication Successfully started")

    buzzer = board.get_pin('d:7:o')
    dir(buzzer)

    buzzer.write(1)

    # while True:
    #     buzzer.write(1)
    #     time.sleep(1)
    #     buzzer.write(0)
    #     time.sleep(1)

    board.exit()
