import cv2
import numpy as np

# note: need to fix lane detection conditions (lengths of shapes based on lighting)

# HSV range for yellow color
lower_yellow = np.array([20, 75, 100])
upper_yellow = np.array([40, 255, 255])

# look ahead pixel (y coordinate) (range 0-270)
# increasing this decreases the look ahead distance
val = 200 

def find_lane(bev):

    # conversion HSV color space
    hsv = cv2.cvtColor(bev, cv2.COLOR_BGR2HSV)

    # mask for yellow color using the HSV range, output is black and white
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    output = cv2.bitwise_not(mask)
    output = cv2.bitwise_not(output)

    img = output

    # define the number of regions of interest, increase ROIs for better resolution (more points)
    num_rois = img.shape[0] // 20

    # compute the histograms for each region of interest
    histograms = []
    for i in range(num_rois):
        roi = slice(i*img.shape[0]//num_rois, (i+1)*img.shape[0]//num_rois)
        histogram = np.sum(output[roi,:], axis=0)
        histograms.append(histogram)

    # smooth the histograms using a Gaussian filter to find local maximas
    smoothed_histograms = []
    for histogram in histograms:
        smoothed_histogram = np.convolve(histogram, np.ones(30)/30, mode='same')
        smoothed_histograms.append(smoothed_histogram)

    # split each smoothed histogram into two halves
    left_halves = []
    right_halves = []
    for smoothed_histogram in smoothed_histograms:
        left_half = smoothed_histogram[:len(smoothed_histogram)//2]
        right_half = smoothed_histogram[len(smoothed_histogram)//2:]
        left_halves.append(left_half)
        right_halves.append(right_half)

    # find the peak of each half in each region
    left_peaks = []
    right_peaks = []
    threshold = 50  # Set the threshold value ( change this according to the slices you choose)
    for i in range(num_rois):
        left_peak_index = np.argmax(left_halves[i])
        right_peak_index = np.argmax(right_halves[i]) + len(smoothed_histograms[i])//2
        if left_halves[i][left_peak_index] > threshold:
            left_peaks.append(left_peak_index)
        if right_halves[i][right_peak_index - len(smoothed_histograms[i])//2] > threshold:
            right_peaks.append(right_peak_index)

    # plot the points on the original image
    img_with_points = bev.copy()


    left_lane_x = []
    left_lane_y = []
    right_lane_x = []
    right_lane_y = []

    for i in range(num_rois):
        y = int(i * img.shape[0] / num_rois + img.shape[0] / num_rois / 2)
        if i < len(left_peaks):
            left_lane_x.append(left_peaks[i])
            left_lane_y.append(y)
        if i < len(right_peaks):
            right_lane_x.append(right_peaks[i])
            right_lane_y.append(y)


    #print(np.shape(left_lane_x),np.shape(right_lane_x))


    ############### HANDLING EDGE CASES ##############

    # WHEN ONLY RIGHT LANE IS DETECTED
    if len(left_lane_x) <10 and len(right_lane_x) > 10:
        print("ONLY RIGHT LANE DETECTED")
        right_fit = np.polyfit(right_lane_y, right_lane_x, 2)
        # Generate x values for plotting the curve
        plot_y = np.linspace(0, img.shape[0]-1, img.shape[0])
        right_fit_x = right_fit[0]*plot_y**2 + right_fit[1]*plot_y + right_fit[2]
        centre_fit_x = (right_fit_x - 200)

        for i in range(len(right_fit_x)):
            cv2.circle(img_with_points, (int(right_fit_x[i]), int(plot_y[i])), 1, (0, 0, 255), 2)
            cv2.circle(img_with_points, (int(centre_fit_x[i]), int(plot_y[i])), 1, (255, 255, 255), 2)
            cv2.circle(img_with_points, (int(240), int(val)), radius=1, color=(255, 0, 0), thickness=10)


        error = error = ((centre_fit_x[val]-240))
        return img_with_points,error
    
    
    # WHEN ONLY LEFT LANE IS DETECTED
    elif len(left_lane_x) >10 and len(right_lane_x) < 10:
        print("ONLY LEFT LANE DETECTED")
        left_fit = np.polyfit(left_lane_y, left_lane_x, 2)
        # Generate x values for plotting the curve
        plot_y = np.linspace(0, img.shape[0]-1, img.shape[0])
        left_fit_x = left_fit[0]*plot_y**2 + left_fit[1]*plot_y + left_fit[2]
        centre_fit_x = (left_fit_x + 200)

        for i in range(len(left_fit_x)):
            cv2.circle(img_with_points, (int(left_fit_x[i]), int(plot_y[i])), 1, (0, 0, 255), 2)
            cv2.circle(img_with_points, (int(centre_fit_x[i]), int(plot_y[i])), 1, (255, 255, 255), 2)
            cv2.circle(img_with_points, (int(240), int(val)), radius=1, color=(255, 0, 0), thickness=10)


        error = error = ((centre_fit_x[val]-240))
        return img_with_points,error
    
    # WHEN NONE OF THE LANES ARE DETECTED
    elif len(left_lane_x) <=10 and len(right_lane_x) <=10:
        print("STOP NO LANE DETCTED")
        error = np.inf
        return img_with_points,error
    

    # WHEN BOTH LANES DETECTED
    elif len(left_lane_x) >=10 and len(right_lane_x) >=10:
        # Fit a curve through the left and right lane points
        left_fit = np.polyfit(left_lane_y, left_lane_x, 2)
        right_fit = np.polyfit(right_lane_y, right_lane_x, 2)

        # Generate x values for plotting the curve
        plot_y = np.linspace(0, img.shape[0]-1, img.shape[0])
        left_fit_x = left_fit[0]*plot_y**2 + left_fit[1]*plot_y + left_fit[2]
        right_fit_x = right_fit[0]*plot_y**2 + right_fit[1]*plot_y + right_fit[2]
        centre_fit_x = (left_fit_x + right_fit_x)/2

        # plot the curve on the original image
        for i in range(len(left_fit_x)):
            cv2.circle(img_with_points, (int(left_fit_x[i]), int(plot_y[i])), 1, (0, 0, 255), 2)
            cv2.circle(img_with_points, (int(right_fit_x[i]), int(plot_y[i])), 1, (0, 0, 255), 2)
            cv2.circle(img_with_points, (int(centre_fit_x[i]), int(plot_y[i])), 1, (255, 255, 255), 2)
            cv2.circle(img_with_points, (int(240), int(val)), radius=1, color=(255, 0, 0), thickness=10)


        error = error = ((centre_fit_x[val]-240))

        return img_with_points,error


# function to transform the camera frame to BEV using the trapezoidal points
def warp_img(output,points,w,h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    img_warp = cv2.warpPerspective(output,matrix,(w,h))
    return img_warp


