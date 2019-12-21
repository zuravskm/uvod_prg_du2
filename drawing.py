import turtle
from math import fabs

### draw input points
# inputs = feats (set of input points) and borders of bounding box
# bbox = x_min, x_max, y_min, y_max


def draw_input_points(feats, bbox):
    coordinates = []
    for point in feats:
        coord = point['geometry']['coordinates']
        coordinates.append(coord)

    turtle.setworldcoordinates(bbox[0], bbox[2], bbox[1], bbox[3])  # adjusting the screen size using the endpoints
    turtle.speed(0)  # drawing speed
    turtle.hideturtle()  # symbol for turtle is not visible
    turtle.tracer(50, 1) # to speed up the drawing, 50 = only every 50 regular screen update is actually performed
    for poi in range(len(coordinates)):
        turtle.up() # no drawing when turtle moving
        turtle.setposition(coordinates[poi][0], coordinates[poi][1])  # turtle position at the beginning of drawing
        turtle.down() # drawing when turtle moving
        turtle.dot(6, "green")  # drawing dot (dot size, dot color)


### draw sides of the bounding box and lines of its recursive division into sub-quadrants
# input = ends points of bounding box


def draw_bbox(bbox):
    x_min, x_max, y_min, y_max = bbox
    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(x_min, y_min) # turtle position at the beginning of drawing
    turtle.down()
    turtle.forward(fabs(x_max - x_min)) # bottom side of the bounding box
    turtle.left(90)
    turtle.forward(fabs(y_max - y_min)) # right side of the bounding box
    turtle.left(90)
    turtle.forward(fabs(x_max - x_min)) # upper side of the bounding box
    turtle.left(90)
    turtle.forward(fabs(y_max - y_min)) # left side of the bounding box
    turtle.left(90)
    turtle.up()
