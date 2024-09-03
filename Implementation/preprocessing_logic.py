import numpy as np
import cv2

def normalize_image(image):
    """
    Normalizes the image pixel values to a range of 0 to 1.
    """
    return image / 255.0

def reduce_noise(image, method='gaussian', kernel_size=5):
    """
    Reduces noise in the image using the specified method and kernel size.
    """
    if method == 'gaussian':
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif method == 'median':
        return cv2.medianBlur(image, kernel_size)
    else:
        return image

def skull_strip(image, threshold=10):
    """
    Performs skull stripping to remove non-brain tissues.
    Allows adjusting the threshold value for binary masking.
    """
    # Convert image to grayscale if not already
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

    # Apply binary threshold to get a mask
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Apply mask to original image to keep only brain region
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def remove_artifacts(image, method='default'):
    """
    Removes artifacts from the image using specified method.
    """
    if method == 'default':
        # Basic noise reduction
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    elif method == 'custom':
        # Placeholder for more sophisticated method
        # Can add specific parameters or methods based on requirements
        return cv2.bilateralFilter(image, 9, 75, 75)
    else:
        return image
