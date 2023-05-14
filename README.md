# F1_tenth_Lane_Detection

## I. Goals
- Driving the car autonomously via Lane Detection

## II. Detecting the Lanes
The objective is to accurately identify the left and right lanes through classical computer vision techniques. While methods like Hough Transforms are effective in detecting straight lanes, they may not suffice for the F1 tenth scenario that involves wider lanes with sharp curves and mounting height limitations. Hence, exploring alternative techniques such as Bird's Eye View (BEV) becomes imperative. BEV involves transforming the input image into a top-down view, offering a better perspective of the lane markings and road curvature, and can be used for lane detection and centreline estimation

## Step 1
The image is first captured in a resolution of (480,270), the trapezoidal region of interests are marked as shown in the figure below, using Perspective Transformation, we can find the Birds eye view of the frame as shown in the figure below.

<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/3db8bc1b-a69d-4768-9f5d-61feb4f9aabd" alt="ROI" width="400"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/dcbfbacd-f5ce-4cf6-be1e-27543ab1d041" alt="BEV" width="400" style="margin-left:50px;"/>
</p>


