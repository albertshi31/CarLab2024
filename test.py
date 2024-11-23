import pixy
from pixy import BlockArray
from ctypes import c_int

# Initialize Pixy2
pixy.init()
pixy.change_prog("color_connected_components")  # Ensure the program for color detection is loaded

# Create an array to store detected blocks
blocks = BlockArray(100)
frame = 0

# Function to detect green objects
def is_green_object_detected():
    global frame
    count = pixy.ccc_get_blocks(100, blocks)
    
    if count > 0:
        print(f"Frame {frame}: Detected {count} block(s).")
        for i in range(count):
            block = blocks[i]
            print(f"Block {i + 1}: Signature {block.signature}, X: {block.x}, Y: {block.y}, Width: {block.width}, Height: {block.height}")

            # Assuming green is Signature 1 (update based on your Pixy2 signature configuration)
            if block.signature == 1:
                print("Green object detected!")
                return True

    frame += 1
    return False

# Main loop
try:
    while True:
        green_detected = is_green_object_detected()
        if green_detected:
            print("Green object detected in the frame!")
except KeyboardInterrupt:
    print("Exiting...")
