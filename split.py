import json
import quadtree

### loading input GeoJSON data

with open("input.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)


### creating new list od data from GeoJson

points = data["features"]
print(points)


### order coordinates by axis
# input = list points
# output = sorting data = list of points_sort_x, points_sort_y


points_sort_x = quadtree.find_max_min(points, 0)
print(points_sort_x)
points_sort_y = quadtree.find_max_min(points, 1)
print(points_sort_y)


### find min a max values of coordinates
# input = points
# output = end points of bounding box
# structure of bbox_end_poi = [x_max, x_min, y_max, y_min]


bbox_end_poi = quadtree.bbox(points)
print(bbox_end_poi)


### distribution data by quadtree and finally saving the output to a new GoeJSON file
# num_poi = the minimum number of points in the quadrant


quadrant = 0
num_poi = 50 # minimum number of points in quadrants


if len(points) <= num_poi:
    points_out = points.append([ID, coord[0], coord[1], 0]) # add cluster_id 0
    quadtree.create_new_geojson(points_out)

else:
    points_out = []
    new_points = quadtree.select_new_quad_poi(points, bbox_end_poi, quadrant)
    points_out = quadtree.quadtree_build(new_points, points_out, bbox_end_poi, quadrant, num_poi)
    quadtree.create_new_geojson(points_out)
