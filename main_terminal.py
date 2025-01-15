# Created on Jan 8th 2025 by Uriel Garcilazo Cruz. Code generated by LLM indicated as *LLM*
'''
Version 1.2.0. is terminal based. Summon the application directly from the terminal.

This program takes a batch of images as input and provides a simple pygame based interface to delimit the area in a 
spectrogram that will be used for thresholding and dilation to give the effect of a thicker line.

Once the area has been setup, the program will perform the operations on a subset of the original image and perform the 
operations. Once completed, they will be placed on top of the original image


Positions in pixels:
 _   30,95
|

            _|  715,415
'''


from constants import *
from utils import *

# DD. ORIG_IMAGE
# img = np.array
# interp. an image opened via opencv
calibIMG = Image.open("./calibration.png")
calibIMG_arr = np.array(calibIMG)
SCREEN = calibIMG_arr.shape[1],calibIMG_arr.shape[0]
calibIMG_arr = np.stack((calibIMG_arr,)*3, axis=-1)*255
calibIMG_surf = np.flipud(np.rot90(calibIMG_arr))


# DD >> RECT_SELECT
# rect_sel = Recsel()
# interp. a bounding box, defined once, to contain the operations performed on pixels
class Recsel():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x1 = 30 
        self.y1 = 95
        self.x2 = 715
        self.y2 = 415
        # self.pressed_0_0 = True #initial press, defines topleft corner of the box
        # self.pressed_1_0 = False #dragging mode, allows to define a rectangle that ends at pointer
        # self.pressed_1_1 = False #completion mode. When True the program initiates other algorithms
        self.press_array = 0
        self.are_coor_set = False #determines whether to set the x,y corner of the bounding box, only once
        # self.rect = pygame.Rect(self.x, self.y, 1,1)
        # self.rect.topleft = (self.x, self.y)
        process_images((self.x1,self.y1),(self.x2,self.y2))
            
            


rect_sel = Recsel()
        
