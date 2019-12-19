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


def bbox_len(points_sort, axis):
    axis_min = points_sort[0][axis]
    axis_max = points_sort[-1][axis]
    length_bbox = fabs(axis_max - axis_min)
    # print(axis_max, axis_min)
    # print(length_bbox)
    return length_bbox


### find min a max values of coordinates
# input = points
# output = end points of bounding box
# output structure of bbox_end_poi = [x_max, x_min, y_max, y_min]


def bbox(points):
    bbox = []
    points_sort_x = sort_by_axis(points, 0) # sorts data by x-axis
    x_min = points_sort_x[0][0] # [0] selects the first element of the sorted list
    x_max = points_sort_x[-1][0] # [-1] selects the last element of the sorted list
    bbox.append(x_max)
    bbox.append(x_min)
    points_sort_y = sort_by_axis(points, 1) # sorts data by y-axis
    y_max = points_sort_y[0][1]
    y_min = points_sort_y[-1][1]
    bbox.append(y_max)
    bbox.append(y_min)
    return bbox


### select points in the new quadrant -> rozdělit na dvě funkce!!!
# quad_box = boundaries of new quadrants
# quad_num = numbers of new quadrants

def select_new_quad_poi(points_in, quad_box, quad_num):
    new_poi = []
    for poi in points_in:
        coordx = poi[1]
        coordy = poi[2]
        old_cluster_id = poi[3]
        cluster_id = old_cluster_id + "1"
        if quad_box[1] <= coordx <= quad_box[0] and quad_box[3] <= coordy <= quad_box[2]:
            new_poi.append([ID, coordx, coordy, cluster_id])
        else:
            continue
        return new_poi


### add a unique group identifier for the new quadrant (cluster_id)


def add_cluster_id():
    pass


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
    else:
        center_box = [(bbox_end_poi[1]+bbox_end_poi[0])/2, (bbox_end_poi[3]+bbox_end_poi[2])/2]
        quad_1_bbox = [center_box[0], bbox_end_poi[1], bbox_end_poi[2], center_box[1]]
        quad_2_bbox = [bbox_end_poi[0], center_box[0], bbox_end_poi[2], center_box[1]]
        quad_3_bbox = [center_box[0], bbox_end_poi[1], center_box[1], bbox_end_poi[3]]
        quad_4_bbox = [bbox_end_poi[0], center_box[0], center_box[1], bbox_end_poi[3]]

        # counts points in the newly created quadrate and saves them in a new list
        new_poi_1 = select_new_quad_poi(points_in, quad_1_bbox, 1)
        new_poi_2 = select_new_quad_poi(points_in, quad_2_bbox, 2)
        new_poi_3 = select_new_quad_poi(points_in, quad_3_bbox, 3)
        new_poi_4 = select_new_quad_poi(points_in, quad_4_bbox, 4)

        # recursive function call
        quadtree_build(new_poi_1, points_out, quad_1_bbox, 1, num_poi)
        quadtree_build(new_poi_2, points_out, quad_2_bbox, 2, num_poi)
        quadtree_build(new_poi_3, points_out, quad_3_bbox, 3, num_poi)
        quadtree_build(new_poi_4, points_out, quad_4_bbox, 4, num_poi)
    return points_out

