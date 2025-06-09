def detect_swipe(point_history, threshold=150, min_frames=4, return_sensitivity=0.6):

    """
    Detects horizontal swipe direction from a sequence of finger positions.
    
    Args:
        point_history: List of (x,y) finger positions
        threshold: Minimum swipe distance in pixels
        min_frames: Minimum consecutive frames to consider
        return_sensitivity: How much return movement cancels swipe (0-1)
        
    Returns:
        "left" if a significant left swipe is detected
        "right" if a significant right swipe is detected
        None if no clear swipe is detected
    """
    
    # Filter out any [0, 0] placeholder points (added when no gesture is active)
    # These zero points act as separators between distinct gestures
    valid_points = [p for p in point_history if p != [0, 0]]
    
    # Check if we have enough valid points after filtering
    if len(valid_points) < min_frames:
        return None
    
    # Find the peak extent point (furthest from start)
    start_point = valid_points[0]
    peak_point = start_point
    max_distance = 0

    for point in valid_points:
        current_dist = abs(point[0] - start_point[0])
        if current_dist > max_distance:
            max_distance = current_dist
            peak_point = point
    
    # Calculate movement to peak point (not end point)
    x_diff = peak_point[0] - start_point[0]
    y_diff = peak_point[1] - start_point[1]
    
    # Check if primary movement was horizontal
    if abs(x_diff) <= abs(y_diff):
        return None

    # Check if movement exceeds threshold
    if abs(x_diff) < threshold:
        return None
    
    # Verify consistent direction to peak point
    direction = 1 if x_diff > 0 else -1
    for i in range(1, valid_points.index(peak_point)):
        dx = valid_points[i][0] - valid_points[i-1][0]
        if (dx * direction) < 0:  # Direction change
            return None
    
    # Check if hand returned too much (cancel swipe if returned beyond sensitivity)
    if len(valid_points) > valid_points.index(peak_point) + 1:
        return_dist = abs(valid_points[-1][0] - peak_point[0])
        if return_dist > (abs(x_diff) * return_sensitivity):
            return None
    
    return "right" if x_diff > 0 else "left"