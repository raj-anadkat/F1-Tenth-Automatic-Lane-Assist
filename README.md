# F1_tenth_Lane_Detection

## I. Goals
- Driving the car autonomously via Lane Detection

## II. Detecting the Lanes
The objective is to accurately identify the left and right lanes through classical computer vision techniques. While methods like Hough Transforms are effective in detecting straight lanes, they may not suffice for the F1 tenth scenario that involves wider lanes with sharp curves and mounting height limitations. Hence, exploring alternative techniques such as Bird's Eye View (BEV) becomes imperative. BEV involves transforming the input image into a top-down view, offering a better perspective of the lane markings and road curvature, and can be used for lane detection and centreline estimation

## Step 1 : Birds Eye View
The captured image has a resolution of (480,270). To identify the region of interest (ROI) in the image, we mark a trapezoidal shape. Using perspective transformation, we can obtain a bird's-eye view of the frame. The figure below illustrates the ROI and the bird's-eye view. The code for adjusting the ROI points can be found in a function named "find_ROI".
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/3db8bc1b-a69d-4768-9f5d-61feb4f9aabd" alt="ROI" width="400"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/dcbfbacd-f5ce-4cf6-be1e-27543ab1d041" alt="BEV" width="400" style="margin-left:50px;"/>
</p>

## Step 2: Detecting and Processing the Yellow using HSV and Masking
After obtaining the bird's-eye view (BEV), we need to detect the yellow lanes. To achieve this, we utilize OpenCV's HSV color space. We first isolate the regions with yellow color in the HSV range. These regions are then masked to white regions with 255 pixel intensity, while the remaining regions are marked as black with 0 pixel intensity, using binary thresholding. However, noise present in the image can cause gaps and inconsistencies in the binary thresholding. To address this, morpholocial operations such as dilation, erosion etc are applied to fill out the gaps. However, life is tough and there may still be some noise, this can be looked after later.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/d0ee5e9e-4885-43a3-9ff8-8c567b359003" alt="mask" width="400"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/98e0ca6e-0d7a-4bd0-90ae-6fde26ce22a0" alt="dilation" width="400" style="margin-left:50px;"/>
</p>

## Step 3: Detecting Points for Lines and Curves using Histograms
The masked image still contains noise despite prior image processing steps. This creates difficulties when applying traditional contour detection methods like Canny edge detection. Additionally, fitting straight lines to the lanes is not feasible due to the nature of F1-tenth racetracks, which contain numerous curves and turns. As a result, it is necessary to identify specific regions of interest for the left and right lanes.

One approach to accomplishing this task is to split the image vertically into two halves and examine the histogram of each half in horizontal slices of 10-20 pixels. This allows us to detect areas of high pixel concentration for the left and right lanes. The pixel indices corresponding to these regions of interest can then be extracted and used as inputs for polynomial curve fitting algorithms. By estimating the curvature of the lanes using polynomial curves, we can obtain a more accurate representation of the lane boundaries and navigate the racetrack more effectively. Furthermore, the slices can be increase to have more resolution , and the histograms can be smoothened to return the top indices.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/4e3f2b4b-914d-4f00-927e-249174e0cc3f" alt="mask" width="400"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/98bb80ef-c705-404e-8e0f-0250b96c65e1" alt="dilation" width="400" style="margin-left:50px;"/>
</p>

## Step 4: Curve Fitting and Lane Marking
To extract the lane lines from the bird's-eye view image, the indices of the white lane points can be determined for each vertical slice. Once the indices are obtained, the lane lines can be fitted using either RANSAC or numpy's Polynomial Fitting to obtain curves that represent the lanes. After fitting the curves, any outliers can be rejected using the chosen method. The resulting left and right lane lines can be used to calculate the center line by taking their average. This center line can then be overlaid on top of the bird's-eye view image to visualize the final result.

The Camera Image and the overlayed BEV curves can be observed in the images below, which illustrate the effectiveness of the curve fitting and outlier rejection process.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/9f91ea52-3c4e-4ca1-b646-846c6c05317d" alt="img" width="300"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/cd133adc-e10f-4c8a-aef1-9d77008c8520" alt="curve" width="300"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/dcca7e08-674f-4bd0-857a-35e419968644" alt="curve" width="300"/>
  
</p>
 


