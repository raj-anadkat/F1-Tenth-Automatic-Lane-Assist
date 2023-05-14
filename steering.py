import numpy as np

# velocity range
max_velocity = 1.5
mid_velocity = 1
min_velocity = 0.5

# PID control constants
KP = 0.5
KI = 0.0
KD = 0.1

# PID control variables
last_error = 0.0
integral = 0.0
last_time = None

# steering angle limits
MIN_ANGLE = -0.35
MAX_ANGLE = 0.35

# Scaling factor for error term (change based on track width)
SCALE_FACTOR = 150.0

def pid_control(error, cur_time):
    global last_error, integral, last_time

    # initialize last_time on the first call
    if last_time is None:
        last_time = cur_time
        return 0.0

    # calculate time difference
    delta_time = cur_time - last_time

    # scale error term
    error /= SCALE_FACTOR

    # calculate PID terms
    p_term = KP * error
    integral += error * delta_time
    i_term = KI * integral
    d_term = KD * (error - last_error) / delta_time

    # calculate steering angle
    steering_angle = p_term + i_term + d_term

    # constarin steering angle to MIN_ANGLE and MAX_ANGLE
    steering_angle = max(MIN_ANGLE, min(MAX_ANGLE, steering_angle))

    # update last error and last time
    last_error = error
    last_time = cur_time

    return steering_angle

def get_velocity(steering_angle):
    # determine speed based on steering angle
    if abs(steering_angle) <= 0.1:
        velocity = max_velocity
    elif abs(steering_angle) <= 0.2:
        velocity = mid_velocity
    else:
        velocity = min_velocity

    return velocity




