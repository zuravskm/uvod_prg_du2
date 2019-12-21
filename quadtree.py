from math import fabs

### function for extract coordinates from data
# inputs = feats (set of entry points)
# outputs = only lists of x,y coordinates for each point


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
# inputs are feats
# outputs are borders of bounding box: x_max, x_min, y_max, y_min


def calculate_bbox(feats):
    x, y = extract_coord(feats)
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    return x_min, x_max, y_min, y_max


### distribution data by quadtree
# inputs are feats, output list points_out, borders of bounding box and list for count cluster_id
# output is a list of points divided by quardants into groups of less than 50 points
# cluster_id is added in the end condition of recursive function


def quadtree_build(feats, points_out, bbox, cluster_counter):
    if len(feats) < 50:
        cluster = cluster_counter[0]
        for poi in feats:
            poi['properties']['cluster_id'] = cluster
            points_out.append(poi)
        cluster_new = cluster_counter.pop()
        cluster_counter.append(cluster_new + 1)
        return points_out

    # calculate the center of the bounding box
    mid = [(bbox[1] + bbox[0]) / 2, (bbox[3] + bbox[2]) / 2]

    # counting new min and max values of new quadrant
    bbox_quad_1 = [bbox[0], mid[0], mid[1], bbox[3]]  # top left quadrant
    bbox_quad_2 = [mid[0], bbox[1], mid[1], bbox[3]]  # top left quadrant
    bbox_quad_3 = [bbox[0], mid[0], bbox[2], mid[1]]  # bottom left quadrant
    bbox_quad_4 = [mid[0], bbox[1], bbox[2], mid[1]]  # bottom right quadrant

    # define a new quadrant and add points into them
    quad_top_left = []
    quad_top_right = []
    quad_bottom_left = []
    quad_bottom_right = []

    for point in feats:
        coord = point['geometry']['coordinates']
        coordx = coord[0]
        coordy = coord[1]
        if coordx <= mid[0] and coordy > mid[1]: # top left quadrant
            quad_top_left.append(point)
        elif coordx > mid[0] and coordy >= mid[1]: # top right quadrant
            quad_top_right.append(point)
        elif coordx < mid[0] and coordy <= mid[1]: # bottom left quadrant
            quad_bottom_left.append(point)
        elif coordx >= mid[0] and coordy < mid[1]: # bottom right quadrant
            quad_bottom_right.append(point)

    # recursive calls of function
    quadtree_build(quad_top_left, points_out, bbox_quad_1, cluster_counter)
    quadtree_build(quad_top_right, points_out, bbox_quad_2, cluster_counter)
    quadtree_build(quad_bottom_left, points_out, bbox_quad_3, cluster_counter)
    quadtree_build(quad_bottom_right, points_out, bbox_quad_4, cluster_counter)

    return points_out
