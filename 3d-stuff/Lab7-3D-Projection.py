# Import a library of functions called 'pygame'
import pygame
from math import pi, cos, sin, tan, radians, isnan
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Line3D():
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Renderer:
    def __init__(self, drawerer, canvas, view_h, view_w, near=5, far=1000, fov=90):
        self.drawerer = drawerer
        self.canvas = canvas
        self.camera_x = 0
        self.camera_y = -5
        self.camera_z = 0
        self.camera_y_rotation = 0
        self.zoom = 1 / tan(radians(fov/2))
        self.max_deg = 360

        self.house_positions = np.array(
        [[[cos(pi),0,-sin(pi),0],
          [0,1,0,0],
          [sin(pi),0,cos(pi),20],
          [0,0,0,1]],

         [[cos(pi),0,-sin(pi),15],
          [0,1,0,0],
          [sin(pi),0,cos(pi),20],
          [0,0,0,1]],

         [[cos(pi),0,-sin(pi),-15],
          [0,1,0,0],
          [sin(pi),0,cos(pi),20],
          [0,0,0,1]],

         [[1,0,0,0],
          [0,1,0,0],
          [0,0,1,-20],
          [0,0,0,1]],

         [[1,0,0,15],
          [0,1,0,0],
          [0,0,1,-20],
          [0,0,0,1]],

         [[1,0,0,-15],
          [0,1,0,0],
          [0,0,1,-20],
          [0,0,0,1]],

         [[cos(3*pi/2),0,-sin(3*pi/2),-25],
          [0,1,0,0],
          [sin(3*pi/2),0,cos(3*pi/2), 0],
          [0,0,0,1]]
        ])
        self.car_position = np.array(
        [[[1,0,0,10],
          [0,1,0,0],
          [0,0,1,-10],
          [0,0,0,1]
        ]])
        self.tire_positions = np.array([
                                           [[1,0,0,2],
                                            [0,1,0,0],
                                            [0,0,1,-2],
                                            [0,0,0,1]],

                                           [[1,0,0,-2],
                                            [0,1,0,0],
                                            [0,0,1,2],
                                            [0,0,0,1]],

                                           [[1,0,0,2],
                                            [0,1,0,0],
                                            [0,0,1,2],
                                            [0,0,0,1]],

                                           [[1,0,0,-2],
                                            [0,1,0,0],
                                            [0,0,1,-2],
                                            [0,0,0,1]]
        ])
        self.clip_matrix = np.array(
        [[self.zoom, 0, 0, 0],
         [0, self.zoom, 0, 0],
         [0, 0, (far+near)/(far-near), (-2*far*near)/(far-near)],
         [0, 0, 1, 0]
        ])

        self.viewport_matrix = np.array(
        [[view_h/2, 0, view_h/2],
         [0, -view_w/2, view_w/2],
         [0,0,1],
        ])

        self.house_def = loadHouse()
        self.car_def = loadCar()
        self.tire_def = loadTire()
        self.house = self.make_homogenous(self.house_def)
        self.car = self.make_homogenous(self.car_def)
        self.tire = self.make_homogenous(self.tire_def)

    def draw(self):
        self.drawHouse()
        self.drawCar()
    
    def drawHouse(self):
        world = self.to_world(self.house, self.house_positions)
        camera = self.to_camera(world)
        clip = self.clip(camera)
        normalized = self.homogenous_divide(clip)
        view = self.to_viewport(normalized)
        for l in view:
            self.drawerer.draw.line(self.canvas, RED, (l.start[0], l.start[1]), (l.end[0], l.end[1]))

    def drawCar(self):
        world = self.to_world(self.car, self.car_position)
        camera = self.to_camera(world)
        clip = self.clip(camera)
        normalized = self.homogenous_divide(clip)
        view = self.to_viewport(normalized)
        for l in view:
            self.drawerer.draw.line(self.canvas, GREEN, (l.start[0], l.start[1]), (l.end[0], l.end[1]))

        self.drawTires()

    def drawTires(self):
        tires = []
        for t in self.tire_positions:
            tires.append(t.dot(self.car_position))
            
        world = self.to_world(self.tire, tires)
        camera = self.to_camera(world)
        clip = self.clip(camera)
        normalized = self.homogenous_divide(clip)
        view = self.to_viewport(normalized)

        for l in view:
            self.drawerer.draw.line(self.canvas, BLUE, (l.start[0], l.start[1]), (l.end[0], l.end[1]))

    def reset(self):
        self.house = self.make_homogenous(self.house_def)
        self.car = self.make_homogenous(self.car_def)
        self.tire = self.make_homogenous(self.tire_def)
        self.camera_x = 0
        self.camera_y = -5
        self.camera_z = 0
        self.camera_y_rotation = 0

    def to_world(self, model, transform):
        lines = []
        for t in transform:
            for l in model:
                v1 = t.dot(l.start)
                v2 = t.dot(l.end)
                lines.append(Line3D(v1, v2))
        
        return lines

    def to_camera(self, model):
        camera_transform = np.array(
        [[1,0,0,self.camera_x],
         [0,1,0,self.camera_y],
         [0,0,1,self.camera_z],
         [0,0,0,1]
        ])
        camera_rotation = np.array(
        [[cos(radians(self.camera_y_rotation)),0,-sin(radians(self.camera_y_rotation)),0],
         [0,1,0,0],
         [sin(radians(self.camera_y_rotation)),0,cos(radians(self.camera_y_rotation)),0],
         [0,0,0,1]
        ])

        lines = []
        for l in model:
            v1 = camera_rotation.dot(camera_transform.dot(l.start))
            v2 = camera_rotation.dot(camera_transform.dot(l.end))
            lines.append(Line3D(v1, v2))

        return lines
            
    def clip(self, model):
        lines = []
        for l in model:
            v1 = self.clip_matrix.dot(l.start)
            v2 = self.clip_matrix.dot(l.end)
            x1 = v1[0]
            y1 = v1[1]
            z1 = v1[2]
            x2 = v2[0]
            y2 = v2[1]
            z2 = v2[2]
            w1 = v1[3]
            w2 = v2[3]
            if not ((x1 < -w1 and x2 < -w2) or 
                    (y1 < -w1 and y2 < -w2) or 
                    (z1 < -w1 or z2 < -w2) or 
                    (x1 > w1 and x2 > w2) or 
                    (y1 > w1 and y2 > w2) or 
                    (z1 > w1 and z2 > w2)):

                    lines.append(Line3D(v1, v2))
        return lines

    def homogenous_divide(self, model):
        lines = []
        for l in model:
            v1 = l.start/l.start[3]
            v2 = l.end/l.end[3]
            lines.append(Line3D(
                [v1[0], v1[1], 1], 
                [v2[0], v2[1], 1]
            ))
        return lines

    def to_viewport(self, model):
        lines = []
        for l in model:
            v1 = self.viewport_matrix.dot(l.start)
            v2 = self.viewport_matrix.dot(l.end)
            lines.append(Line3D(
                [v1[0], v1[1]],
                [v2[0], v2[1]]
            ))

        return lines

    def make_homogenous(self, model):
        lines = []
        for l in model:
            lines.append(Line3D([l.start.x, l.start.y, l.start.z, 1], [l.end.x, l.end.y, l.end.z, 1]))

        return lines
    
    def turn_right(self, amount):
        self.camera_y_rotation += amount
        self.camera_y_rotation % self.max_deg

    def turn_left(self, amount):
        self.camera_y_rotation -= amount
        self.camera_y_rotation % self.max_deg

    def move_up(self, amount):
        self.camera_y -= amount

    def move_down(self, amount):
        self.camera_y += amount

    def move_left(self):
        self.camera_x += cos(radians(self.camera_y_rotation))
        self.camera_z += -sin(radians(self.camera_y_rotation))

    def move_right(self):
        self.camera_x += -cos(radians(self.camera_y_rotation))
        self.camera_z += sin(radians(self.camera_y_rotation))

    def move_forward(self):
        self.camera_x += -sin(radians(self.camera_y_rotation))
        self.camera_z += -cos(radians(self.camera_y_rotation))

    def move_backward(self):
        self.camera_x += sin(radians(self.camera_y_rotation))
        self.camera_z += cos(radians(self.camera_y_rotation))

def loadOBJ(filename):
    vertices = []
    indices = []
    lines = []
    f = open(filename, "r")
    for line in f:
        t = str.split(line)
        if not t:
            continue
        if t[0] == "v":
            vertices.append(Point3D(float(t[1]), float(t[2]), float(t[3])))
        if t[0] == "f":
            for i in range(1, len(t) - 1):
                index1 = int(str.split(t[i], "/")[0])
                index2 = int(str.split(t[i+1], "/")[0])
                indices.append((index1, index2))
    f.close()

    # Add faces as lines
    for index_pair in indices:
        index1 = index_pair[0]
        index2 = index_pair[1]
        lines.append(Line3D(vertices[index1 - 1], vertices[index2 - 1]))

    # Find duplicates
    duplicates = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]
            # Case 1 -> Starts match
            if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
                if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
                    duplicates.append(j)
            # Case 2 -> Start matches end
            if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
                if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
                    duplicates.append(j)

    duplicates = list(set(duplicates))
    duplicates.sort()
    duplicates = duplicates[::-1]

    # Remove duplicates
    for j in range(len(duplicates)):
        del lines[duplicates[j]]

    return lines


def loadHouse():
    house = []
    # Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    # Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    # Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    # Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    # Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
    return house


def loadCar():
    car = []
    # Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))
    # Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    # Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))
    return car


def loadTire():
    tire = []
    # Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))
    # Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))
    # Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    return tire


# Initialize the game engine
pygame.init()
# Define the colors we will use in RGB format
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shape Drawing")
# Set needed variables
done = False
clock = pygame.time.Clock()
renderer = Renderer(pygame, screen, size[0], size[1])

# Loop until the user clicks the close button.
while not done:
    # This limits the while loop to a max of 100 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(100)
    # Clear the screen and set the screen background
    screen.fill(BLACK)
    #Controller Code#
    #####################################################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a]:
        # print("move left")
        renderer.move_left()

    if pressed[pygame.K_d]:
        # print("move right")
        renderer.move_right()

    if pressed[pygame.K_w]:
        # print("move forward")
        renderer.move_forward()

    if pressed[pygame.K_s]:
        # print("move backward")
        renderer.move_backward()

    if pressed[pygame.K_q]:
        # print("turn left")
        renderer.turn_left(1)

    if pressed[pygame.K_e]:
        # print("turn right")
        renderer.turn_right(1)

    if pressed[pygame.K_r]:
        # print("move upward")
        renderer.move_up(1)

    if pressed[pygame.K_f]:
        # print("move downward")
        renderer.move_down(1)

    if pressed[pygame.K_h]:
        # print("resetting")
        renderer.reset()

    #Redraw the updates#
    #####################################################################
    renderer.draw()

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
# Be IDLE friendly
pygame.quit()
