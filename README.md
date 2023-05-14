# F1 Tenth Automatic Lane Assist

## I. Goals
- Develop an autonomous driving system that uses classical computer vision techniques to detect and follow lanes
- Comply with Camera mounting height and wide lane constraints with limited Field of view (55 degrees)
- Ensure the system is robust to detect curves , operate in different lighting conditions and operate in real time.

## II. Detecting the Lanes
The objective is to accurately identify the left and right lanes through classical computer vision techniques. While existing methods on the internet use techniques like canny edge detection and Hough Transforms to detect straight lanes, they may not suffice for the F1 tenth scenario that involves wider lanes with tight turns and camera mounting height limitations. Hence, exploring alternative techniques such as Bird's Eye View (BEV) becomes imperative. BEV involves transforming the input image into a top-down view, offering a better perspective of the lane markings, road curvature and lookahead distance, and can be used for lane detection and centreline estimation

## Step 1 : Birds Eye View
 <p float="left">
<img src= "https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/228b8736-ab66-4467-9386-7f805edc6a18"alt="ROI" width="400"/>
 </p>

The captured image has a resolution of (480,270). To identify the region of interest (ROI) in the image, we mark a trapezoidal shape. Using perspective transformation, we can obtain a bird's-eye view of the frame. The figure below illustrates the ROI and the bird's-eye view. OpenCV provides a simple way to perform bird's eye view transformation using the warpPerspective function. The function requires two sets of points: the source points, which are the coordinates of the corners of the original image, and the destination points, which are the coordinates of where you want those corners to be in the transformed image. The code for adjusting the ROI points can be found in a function named "find_ROI".

  
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/3db8bc1b-a69d-4768-9f5d-61feb4f9aabd" alt="ROI" width="300"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/dcbfbacd-f5ce-4cf6-be1e-27543ab1d041" alt="BEV" width="300" style="margin-left:50px;"/>
</p>

## Step 2: Detecting and Processing the Yellow Lanes using HSV and Masking
After obtaining the bird's-eye view (BEV), we need to detect the yellow lanes. To achieve this, we utilize OpenCV's HSV color space. We first isolate the regions with yellow color in the HSV range. These regions are then masked to white regions with 255 pixel intensity, while the remaining regions are marked as black with 0 pixel intensity, using binary thresholding. However, noise present in the image can cause gaps and inconsistencies in the binary thresholding. To address this, morpholocial operations such as dilation, erosion etc are applied to fill out the gaps. However, life is tough and there may still be some noise, this can be looked after later.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/d0ee5e9e-4885-43a3-9ff8-8c567b359003" alt="mask" width="300"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/98e0ca6e-0d7a-4bd0-90ae-6fde26ce22a0" alt="dilation" width="300" style="margin-left:50px;"/>
</p>

## Step 3: Detecting Points for Lines and Curves using Histograms
The masked image still contains noise despite prior image processing steps. This creates difficulties when applying traditional contour detection methods like Canny edge detection. Additionally, fitting straight lines to the lanes is not feasible due to the nature of F1-tenth racetracks, which contain numerous curves and turns. As a result, it is necessary to identify specific regions of interest for the left and right lanes.
 <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/5fdf67b2-fa84-4c3b-85ae-670154b93607" alt="mask" width="400"/>

This can be done by splitting the image vertically into two halves and examine the histogram of each half in horizontal slices of 10-20 pixels. This allows us to detect areas of high pixel concentration for the left and right lanes. The pixel indices corresponding to these regions of interest can then be extracted and used as inputs for polynomial curve fitting algorithms. By estimating the curvature of the lanes using polynomial curves, we can obtain a more accurate representation of the lane boundaries and navigate the racetrack more effectively. Furthermore, the slices can be increase to have more resolution , and the histograms can be smoothened to return the top indices.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/4e3f2b4b-914d-4f00-927e-249174e0cc3f" alt="mask" width="400"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/98bb80ef-c705-404e-8e0f-0250b96c65e1" alt="dilation" width="400" style="margin-left:50px;"/>
</p>

## Step 4: Curve Fitting and Lane Marking
To extract the lane lines from the bird's-eye view image, the indices of the white lane points can be determined for each horizontal slice. Once the indices are obtained, the lane lines can be fitted using either RANSAC or numpy's Polynomial Fitting to obtain curves that represent the lanes. After fitting the curves, any outliers can be rejected using the chosen method. The resulting left and right lane lines can be used to calculate the center line by taking their average. This center line can then be overlaid on top of the bird's-eye view image to visualize the final result.

The Camera Image and the overlayed BEV curves can be observed in the images below, which illustrate the effectiveness of the curve fitting and outlier rejection process.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/9f91ea52-3c4e-4ca1-b646-846c6c05317d" alt="img" width="200"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/53427130-6143-4caa-a8e3-db6e31b8ad61"alt="img" height="115"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/cd133adc-e10f-4c8a-aef1-9d77008c8520" alt="curve" width="200"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/dcca7e08-674f-4bd0-857a-35e419968644" alt="curve" width="200"/> 
</p>

## Step 5: Handling Edge Cases - When only One lane is Detected/ No Lanes Detected
Detecting only one side of a lane or none at all can be a challenging task, especially in the case of F1 tracks with aggressive curves and lanes that are two car lengths wide. In order to overcome this issue, it is possible to count the number of histogram peaks detected in the left and right sides of the image.

If the number of peaks in the left lane is below a certain threshold, this indicates that the left lane is not detected, and the system may have to rely on the right lane and estimate the center line. To accomplish this, the average width of the track can be estimated and half of this value can be added to the right lane position. If no lanes are detected, the error can be set to inifinity indicating application of brakes. This approach can increase the robustness of the system and enable it to handle scenarios where one lane or no lanes are detected.
<p float="left">
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/16ea79b6-8fab-4349-8356-427ff8c60bef" alt="half_lane" width="300"/>
  <img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/4786a55d-ce33-4fd7-a5c3-cf385070f25c" alt="approx" width="300" style="margin-left:50px;"/>
</p>

## III. Calculating Error in the Trajectory
Once the Centre Line has been estimated, the next step is to calculate the error between the car's heading and the estimated Centre Line. This can be achieved by selecting a reference point in the image that corresponds to the Centre of the track and calculating its deviation from the estimated Centre Line. Using the Birds eye view is here an advantage as you can easily set the reference point. The reference point can be selected by considering the dimensions of the car and the desired trajectory.

The error is then calculated as the distance between the reference point and the estimated Centre Line. 
$$error = x_{e} - x_{i}$$, 
where $x_{e}$ is the x-coordinate of the estimated centerline at a lookahead distance, and $x_{i}$ is the x-coordinate of the image center, which is typically half of the image width.

The direction of the error (left or right) indicates the direction in which the car should steer to stay on track. Once the error has been calculated, it can be used to determine the Steering Angle of the car.
 </p>
<img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/4ab3c2f4-1074-43e0-9033-6c46db1fa83a" alt="half_lane" width="400"/>
 </p>

## IV. Calculating Steering Angle and Velocities
The error term in the lane centering algorithm is a measure of the deviation of the estimated lane centerline from the actual center of the track in the image. The magnitude of the deviation can be quite large, ranging from -150 to 150 pixels, depending on the width of the track. In order to ensure that the error term is scaled to a range appropriate for the steering angle range of [-0.35, 0.35], the error is first normalized by dividing it by a scaling factor.

Once the normalized error value is obtained, it is used to calculate the proportional, integral, and derivative terms of the PID controller. The proportional term represents the immediate response of the system to the error and is proportional to the magnitude of the error. The integral term represents the cumulative effect of the error over time and helps to eliminate steady-state errors. The derivative term represents the rate of change of the error and helps to dampen oscillations.

$$ u(t)=K_{p}e(t)+K_{i}\int_{0}^{t}e(t^{\prime})dt^{\prime}+K_{d}\frac{d}{dt}(e(t)) $$

Here, $K_p$, $K_i$, and $K_d$ are constants that determine how much weight each of the three components (proportional, integral, derivative) contribute to the control output $u(t)$. $u(t)$ in our case is the steering angle we want the car to drive at. The error term $e(t)$ is the difference between the set point and the parameter we want to maintain around that set point.

Finally, the output of the PID controller is the steering angle that will be used to adjust the direction of the vehicle. constrained to a range of [-0.35, 0.35] which are the minimum and maximum steering angles.

Depending on the steering angles, velocities are assigned to ensure lower speeds during curves and higher speeds on the straights.

## V. Results
The Birds Eye View image can be Re-Projected Back to the camera frame and other methods such as Object Detection can be implemented to adopt startegies like Lane Switching. This can be done by defining two race-lines instead of one centre line that was calculated.

</p>
<img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/43d557c9-c99e-4082-9d6e-00120bc4cef8" alt="half_lane" width="300"/>
<img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/1ed5d994-4005-410e-a094-da673d19121b" alt="half_lane" width="300"/>
<img src="https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/0d1c79c3-08ed-44a5-a723-407ee14b5b6f" alt="half_lane" height="105"/>

</p>

https://github.com/raj-anadkat/F1_tenth_Lane_Detection/assets/109377585/05299137-f89c-4d51-a73d-8546f7eca817





