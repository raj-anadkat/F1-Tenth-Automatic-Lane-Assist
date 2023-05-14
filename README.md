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

## Step 2: Overlaying Lines and Curves using Histograms and Optimizations



