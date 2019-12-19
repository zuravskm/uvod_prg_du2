from math import fabs

### function for find coordinates


def find_coord(feat):
    points_list = []
    for point in feat:
        coord = point['geometry']['coordinates']
        # print(coord)
        points_list.append(coord)
    return points_list


### order coordinates by axis
# input = list points, axis - [0] for axis x, [1] for axis y
# output = sorting data


def sort_by_axis(points, axis):
    # print(type(axis))
    points.sort(key=lambda p: p[axis])
    return points


### find borders of bounding box and middle lines for divided quadrants
# input are points
# output are borders of bounding box: x_max, x_min, y_max, y_min and middle: x_mid, y_mid


def find_borders_lines(points):
    sort_by_x = sort_by_axis(points, [0])
    x_min = sort_by_x[0][0]
    x_max = sort_by_x[-1][0]
    x_mid = fabs(x_max - x_min)/2

    sort_by_y = sort_by_axis(points, [1])
    y_min = sort_by_y[0][1]
    y_max = sort_by_y[-1][1]
    y_mid = fabs(y_max - y_min)/2

    return x_max, x_min, y_max, y_min, x_mid, y_mid


### distribution data by quadtree
# num_poi = the minimum number of points in the quadrant = 50
# the first time using this function points_in = points
# points_out = output list of points points
# borders = x_max, x_min, y_max, y_min, x_mid, y_mid
# quad = which quadrant to call because of signs and the calculation of the new quadrant half
# for the firts call of quadtree function is quad = 0


def quadtree_build(feat, points_out, half_len_x, half_len_y, x_mid, y_mid, rank, quad, num_poi):
    if len(feat) < num_poi:
        for poi in feat:
            poi["properties"]["cluster_id"] = 0
            points_out.append(poi)
        return

    # define a new quadrant and add points into them

    quad_top_left = []
    quad_top_right = []
    quad_bottom_left = []
    quad_bottom_right = []

    for point in feat:
        coord = point['geometry']['coordinates']
        if coord[0] < x_mid and coord[1] > y_mid:
            quad_top_left.append(coord)
        elif coord[0] > x_mid and coord[1] > y_mid:
            quad_top_right.append(coord)
        elif coord[0] < x_mid and coord[1] < y_mid:
            quad_bottom_left.append(coord)
        elif coord[0] > x_mid and coord[1] < y_mid:
            quad_bottom_right.append(coord)

    # designation of a particular quadrant

    if quad == 1:
        x_mid = x_mid - half_len_x
        y_mid = y_mid + half_len_y

    elif quad == 2:
        x_mid = x_mid + half_len_x
        y_mid = y_mid + half_len_y

    elif quad == 3:
        x_mid = x_mid - half_len_x
        y_mid = y_mid - half_len_y

    elif quad == 4:
        x_mid = x_mid + half_len_x
        y_mid = y_mid - half_len_y

    # recursive calls a function
    # the function gets modified parameters: len_x/2 and len_y/2, rank + 1
    quadtree_build(quad_top_left, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, rank+1, quad=1, num_poi=50)
    quadtree_build(quad_top_right, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, rank+1, quad=2, num_poi=50)
    quadtree_build(quad_bottom_left, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, rank+1, quad=3, num_poi=50)
    quadtree_build(quad_bottom_right, points_out, half_len_x/2, half_len_y/2, x_mid, y_mid, rank+1, quad=4, num_poi=50)

    return points_out