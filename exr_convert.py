import OpenEXR
import Imath
import numpy as np

def load_exr_red_channel(filepath):
    # Open the EXR file
    file = OpenEXR.InputFile(filepath)
    
    # Get the header to retrieve the data window which gives image size
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    
    # Define the pixel type
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    
    # Read the red channel
    redstr = file.channel('R', pt)
    
    # Convert the string data to a numpy array
    red = np.fromstring(redstr, dtype=np.float32)
    red.shape = (size[1], size[0])  # Note the numpy array shape is (height, width)

    return red

# Example usage:
# Assuming you have an EXR file at the specified path
# red_channel_array = load_exr_red_channel('path_to_your_file.exr')
# print(red_channel_array)

print(load_exr_red_channel('step0.sim_cam.Depth.exr'))