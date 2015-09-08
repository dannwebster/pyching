math = ximport("math")

WEDGE_ANGLE = math.pi * 2.0 / 64.0
WEDGE_DEGREES = 360.0 / 64.0

def rotational_angle(i, angle_offset_percent=0):
    angle = WEDGE_ANGLE * i
    angle_offset = WEDGE_ANGLE * angle_offset_percent
    angle = angle + angle_offset
    return angle
    
def rotational_degrees(i, angle_offset_percent=0):
    angle = WEDGE_DEGREES * i
    angle_offset = WEDGE_DEGREES * angle_offset_percent
    angle = angle + angle_offset
    return angle
    
def cos_sin(i, angle_offset_percent=0):
    angle = rotational_angle(i, angle_offset_percent)
    cos = math.cos(angle)
    sin = math.sin(angle)
    return cos, sin
    
def radial_coordinates(x_center, y_center, radius, i, angle_offset_percent=0):
    cos, sin = cos_sin(i, angle_offset_percent)
    w = radius * cos
    h = radius * sin
    x1 = x_center + w
    y1 = y_center + h
    return x1, y1

def divider(x_center, y_center, radius, i):
    x1, y1 = radial_coordinates(x_center, y_center, radius, i, 0.5)
    line(x_center, y_center, x1, y1)

def inner_coordinate(outer_diameter, inner_diameter, c0):
    return (outer_diameter-inner_diameter)/2.0+c0

def radial_text(i, x_center, y_center, radius, value, alignment, degree_function):
    font("Helvetica", 12)
    fill(0)
    centered = alignment == CENTER
    offset=0.0
    x1, y1 = radial_coordinates(x_center, y_center, radius, i, offset)
    degrees = degree_function(i)
    w, h = textmetrics(value)
    cos, sin = cos_sin(i, offset)
    delta_x = w/2 if centered else 0.0
    delta_x = w/2
    delta_y = h/2
    x = x1-delta_x
    y = y1+delta_y
    rotate(degrees)
    if not centered:
        translate(delta_x, 0)
    text(value, x, y)
    if not centered:
        translate(-delta_x, 0)
    rotate(-degrees)
    
    

def draw_symbol(degrees_rotated, xc, yc, w, h, symbol):
    transform(CORNER)
    translate(xc, yc)
    dy = h / 5.0
    rotate(degrees_rotated)
    for i in range(6):
        broken = symbol[i] == ':'
        xStart = - w/2
        yStart = - h/2 + dy * i
        xEnd = xStart + w
        yEnd = yStart
        if not broken:
            line(xStart, yStart, xEnd, yEnd) 
        else:
            xA = xStart + w * 0.4
            xB = xStart + w * 0.6
            yA = yStart
            yB = yStart
            line(xStart, yStart, xA, yA) 
            line(xB, yB, xEnd, yEnd)
    rotate(-degrees_rotated)
    translate(-xc, -yc)
    transform(CENTER)
    
def draw_symbol_radially(i, x_center, y_center, radius, w, h, symbol):
    x1, y1 = radial_coordinates(x_center, y_center, radius, i, 0.0)
    angle = -rotational_degrees(i, 0.0) - 90.0
    draw_symbol(angle, x1, y1, w, h, symbol)
                
def extract_data(comma_delimited_data):
    data = [x.strip() for x in comma_delimited_data.split(',')]
    number = data[0]
    symbol = data[2]
    word = data[1]
    return number, symbol, word


class Ring:
    def __init__(self, diameter, x0, y0):
        self.diameter = diameter
        self.x0 = x0
        self.y0 = y0
        self.radius = self.diameter/2.0
        self.x_center = x0 + self.radius
        self.y_center = y0 + self.radius
        
    def ratio(self, ratio):
        return self.to_smaller(self.diameter * (1.0-ratio));
        
    def to_smaller(self, radius_difference):
        next_diameter = self.diameter - radius_difference
        next_x0 = inner_coordinate(self.diameter, next_diameter, self.x0)
        next_y0 = inner_coordinate(self.diameter, next_diameter, self.y0)
        return Ring(next_diameter, next_x0, next_y0)
        
    def draw(self):
        oval(self.x0, self.y0, self.diameter, self.diameter, True)
        
        

#### Set Global Variables
outer_ring = Ring(600.0, 20.0, 20.0)

number_ring = outer_ring.to_smaller(25.0)
inside_number = number_ring.to_smaller(25.0)

symbol_ring = inside_number.to_smaller(35.0)
inside_symbol = symbol_ring.to_smaller(30.0)

word_ring = inside_symbol.to_smaller(25.0)

center = outer_ring.ratio(0.3)

xc = outer_ring.x_center
yc = outer_ring.y_center

#### Set Base State    
colormode(RGB)
stroke(0)
nofill()
lineheight(1)

#### Draw Main Ovals
outer_ring.draw()
inside_number.draw()
inside_symbol.draw()

txt = open("/Users/dannwebster/code/iching/iching_data.csv").readlines()
    
#### Draw Wedges
i = 0
lines = open("/Users/dannwebster/code/iching/iching_data.csv").readlines()
for comma_delimited_data in lines:
    number, symbol, word = extract_data(comma_delimited_data)
    divider(xc, yc, outer_ring.radius, i)
    radial_text(i, xc, yc, number_ring.radius, number, CENTER, lambda i: -rotational_degrees(i, 0.0) - 90.0)
    # radial_text(i, xc, yc, symbol_ring.radius, symbol, CENTER, lambda i: 180-rotational_degrees(i, 0.0))
    draw_symbol_radially(i, xc, yc, symbol_ring.radius, 15, 15, symbol)
    radial_text(i, xc, yc, word_ring.radius,   word,   LEFT,   lambda i: 180-rotational_degrees(i, 0.0))
    i += 1
    
#### Draw Inner Oval
fill(1, 1, 1, 1.0)
center.draw()
