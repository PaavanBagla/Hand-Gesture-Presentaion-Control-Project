def detect_swipe(point_history, threshold=30):
    """
    Detects horizontal swipe direction from a sequence of finger positions.
    
    Args:
        point_history: List of recent finger positions (typically index finger tip coordinates)
        threshold: Minimum required horizontal movement in pixels to register as a swipe (default: 50px)
        
    Returns:
        "left" if a significant left swipe is detected
        "right" if a significant right swipe is detected
        None if no clear swipe is detected
    """
    
    # Early exit if we don't have enough data points to analyze
    if len(point_history) < 2:
        return None
    
    # Filter out any [0, 0] placeholder points (added when no gesture is active)
    # These zero points act as separators between distinct gestures
    valid_points = [p for p in point_history if p != [0, 0]]
    
    # Check if we have enough valid points after filtering
    if len(valid_points) < 2:
        return None
    
    # Extract the starting and ending positions from the gesture
    start_point = valid_points[0]  # First recorded position of the gesture
    end_point = valid_points[-1]   # Most recent position of the gesture
    
    # Calculate the total X (horizontal) and Y (vertical) movement
    x_diff = end_point[0] - start_point[0]  # Horizontal displacement (right=positive)
    y_diff = end_point[1] - start_point[1]  # Vertical displacement (down=positive)
    
    # Determine if the primary movement was horizontal (rather than vertical)
    if abs(x_diff) > abs(y_diff):  # Horizontal movement dominates
        # Check for left swipe (negative x displacement exceeding threshold)
        if x_diff < -threshold:
            return "left"
        # Check for right swipe (positive x displacement exceeding threshold)
        elif x_diff > threshold:
            return "right"
    
    # Return None if:
    # - Movement was primarily vertical
    # - Horizontal movement was below threshold
    # - Movement was ambiguous
    return None