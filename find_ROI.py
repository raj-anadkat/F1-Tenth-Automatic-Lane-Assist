import cv2
import numpy as np

# setting up video capture device
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
cap.set(cv2.CAP_PROP_FPS, 60)

# HSV range for yellow, modify it according to the track lighting
lower_yellow = np.array([20, 70, 100])
upper_yellow = np.array([35, 255, 255])

# initial points for warping
points = np.float32([[191, 200], [760-191, 200], [0, 400], [960, 400]])
w = 200
h = 200

def on_point_1_x_change(val):
    points[0][0] = val
def on_point_1_y_change(val):
    points[0][1] = val
def on_point_2_x_change(val):
    points[1][0] = val
def on_point_2_y_change(val):
    points[1][1] = val
def on_point_3_x_change(val):
    points[2][0] = val
def on_point_3_y_change(val):
    points[2][1] = val
def on_point_4_x_change(val):
    points[3][0] = val
def on_point_4_y_change(val):
    points[3][1] = val

# creating the trackbar for finding ROI
cv2.namedWindow('points')
cv2.createTrackbar('point 1 x', 'points', 200, 960, on_point_1_x_change)
cv2.createTrackbar('point 1 y', 'points', 200, 540, on_point_1_y_change)
cv2.createTrackbar('point 2 x', 'points', 400, 960, on_point_2_x_change)
cv2.createTrackbar('point 2 y', 'points', 200, 540, on_point_2_y_change)
cv2.createTrackbar('point 3 x', 'points', 200, 960, on_point_3_x_change)
cv2.createTrackbar('point 3 y', 'points', 400, 540, on_point_3_y_change)
cv2.createTrackbar('point 4 x', 'points', 400, 960, on_point_4_x_change)
cv2.createTrackbar('point 4 y', 'points', 400, 540, on_point_4_y_change)
cv2.resizeWindow('points', 800, 500)


def draw_points(frame, points):
    for point in points:
        cv2.circle(frame, tuple(map(int, point)), 5, (0, 0, 255), -1)

def warp_img(output,points,w,h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    img_warp = cv2.warpPerspective(output,matrix,(w,h))
    return img_warp

while True:

    ret, frame = cap.read()

    # converting the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # masking for yellow color using the HSV range
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    output = cv2.bitwise_not(mask)
    output = cv2.bitwise_not(output)

    # call warp function to the frame based on the selected points
    img_warp = warp_img(output, points, w, h)
    img_warp = cv2.resize(img_warp, (frame.shape[1], frame.shape[0]))
    img_warp_2 = warp_img(frame, points, w, h)
    img_warp_2 = cv2.resize(img_warp_2, (frame.shape[1], frame.shape[0]))
    
    # canny edge detection
    edges = cv2.Canny(img_warp_2, 200, 400, apertureSize=7)
    cv2.imshow('edges',edges)

    # visualize the trapezoidal points on the original frame
    draw_points(frame, points)

    # show the original frame and the warped frame
    cv2.imshow('Warping',img_warp)
    cv2.imshow('frame', frame)
    cv2.imshow('Original Warp', img_warp_2)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# release the video capture device and close all windows
cap.release()
cv2.destroyAllWindows()
