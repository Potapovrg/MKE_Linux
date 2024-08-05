import os
import struct

def move_mouse(button, mouse_x, mouse_y, wheel):
    # Maximum and minimum values for a signed 8-bit integer
    max_movement = 127
    min_movement = -128

    # Split the movement into valid ranges for multiple reports if necessary
    while mouse_x != 0 or mouse_y != 0 or wheel != 0:
        # Determine the movement for this report
        move_x = max(min(mouse_x, max_movement), min_movement)
        move_y = max(min(mouse_y, max_movement), min_movement)
        move_wheel = max(min(wheel, max_movement), min_movement)

        # Prepare the HID report
        report = struct.pack('BBBB', button, move_x & 0xff, move_y & 0xff, move_wheel & 0xff)

        # Send the HID report
        with open('/dev/hidg1', 'wb') as f:
            f.write(report)

        # Update the remaining movements
        mouse_x -= move_x
        mouse_y -= move_y
        wheel -= move_wheel

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python move_mouse.py <button> <mouse_x> <mouse_y> <wheel>")
        sys.exit(1)

    try:
        button = int(sys.argv[1])
        mouse_x = int(sys.argv[2])
        mouse_y = int(sys.argv[3])
        wheel = int(sys.argv[4])
    except ValueError:
        print("Invalid input. Please enter valid integers.")
        sys.exit(1)

    move_mouse(button, mouse_x, mouse_y, wheel)
