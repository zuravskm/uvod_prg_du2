import json
import quadtree as q

### loading input GeoJSON data

with open("input.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)


### creating new list od data from GeoJson

points = data["features"]
print(points)


### order coordinates by axis
# input = list points
# output = sorting data = list of points_sort_x, points_sort_y


points_sort_x = q.sort_by_axis(points, 0)
print("osa x", points_sort_x)
points_sort_y = q.sort_by_axis(points, 1)
print("osa y", points_sort_y)
# výsledek tohoto bloku je, že vytiskne pouze řazení podle osy y (což je správně seřazeno), ale podle osy x nevytiskne nic

souradnice = points.sort(key=lambda p: p["geometry"]["coordinates"])
osa_x = points.sort(key=lambda p: p["geometry"]["coordinates"][0])
osa_y = points.sort(key=lambda p: p["geometry"]["coordinates"][1])

print(souradnice)
print("x", osa_x)
print("y", osa_y)
# výsledkem tohoto bloku je vytisknuté None


### find min a max values of coordinates
# input = points
# output = end points of bounding box
# structure of bbox_end_poi = [x_max, x_min, y_max, y_min]

# bbox_end_poi = q.bbox(points)
# print(bbox_end_poi)


### distribution data by quadtree and finally saving the output to a new GoeJSON file
# quadrant = 0
# num_poi = 50 # minimum number of points in quadrants


# if len(points) <= num_poi:
    # points_out = points.append([ID, coord[0], coord[1], 0]) # add cluster_id 0
    # q.create_new_geojson(points_out)

# else:
    # points_out = []
    # new_points = q.select_new_quad_poi(points, bbox_end_poi, quadrant)
    # points_out = q.quadtree_build(new_points, points_out, bbox_end_poi, quadrant, num_poi)
    # q.create_new_geojson(points_out)
