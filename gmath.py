import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    amb = calculate_ambient (light, areflect)
    diff = calculate_diffuse (light, dreflect, normal)
    spec = calculate_specular (light, sreflect, view, normal)
    return amb + diff + spec

def calculate_ambient(alight, areflect):
    r = alight[0] * areflect
    g = alight[1] * areflect
    b = alight[2] * areflect
    return limit_color ([r,g,b])

def calculate_diffuse(light, dreflect, normal):
    c = dot_product (normal, light[LOCATION])
    r = light[COLOR][0] * dreflect[0] * c[0]
    g = light[COLOR][1] * dreflect[1] * c[1]
    b = light[COLOR][2] * dreflect[2] * c[2]
    return limit_color ([r,g,b])

def calculate_specular(light, sreflect, view, normal):
    nl = dot_product (light[LOCATION], normal)
    r = (2 * normal[0] * nl - light[LOCATION][0]) * view[0]
    g = (2 * normal[1] * nl - light[LOCATION][1]) * view[1]
    b = (2 * normal[2] * nl - light[LOCATION][2]) * view[2]

    r = r ** SPECULAR_EXP
    g = g ** SPECULAR_EXP
    b = g ** SPECULAR_EXP

    r = r * light[COLOR][0] * sreflect
    g = g * light[COLOR][1] * sreflect
    b = b * light[COLOR][2] * sreflect
    return limit_color ([r,g,b])


def limit_color(color):
    if type (color) == list:
        for i in range (len (color)):
            if color[i] > 255:
                color[i] = 255
            if color[i] < 0:
                color[i] = 0
        return color
    else:
        if color > 255:
            return 255
        if color < 0:
            return 0
        else:
            return color
#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
