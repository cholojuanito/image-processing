""" Modified code from Peter Colling Ridge 
	Original found at http://www.petercollingridge.co.uk/pygame-3d-graphics-tutorial
"""

import pygame
import numpy as np
import wireframe as wf
import basicShapes as shape
from math import pi


class WireframeViewer(wf.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """

    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)

        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []

        self.displayNodes = False
        self.displayEdges = True
        self.displayFaces = True

        self.perspective = False
        self.eyeX = self.width/2
        self.eyeY = 100
        self.light_color = np.array([1, 1, 1])
        self.view_vector = np.array([0, 0, -1])
        self.light_vector = np.array([0, 0, -1])

        self.background = (10, 10, 50)
        self.nodeColour = (250, 250, 250)
        self.nodeRadius = 4

        self.control = 0
        self.m_gloss = 10
        # The following three coeffecients must add up to 1.0
        self.m_diff = 0.4
        self.m_spec = 0.5
        self.m_amb = 0.1

    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250, 250, 250)

    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)

    def display(self):
        self.screen.fill(self.background)

        for name, wireframe in self.wireframes.items():
            nodes = wireframe.nodes

            if self.displayFaces:
                for (face, color) in wireframe.sortedFaces():
                    v1 = (nodes[face[1]] - nodes[face[0]])[:3]
                    v2 = (nodes[face[2]] - nodes[face[0]])[:3]

                    normal = np.cross(v1, v2)
                    normal /= np.linalg.norm(normal)
                    towards_us = normal.dot(self.view_vector)

                    # Only draw faces that face us
                    if towards_us > 0:
                        amb = self.light_color * (self.m_amb * color)
                        # Assume the face is in shadow
                        diff = np.array([0.0, 0.0, 0.0])
                        spec = np.array([0.0, 0.0, 0.0])

                        if (normal.dot(self.light_vector) > 0):
                            # Face normal is not in shadow
                            reflect_vector = 2 * \
                                (self.light_vector.dot(normal)) * \
                                normal - self.light_vector
                            diff = self.light_color * \
                                (self.m_diff * color) * \
                                normal.dot(self.light_vector)
                            spec = self.light_color * \
                                (self.m_spec * color) * \
                                self.view_vector.dot(
                                    reflect_vector) ** self.m_gloss

                        light_total = np.add(amb, diff)
                        light_total = np.clip(
                            np.add(light_total, diff), 0, 255)

                        pygame.draw.polygon(self.screen, light_total, [
                                            (nodes[node][0], nodes[node][1]) for node in face], 0)

                if self.displayEdges:
                    for (n1, n2) in wireframe.edges:
                        if self.perspective:
                            if wireframe.nodes[n1][2] > -self.perspective and nodes[n2][2] > -self.perspective:
                                z1 = self.perspective / \
                                    (self.perspective + nodes[n1][2])
                                x1 = self.width/2 + z1 * \
                                    (nodes[n1][0] - self.width/2)
                                y1 = self.height/2 + z1 * \
                                    (nodes[n1][1] - self.height/2)

                                z2 = self.perspective / \
                                    (self.perspective + nodes[n2][2])
                                x2 = self.width/2 + z2 * \
                                    (nodes[n2][0] - self.width/2)
                                y2 = self.height/2 + z2 * \
                                    (nodes[n2][1] - self.height/2)

                                pygame.draw.aaline(
                                    self.screen, color, (x1, y1), (x2, y2), 1)
                        else:
                            pygame.draw.aaline(
                                self.screen, color, (nodes[n1][0], nodes[n1][1]), (nodes[n2][0], nodes[n2][1]), 1)

            if self.displayNodes:
                for node in nodes:
                    pygame.draw.circle(self.screen, color, (int(
                        node[0]), int(node[1])), self.nodeRadius, 0)

        pygame.display.flip()

    def keyEvent(self, key):
        if key == pygame.K_a:
            # print("a is pressed")
            temp = self.light_vector
            temp = np.insert(temp, 3, 1)
            self.light_vector = np.dot(temp, wf.rotateYMatrix(-pi/16))[:-1]
        if key == pygame.K_d:
            # print("d is pressed")
            temp = self.light_vector
            temp = np.insert(temp, 3, 1)
            self.light_vector = np.dot(temp, wf.rotateYMatrix(pi/16))[:-1]
        if key == pygame.K_w:
            # print("w is pressed")
            temp = self.light_vector
            temp = np.insert(temp, 3, 1)
            self.light_vector = np.dot(temp, wf.rotateXMatrix(pi/16))[:-1]
        if key == pygame.K_s:
            # print("s is pressed")
            temp = self.light_vector
            temp = np.insert(temp, 3, 1)
            self.light_vector = np.dot(temp, wf.rotateXMatrix(-pi/16))[:-1]
        if key == pygame.K_q:
            # print("q is pressed")
            temp = self.light_vector
            temp = np.insert(temp, 3, 1)
            self.light_vector = np.dot(temp, wf.rotateZMatrix(pi/16))[:-1]
        if key == pygame.K_e:
            # print("e is pressed")
            temp = self.light_vector
            temp = np.insert(temp, 3, 1)
            self.light_vector = np.dot(temp, wf.rotateZMatrix(-pi/16))[:-1]
        return

    def run(self):
        """ Display wireframe on screen and respond to keydown events """

        running = True
        key_down = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_down = event.key
                elif event.type == pygame.KEYUP:
                    key_down = None

            if key_down:
                self.keyEvent(key_down)

            self.display()
            self.update()

        pygame.quit()


resolution = 52
viewer = WireframeViewer(600, 400)
viewer.addWireframe('sphere', shape.Spheroid(
    (300, 200, 20), (160, 160, 160), resolution=resolution))

# Colour ball
faces = viewer.wireframes['sphere'].faces
for i in range(int(resolution/4)):
    for j in range(resolution*2-4):
        f = i*(resolution*4-8) + j
        faces[f][1][1] = 0
        faces[f][1][2] = 0

viewer.displayEdges = False
viewer.run()
