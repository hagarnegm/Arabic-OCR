from allimports import *


def skewCorrection(image):
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def preprocessing(image):
    # median=cv2.medianBlur(image,5)
    gray = rgb2gray(image)
    gray = cv2.bitwise_not(gray)
    rotated = skewCorrection(gray)
    # thresh = cv2.threshold(rotated, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # thresh=filters.apply_hysteresis_threshold(rotated,60,150)
    thresh = cv2.adaptiveThreshold(rotated, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, -2)
    kernel = np.ones((2, 2), np.uint8)
    kernel2 = np.ones((3, 3), np.uint8)
    #
    #     for i in range(np.shape(thresh)[0]):
    #         for j in range(np.shape(thresh)[1]):
    #             print(thresh[i][j])
    #     thresh=threshold_otsu(rotated)
    #     binary=rotated>=thresh
    # thresh=cv2.dilate(thresh,kernel,iterations=1)
    # edges=canny(thresh,sigma=0.3)
    # thresh=thresh-edges
    # morphed=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # thresh=cv2.erode(thresh,kernel,iterations=1)
    return thresh
