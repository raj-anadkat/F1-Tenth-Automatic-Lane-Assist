# F1_tenth_Lane_Detection

## I. Goals
- Driving the car autonomously via Lane Detection

## II. Detecting the Lanes
The objective is to accurately identify the left and right lanes through classical computer vision techniques. While methods like Hough Transforms are effective in detecting straight lanes, they may not suffice for the F1 tenth scenario that involves wider lanes with sharp curves and mounting height limitations. Hence, exploring alternative techniques such as Bird's Eye View (BEV) becomes imperative. BEV involves transforming the input image into a top-down view, offering a better perspective of the lane markings and road curvature, and can be used for lane detection and centreline estimation

## Step 1
The image is first captured in a resolution of (480,270), the trapezoidal region of interests are marked as shown in the figure below, using Perspective Transformation, we can find the Birds eye view of the frame as shown in the figure below.
