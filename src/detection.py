def get_closest_enemy(detections, screen_center_x, screen_center_y):
    """Find the enemy closest to crosshair (screen center)."""
    if not detections:
        return None
    
    closest = None
    min_distance = float('inf')
    
    # Priority: Heads > Bodies
    # Filter detections into heads and others
    head_detections = [d for d in detections if int(d[5]) in [1, 3]]
    body_detections = [d for d in detections if int(d[5]) in [0, 2]]
    
    # If any heads are detected, ONLY consider them
    # Otherwise, fall back to bodies
    target_candidates = head_detections if head_detections else body_detections
    
    for det in target_candidates:
        x1, y1, x2, y2, conf, cls_id = det
        # Get center of bounding box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Calculate distance from crosshair
        distance = ((center_x - screen_center_x) ** 2 + 
                   (center_y - screen_center_y) ** 2) ** 0.5
        
        if distance < min_distance:
            min_distance = distance
            closest = (center_x, center_y, x1, y1, x2, y2, conf, cls_id)
    
    return closest
