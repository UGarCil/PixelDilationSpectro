from constants import *

# *LLM* FD >>> process_area()
# Signature: np.array,tuple,tuple,int
# purp. crop a subsection of an image to apply transformation
def process_area(image_array, start_coords, end_coords):
    # Ensure coordinates are integers
    x1, y1 = map(int, start_coords)
    x2, y2 = map(int, end_coords)

    # Ensure proper ordering of coordinates
    x_min, x_max = sorted((x1, x2))
    y_min, y_max = sorted((y1, y2))

    # Extract the subimage using slicing
    subarea = image_array[y_min:y_max, x_min:x_max]
    
    # Convert to grayscale if it's RGB
    # cv2.imwrite("output_image.png", subarea)
    
    if len(subarea.shape) == 3:
        subarea_gray = cv2.cvtColor(subarea, cv2.COLOR_RGB2GRAY)
    else:
        subarea_gray = subarea
    
    # Apply thresholding
    _, thresholded = cv2.threshold(subarea_gray, 127, 255, cv2.THRESH_BINARY)
    # print(thresholded)
    # print(thresholded.shape)
    return thresholded

# *LLM* >>> FD. dilate_subarea
# Signature = np.array, int
# purp. expand pixels by using convolutions to make lines thicker
def dilate_subarea(thresholded_subarea, kernel_size=2):
    """
    Thicken lines in the image using dilation.
    
    Args:
        subarea (np.array): The thresholded subarea
        kernel_size (int): Size of the dilation kernel
    
    Returns:
        np.array: Dilated image
    """
    # Invert the image (now black becomes white and vice versa)
    inverted = cv2.bitwise_not(thresholded_subarea)
    
    # Create a kernel for dilation
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # Apply dilation
    dilated = cv2.dilate(inverted, kernel, iterations=1)
    result = cv2.bitwise_not(dilated)
    # cv2.imwrite("output_image.png", result)
    return result

# *LLM* >>> FD. overlay_processed_area()
# Signature: np.array, np.array, tuple, tuple
def overlay_processed_area(original_img, processed_subarea, top_left, bottom_right):
    """
    Overlay the processed subarea back onto the original image.
    
    Args:
        original_img (np.array): The original image array
        processed_subarea (np.array): The processed subarea
        top_left (tuple): (x1, y1) coordinates
        bottom_right (tuple): (x2, y2) coordinates
    
    Returns:
        np.array: Original image with processed subarea overlaid
    """
    x1, y1 = top_left
    x2, y2 = bottom_right
    
    # Ensure correct order of coordinates
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    
    # Create a copy of the original image
    result = original_img.copy()
    
    # Convert processed subarea to 3 channels if needed
    if len(processed_subarea.shape) == 2:
        processed_subarea = cv2.cvtColor(processed_subarea, cv2.COLOR_GRAY2RGB)
    
    # Overlay the processed subarea
    result[y1:y2, x1:x2] = processed_subarea
    return result

def process_images(pts1,pts2):
    x1,y1 = pts1
    x2,y2 = pts2
    
    
    # iterate over the images
    images = [img for img in os.listdir(PATH_IMAGES) if ".png" in img]
    if not os.path.exists("./output/"):
        os.mkdir("output")
    for image in images:
        image_name = jn(PATH_IMAGES,image)
        dest_image_name = jn("./output/",f"o_{image}")
        calibIMG = Image.open(image_name)
        calibIMG_arr = np.array(calibIMG)
        calibIMG_arr = np.stack((calibIMG_arr,)*3, axis=-1)*255
        subarea_arr = process_area(calibIMG_arr,(x1,y1),(x2,y2))
        # dilate the area
        subarea_arr_thick = dilate_subarea(subarea_arr)
        result = overlay_processed_area(calibIMG_arr,subarea_arr_thick,(x1,y1),(x2,y2))
        cv2.imwrite(dest_image_name, result)
    # overlap the area on top of the previous image
    # save the image with original name + output