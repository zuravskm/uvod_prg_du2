### function for find coordinates


def find_coord(feat):
    points_list = []
    for point in feat:
        coord = point['geometry']['coordinates']
        # print(coord)
        points_list.append(coord)
    return points_list


### order coordinates by axis
# input = list points
# output = sorting data


def sort_by_axis(points, axis):
    # print(type(axis))
    points.sort(key=lambda p: p[axis])
    return points


### compute length of bounding box
# input = sorted points by given axis and axis: 0 = axis x, 1 = axis y
# output = length of the bounding box side


def bbox_len_2(points):
    points_sort_x = sort_by_axis(points, 0)
    x_min = points_sort_x[0][0]
    x_max = points_sort_x[-1][0]
    length_bbox_x = abs(x_max - x_min)
    points_sort_y = sort_by_axis(points, 1)
    y_max = points_sort_y[0][1]
    y_min = points_sort_y[-1][1]
    length_bbox_y = abs(y_max - y_min)
    return length_bbox_x, length_bbox_y


### function for dividing sides of a bounding box


def divide_sides_bbox(length):
    new_length = length/2
    return new_length


### select points in the new quadrant


def select_new_quad_poi(points):
    new_poi_1 = []
    new_poi_2 = []
    new_poi_3 = []
    new_poi_4 = []
    length = bbox_len_2(points)
    half_len_x = divide_sides_bbox(length[0])
    half_len_y = divide_sides_bbox(length[1])
    for poi in points:
        if (poi[0] > 0 and poi[0] < half_len_x) and (poi[1] > half_len_y and poi[1] < length[1]):
            # kvadrant vlevo na hoře
            new_poi_1.append(poi)
        elif (poi[0] > half_len_x and poi[0] < length[0]) and (poi[1] > half_len_y and poi[1] < length[1])
            # kvadrant vpravo nahoře
            new_poi_2.append(poi)
        elif (poi[0] > 0 and poi[0] < hlaf_len_x) and (poi[1] > 0 and poi[1] < half_len_y)
            # kvadrant vlevo dole
            new_poi_3.append(poi)
        elif (poi[0] > half_len_x and poi[0] < length[0]) and (poi[1] > 0 and poi[1] < half_len_y)
            # kvadrant vpravo dole
            new_poi_4.append(poi)
    return new_poi_1, new_poi_2, new_poi_3, new_poi_4


### add cluster_id function


def add_cluster_id(data, points_out, rank):
    for i in data:
        i["properties"]["cluster_id"] = rank # už zapisuju cluster_id


### distribution data by quadtree
# num_poi = the minimum number of points in the quadrant
# the first time using this function points_in = points
# the first time using this function quadrant = 0
# structure of bbox_end_poi = [x_max, x_min, y_max, y_min]


def quadtree_build(points_in, points_out, bbox_end_poi, quadrant, num_poi):
    if len(points_in) <= num_poi:
        for poi in points_in:
            points_out.append(poi)
        return


    return points_out

