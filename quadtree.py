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
# quad = na který kvadrant to má zavolat, kvůli znaménkům a výpočtu novýho midu


def quadtree_build(feat, points_out, len_x, len_y, x_mid, y_mid, rank, quad, num_poi):
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


    # rekurzivně volám funkci a dávám jí parametr len_x/2 a len_y/2


    # quadrant side length
    # označení kvadrantu

    if quad == 1:
        # new_x_mid = mid - předchozí +/- dělená vzdálenost
        nwe_y_mid =

    if quad == 2:
        new_x_mid =
        nwe_y_mid =

    quad_3:
        new_x_mid =
        nwe_y_mid =

    quad_4:
        new_x_mid =
        nwe_y_mid =

    # rekurzivní volání
    # quadtree_build(rank+1) rekurzvní volání na první kvadrant (bacha na vstupy!)
    # quadtree_build()
    # quadtree_build()
    # quadtree_build()

    return points_out