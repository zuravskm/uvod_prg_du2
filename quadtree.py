from math import fabs

### function for extract coordinates from data
# input = feats (set of entry points)
# output = only list of x,y coordinates for each point


def extract_coord(feats):
    coord_x = []
    coord_y = []
    for point in feats:
        x_axis = point['geometry']['coordinates'][0]
        y_axis = point['geometry']['coordinates'][1]
        coord_x.append(x_axis)
        coord_y.append(y_axis)
    return coord_x, coord_y


### find borders of bounding box
# input are feats
# output are borders of bounding box: x_max, x_min, y_max, y_min


def calculate_bbox(feats):
    x, y = extract_coord(feats)
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    return x_min, x_max, y_min, y_max


### distribution data by quadtree
# points_out = output list of points
# quad = which quadrant to call because of signs and the calculation of the new quadrant half
# for the firts call of quadtree function is quad = 0


def quadtree_build(feats, points_out, half_len_x, half_len_y, x_mid, y_mid, cluster_counter, quad=0):
    if len(feats) < 50:
        cluster = cluster_counter[0]
        for poi in feats:
            poi['properties']['cluster_id'] = cluster
            points_out.append(poi)
        cluster_new = cluster_counter.pop()
        cluster_counter.append(cluster_new + 1)
        return points_out

    # designation of a particular quadrant
    # always add or subtract half of the bounding box length depending on the new quadrant

    if quad == 1: # top left quadrant
        x_mid = x_mid - half_len_x
        y_mid = y_mid + half_len_y

    elif quad == 2: # top right quadrant
        x_mid = x_mid + half_len_x
        y_mid = y_mid + half_len_y

    elif quad == 3: # bottom left quadrant
        x_mid = x_mid - half_len_x
        y_mid = y_mid - half_len_y

    elif quad == 4: # bottom right quadrant
        x_mid = x_mid + half_len_x
        y_mid = y_mid - half_len_y

    # define a new quadrant and add points into them

    quad_top_left = []
    quad_top_right = []
    quad_bottom_left = []
    quad_bottom_right = []

    for point in feats:
        coord = point['geometry']['coordinates']
        coordx = coord[0]
        coordy = coord[1]
        if coordx < x_mid and coordy > y_mid: # top left quadrant
            quad_top_left.append(point)
        elif coordx > x_mid and coordy > y_mid: # top right quadrant
            quad_top_right.append(point)
        elif coordx < x_mid and coordy < y_mid: # bottom left quadrant
            quad_bottom_left.append(point)
        elif coordx > x_mid and coordy < y_mid: # bottom right quadrant
            quad_bottom_right.append(point)

    # recursive calls of function
    # this recursive function gets modified parameters: len_x/2 and len_y/2
    quadtree_build(quad_top_left, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, cluster_counter, quad=1)
    quadtree_build(quad_top_right, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, cluster_counter, quad=2)
    quadtree_build(quad_bottom_left, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, cluster_counter, quad=3)
    quadtree_build(quad_bottom_right, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, cluster_counter, quad=4)

    return points_out
