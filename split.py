import json
import quadtree as q
from math import fabs

with open("input.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)


feats = data["features"]
# only for control
print(feats)

points = q.extract_coord(feats)
# only for control
print(points)

x_max, x_min, y_max, y_min, x_mid, y_mid = q.find_borders_lines(points)
# only for control
print(x_max, x_min, y_max, y_min, x_mid, y_mid)


# than pass to function of quadtree only half of the original length, which then recursively call and divide by 2
length_bbox_x = fabs(x_max - x_min)
half_len_x = length_bbox_x/2
length_bbox_y = fabs(y_max - y_min)
half_len_y = length_bbox_y/2


### distribution data by quadtree
rank = 0 # if a user entered a list with less than 50 points, they would be given a cluster_id 0
quad = 0 # for the firts call of quadtree, because it must not recalculate half quadrants, but use the original ones
num_poi = 50 # minimum number of points in quadrants

# list for output writing from recursive function
points_out = []

completely_final_list = q.quadtree_build(feats, points_out, half_len_x, half_len_y, x_mid, y_mid, rank, quad, num_poi)


### finally saving the output to a new GoeJSON file

gj_structure = {'type': 'FeatureCollection'}
gj_structure['features'] = completely_final_list
with open("output.geojson", "w", encoding="utf-8") as f:
    completely_final_list.dump(gj_structure, f, indent=2, ensure_ascii=False)
