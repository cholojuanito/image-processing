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
x_d = 0
y_d = 0
z_d = 0
x_y_rotate_deg = 0
x_z_rotate_deg = 0
y_z_rotate_deg = 0
max_deg = 360


def init():
    global x_z_rotate_deg
    global y_z_rotate_deg
    global x_d
    global y_d
    global z_d
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x_z_rotate_deg = 0
    y_z_rotate_deg = 0
    x_d = 0
    y_d = 0
    z_d = 0


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
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    # viewing transformation

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if perspective:
        gluPerspective(100, 1, 1, 100)
    else:
        glOrtho(-10, 10, -10, 10, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    drawHouse()

    glFlush()


def keyboard(key, x, y):
    global x_z_rotate_deg
    global y_z_rotate_deg
    global x_d
    global y_d
    global z_d
    global perspective

    if key == chr(27):
        import sys
        sys.exit(0)

    if key == b'a':
        # print("A - Moving left")
        x = cos(radians(x_z_rotate_deg))
        z = -sin(radians(x_z_rotate_deg))
        x_d += x
        z_d += z
        glTranslate(x, 0, z)
    elif key == b'd':
        # print("D - Moving right")
        x = -cos(radians(x_z_rotate_deg))
        z = sin(radians(x_z_rotate_deg))
        x_d += x
        z_d += z
        glTranslate(x, 0, z)
    elif key == b'w':
        # print("W - Moving forward")
        x = sin(radians(x_z_rotate_deg))
        z = cos(radians(x_z_rotate_deg))
        x_d += x
        z_d += z
        glTranslate(x, 0, z)
    elif key == b's':
        # print("S - Moving backward")
        x = -sin(radians(x_z_rotate_deg))
        z = -cos(radians(x_z_rotate_deg))
        x_d += x
        z_d += z
        glTranslate(x, 0, z)
    elif key == b'r':
        # print("R - Moving upward")
        glTranslate(0, -1, 0)
    elif key == b'f':
        # print("F - Moving downward")
        glTranslate(0, 1, 0)
    elif key == b'q':
        # print("Q - Turning to the left")
        x_z_rotate_deg += 1
        x_z_rotate_deg %= max_deg
        # Move to origin
        glTranslate(-x_d, 0, -z_d)
        # Rotate around y-axis
        glRotate(-1, 0, 1, 0)
        # Move back to original camera position
        glTranslate(x_d, 0, z_d)
    elif key == b'e':
        # print("E - Turning to the right")
        x_z_rotate_deg -= 1
        x_z_rotate_deg %= max_deg
        # Move to origin
        glTranslate(-x_d, 0, -z_d)
        # Rotate around y-axis
        glRotate(1, 0, 1, 0)
        # Move back to original camera position
        glTranslate(x_d, 0, z_d)
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
glutInitWindowPosition(100, 100)
glutCreateWindow(b'OpenGL Lab')
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
