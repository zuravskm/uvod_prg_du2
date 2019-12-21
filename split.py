import json
import quadtree as q


### open and load input file
with open("input.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)


### select attribute "features" from input file
feats = data["features"]
# only for control
print(feats)
print(len(feats))


### calculation of end points of bounding box
bbox = q.calculate_bbox(feats)
# only for control
print(bbox)


### distribution data by quadtree
cluster_counter = [0] # the first value of the cluster_id adding list is 0

# list for output writing from recursive function
points_out = []

points_out = q.quadtree_build(feats, points_out, bbox, cluster_counter)

# only for control
print(len(points_out))


### finally saving the output to a new GoeJSON file

gj_structure = {'type': 'FeatureCollection'}
gj_structure['features'] = points_out
with open("output.geojson", "w", encoding="utf-8") as f:
    json.dump(gj_structure, f, indent=2, ensure_ascii=False)
