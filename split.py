import json
import quadtree as q
from math import fabs

with open("input.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)


feats = data["features"]
# only for control
print(feats)

x_max, x_min, y_max, y_min = q.calculate_bbox(feats)
# only for control
print(x_max, x_min, y_max, y_min)


# than pass to function of quadtree only half of the original length, which then recursively call and divide by 2
half_len_x = fabs(x_max - x_min)/2
half_len_y = fabs(y_max - y_min)/2
x_mid = (x_max + x_min)/2
y_mid = (y_max + y_min)/2

### distribution data by quadtree
# rank = 0 # if a user entered a list with less than 50 points, they would be given a cluster_id 0
quad = 0 # for the firts call of quadtree, because it must not recalculate half quadrants, but use the original ones

# list for output writing from recursive function
points_out = []

points_out = q.quadtree_build(feats, points_out, half_len_x, half_len_y, x_mid, y_mid, quad)


### finally saving the output to a new GoeJSON file

gj_structure = {'type': 'FeatureCollection'}
gj_structure['features'] = points_out
with open("output.geojson", "w", encoding="utf-8") as f:
    json.dump(gj_structure, f, indent=2, ensure_ascii=False)
