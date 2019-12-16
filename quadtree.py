### order coordinates by axis
# input = list points
# output = sorting data


def sort_by_axis(points, axis):
    # print(type(axis))
    points.sort(key=lambda p: p["geometry"]["coordinates"][axis])
    return points


### compute length of bounding box
# it probably won't be needed
# maybe for turtle drawing


def bbox_len_x (points):
    points_sort_x = sort_by_axis(points, 0)
    x_min = points_sort_x[0][0]
    x_max = points_sort_x[-1][0]
    length_bbox_x = x_max - x_min
    # print(x_max, x_min)
    # print("x", length_bbox_x)
    return length_bbox_x


def bbox_len_y(points):
    points_sort_y = sort_by_axis(points, 1)
    y_max = points_sort_y[0][1]
    y_min = points_sort_y[-1][1]
    length_bbox_y = y_max - y_min
    # print(y_max, y_min)
    # print("y", length_bbox_y)
    return length_bbox_y


### find min a max values of coordinates
# input = points
# output = end points of bounding box
# output structure of bbox_end_poi = [x_max, x_min, y_max, y_min]


def bbox(points):
    bbox = []
    points_sort_x = sort_by_axis(points, 0) # sorts data by x-axis
    x_min = points_sort_x[0][0] # [0] selects the first element of the list
    x_max = points_sort_x[-1][0] # [-1] selects the last element of the list
    bbox.append(x_max)
    bbox.append(x_min)
    points_sort_y = sort_by_axis(points, 1) # sorts data by y-axis
    y_max = points_sort_y[0][1]
    y_min = points_sort_y[-1][1]
    bbox.append(y_max)
    bbox.append(y_min)
    return bbox


### select points in the new quadrant and creating a unique group identifier for the new quadrant (cluster_id)
# quad_box = boundaries of new quadrants
# quad_num = numbers of new quadrants

def select_new_quad_poi(points_in, quad_box, quad_num):
    new_poi = []
    for poi in points_in:
        ID = poi[0]
        coordx = poi[1]
        coordy = poi[2]
        old_cluster_id = poi[3]
        cluster_id = old_cluster_id + "1"
        if quad_box[1] <= coordx <= quad_box[0] and quad_box[3] <= coordy <= quad_box[2]:
            new_poi.append([ID, coordx, coordy, cluster_id])
            return new_poi
        else:
            continue


### distribution data by quadtree
# num_poi = the minimum number of points in the quadrant
# the first time using this function points_in = points
# the first time using this function quadrant = 0
# structure of bbox_end_poi = [x_max, x_min, y_max, y_min]


def quadtree_build(points_in, points_out, bbox_end_poi, quadrant, num_poi):
    if len(points_in) <= num_poi:
        for poi in points_in:
            points_out.append(poi)
        return points_out
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


### finally saving the output to a new GoeJSON file


def create_new_geojson (points_out):
    gj_structure = {'type': 'FeatureCollection'}
    # gj_structure['features'] = something
    with open("output.geojson", "w", encoding="utf-8") as f:
        points_out.dump(gj_structure, f, indent=2, ensure_ascii=False)
