import cv2


def image_to_black_white(im, threshold=123):
    im[im >= threshold] = 255
    im[im < threshold] = 0
    return im


# Grab the image to manipulate
image = cv2.imread('play_button.png', cv2.IMREAD_GRAYSCALE)
image = image_to_black_white(image)
cv2.imshow('Image Viewer', image)
cv2.waitKey()

# If you get warnings, run this in the terminal:
# sudo apt-get install gtk2-engines-pixbuf
