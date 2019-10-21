import sys
from math import cos, sin, radians

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except err:
    print(f"ERROR: PyOpenGL not installed properly. {err}")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
# If true use perspective projection
# If false use orthographic projection
perspective = True
x_camera = 10  # camera's current x
y_camera = 5  # camera's current y
z_camera = 10  # camera's current z
x_axis_rotation = 0  # camera's current rotation around the x-axis in degrees
y_axis_rotation = 0  # camera's current rotation around the y-axis in degrees
z_axis_rotation = 0  # camera's current rotation around the z-axis in degrees
max_deg = 360

x_car = 15  # car's initial x
y_car = 0  # car's initial y
z_car = 15  # car's initial z
tire_distance = 2  # distance of the tire from the center of the car
z_axis_rotation_tire = 0  # rotation of the tires around z-axis


def init():
    global y_axis_rotation
    # global x_axis_rotation
    global x_camera
    global y_camera
    global z_camera
    global x_car
    global y_car
    global z_car
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    y_axis_rotation = 0
    # x_axis_rotation = 0
    x_camera = 0
    y_camera = -1
    z_camera = 0
    x_car = 15
    y_car = 0
    z_car = 15


def drawCar():
    glLineWidth(2.5)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    # Front Side
    glVertex3f(-3, 2, 2)
    glVertex3f(-2, 3, 2)
    glVertex3f(-2, 3, 2)
    glVertex3f(2, 3, 2)
    glVertex3f(2, 3, 2)
    glVertex3f(3, 2, 2)
    glVertex3f(3, 2, 2)
    glVertex3f(3, 1, 2)
    glVertex3f(3, 1, 2)
    glVertex3f(-3, 1, 2)
    glVertex3f(-3, 1, 2)
    glVertex3f(-3, 2, 2)
    # Back Side
    glVertex3f(-3, 2, -2)
    glVertex3f(-2, 3, -2)
    glVertex3f(-2, 3, -2)
    glVertex3f(2, 3, -2)
    glVertex3f(2, 3, -2)
    glVertex3f(3, 2, -2)
    glVertex3f(3, 2, -2)
    glVertex3f(3, 1, -2)
    glVertex3f(3, 1, -2)
    glVertex3f(-3, 1, -2)
    glVertex3f(-3, 1, -2)
    glVertex3f(-3, 2, -2)
    # Connectors
    glVertex3f(-3, 2, 2)
    glVertex3f(-3, 2, -2)
    glVertex3f(-2, 3, 2)
    glVertex3f(-2, 3, -2)
    glVertex3f(2, 3, 2)
    glVertex3f(2, 3, -2)
    glVertex3f(3, 2, 2)
    glVertex3f(3, 2, -2)
    glVertex3f(3, 1, 2)
    glVertex3f(3, 1, -2)
    glVertex3f(-3, 1, 2)
    glVertex3f(-3, 1, -2)
    glEnd()


def drawTire():
    glLineWidth(2.5)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    # Front Side
    glVertex3f(-1, .5, .5)
    glVertex3f(-.5, 1, .5)
    glVertex3f(-.5, 1, .5)
    glVertex3f(.5, 1, .5)
    glVertex3f(.5, 1, .5)
    glVertex3f(1, .5, .5)
    glVertex3f(1, .5, .5)
    glVertex3f(1, -.5, .5)
    glVertex3f(1, -.5, .5)
    glVertex3f(.5, -1, .5)
    glVertex3f(.5, -1, .5)
    glVertex3f(-.5, -1, .5)
    glVertex3f(-.5, -1, .5)
    glVertex3f(-1, -.5, .5)
    glVertex3f(-1, -.5, .5)
    glVertex3f(-1, .5, .5)
    # Back Side
    glVertex3f(-1, .5, -.5)
    glVertex3f(-.5, 1, -.5)
    glVertex3f(-.5, 1, -.5)
    glVertex3f(.5, 1, -.5)
    glVertex3f(.5, 1, -.5)
    glVertex3f(1, .5, -.5)
    glVertex3f(1, .5, -.5)
    glVertex3f(1, -.5, -.5)
    glVertex3f(1, -.5, -.5)
    glVertex3f(.5, -1, -.5)
    glVertex3f(.5, -1, -.5)
    glVertex3f(-.5, -1, -.5)
    glVertex3f(-.5, -1, -.5)
    glVertex3f(-1, -.5, -.5)
    glVertex3f(-1, -.5, -.5)
    glVertex3f(-1, .5, -.5)
    # Connectors
    glVertex3f(-1, .5, .5)
    glVertex3f(-1, .5, -.5)
    glVertex3f(-.5, 1, .5)
    glVertex3f(-.5, 1, -.5)
    glVertex3f(.5, 1, .5)
    glVertex3f(.5, 1, -.5)
    glVertex3f(1, .5, .5)
    glVertex3f(1, .5, -.5)
    glVertex3f(1, -.5, .5)
    glVertex3f(1, -.5, -.5)
    glVertex3f(.5, -1, .5)
    glVertex3f(.5, -1, -.5)
    glVertex3f(-.5, -1, .5)
    glVertex3f(-.5, -1, -.5)
    glVertex3f(-1, -.5, .5)
    glVertex3f(-1, -.5, -.5)
    glEnd()


def drawHouse():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    # Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    # Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    # Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    # Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    # Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()


def display():
    global perspective
    global x_car
    global z_car
    global tire_distance
    global z_axis_rotation_tire
    global x_camera
    global y_camera
    global z_camera
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    # viewing transformation

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if perspective:
        gluPerspective(100, 1, 5, 200)
    else:
        glOrtho(-10, 10, -10, 10, 1, 100)

    glMatrixMode(GL_MODELVIEW)

    glPushMatrix()
    glTranslate(-x_car, 0, z_car)
    drawCar()
    glPopMatrix()

    # Back passenger side tire
    glPushMatrix()
    glTranslate(-x_car-tire_distance, 0, z_car+tire_distance)
    glRotate(z_axis_rotation_tire, 0, 0, 1)
    drawTire()
    glPopMatrix()

    # Front passenger side tire
    glPushMatrix()
    glTranslate(-x_car+tire_distance, 0, z_car+tire_distance)
    glRotate(z_axis_rotation_tire, 0, 0, 1)
    drawTire()
    glPopMatrix()

    # Back driver side tire
    glPushMatrix()
    glTranslate(-x_car-tire_distance, 0, z_car-tire_distance)
    glRotate(z_axis_rotation_tire, 0, 0, 1)
    drawTire()
    glPopMatrix()

    # Front driver side tire
    glPushMatrix()
    glTranslate(-x_car+tire_distance, 0, z_car-tire_distance)
    glRotate(z_axis_rotation_tire, 0, 0, 1)
    drawTire()
    glPopMatrix()

    # Other houses
    glPushMatrix()

    glTranslate(0, 0, -10)
    drawHouse()

    glTranslate(-20, 0, 0)
    drawHouse()

    glTranslate(40, 0, 0)
    drawHouse()

    # Flip scene around and put houses on other side of street
    glTranslate(0, 0, 40)
    glRotate(180, 0, 1, 0)
    drawHouse()

    glTranslate(40, 0, 0)
    drawHouse()

    glTranslate(-20, 0, 0)
    drawHouse()

    # Houses on the left end of the street
    glTranslate(40, 0, 10)
    glRotate(-90, 0, 1, 0)
    drawHouse()

    glTranslate(20, 0, 0)
    drawHouse()

    glPopMatrix()

    glFlush()

# Controls tire rotation and movement of car


def timer(t):
    global x_car
    global z_axis_rotation_tire
    global max_deg

    x_car -= 0.05
    z_axis_rotation_tire -= 1.0
    z_axis_rotation_tire % max_deg

    glutPostRedisplay()
    glutTimerFunc(25, timer, 1)


def keyboard(key, x, y):
    global y_axis_rotation
    global x_camera
    global y_camera
    global z_camera
    global perspective

    if key == chr(27):
        import sys
        sys.exit(0)

    if key == b'a':
        # print("A - Moving left")
        x = cos(radians(y_axis_rotation))
        z = -sin(radians(y_axis_rotation))
        x_camera += x
        z_camera += z
        glTranslate(x, 0, z)
    elif key == b'd':
        # print("D - Moving right")
        x = -cos(radians(y_axis_rotation))
        z = sin(radians(y_axis_rotation))
        x_camera += x
        z_camera += z
        glTranslate(x, 0, z)
    elif key == b'w':
        # print("W - Moving forward")
        x = sin(radians(y_axis_rotation))
        z = cos(radians(y_axis_rotation))
        x_camera += x
        z_camera += z
        glTranslate(x, 0, z)
    elif key == b's':
        # print("S - Moving backward")
        x = -sin(radians(y_axis_rotation))
        z = -cos(radians(y_axis_rotation))
        x_camera += x
        z_camera += z
        glTranslate(x, 0, z)
    elif key == b'r':
        # print("R - Moving upward")
        glTranslate(0, -1, 0)
    elif key == b'f':
        # print("F - Moving downward")
        glTranslate(0, 1, 0)
    elif key == b'q':
        # print("Q - Turning to the left")
        y_axis_rotation += 1
        y_axis_rotation %= max_deg
        # Move to origin
        glTranslate(-x_camera, 0, -z_camera)
        # Rotate around y-axis
        glRotate(-1, 0, 1, 0)
        # Move back to original camera position
        glTranslate(x_camera, 0, z_camera)
    elif key == b'e':
        # print("E - Turning to the right")
        y_axis_rotation -= 1
        y_axis_rotation %= max_deg
        # Move to origin
        glTranslate(-x_camera, 0, -z_camera)
        # Rotate around y-axis
        glRotate(1, 0, 1, 0)
        # Move back to original camera position
        glTranslate(x_camera, 0, z_camera)
    # elif key == b'z':
    #     print("z - Look upward")
    #     y_z_rotate_deg += 1
    #     y_z_rotate_deg %= max_deg
    #     glTranslate(0, -y_d, -z_d)
    #     glRotate(1, 1, 0, 0)
    #     glTranslate(0, y_d, z_d)
    # elif key == b'c':
    #     print("c - Look downward")
    #     y_z_rotate_deg -= 1
    #     y_z_rotate_deg %= max_deg
    #     glTranslate(0, -y_d, -z_d)
    #     glRotate(1, -1, 0, 0)
    #     glTranslate(0, y_d, z_d)
    elif key == b'h':
        # print("H - Resetting")
        init()
    elif key == b'o':
        # print("O - Orthographic projection")
        perspective = False
    elif key == b'p':
        # print("P - Perspective projection")
        perspective = True

    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition(200, 200)
glutCreateWindow(b'OpenGL Lab')
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(25, timer, 1)
glutMainLoop()
