import pygame
from math import *
import Main

# Colors definitions
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

# Coordinate Constants
X = 0
Y = 1
Z = 2

# Matrices
projection_matrix = [[1,0,0],[0,1,0],[0,0,0]]

# Rendering Settings
render_edges = True
render_corners = True
render_centers = True

Window_x = Main.Window_x
Window_y = Main.Window_y

scale = 100


# Matrix values for the centers of each face in a cube
face_centers = [n for n in range(6)]
face_centers[0] = [[0],[-1],[0]] # Top
face_centers[1] = [[0],[0],[-1]] # Front
face_centers[2] = [[-1],[0],[0]] # Left
face_centers[3] = [[0],[1],[0]] # Bottom
face_centers[4] = [[0],[0],[1]] # Back
face_centers[5] = [[1],[0],[0]] # Right

# Corner of a cube. Is a smaller cube defined by 8 points, 3 colors, and its location on the cube. 
class Corner:

    def __init__(self, colors, index):
        self.colors = colors
        corner_points = [n for n in range(8)]
        corner_points[0] = [[-1],[-1],[1]]
        corner_points[1] = [[1],[-1],[1]]
        corner_points[2] = [[1],[-1],[-1]]
        corner_points[3] = [[-1],[-1],[-1]]
        corner_points[4] = [[-1],[1],[-1]]
        corner_points[5] = [[1],[1],[-1]]
        corner_points[6] = [[1],[1],[1]]
        corner_points[7] = [[-1],[1],[1]]
        self.points = corner_points
        self.index = index
        self.orientation = 0
        return
    
    def set_index(self, num):
        self.index = num
    
    def set_orientation(self, num):
        self.orientation = num

# Edge of a cube. Also defined by 8 points, but has only 2 colors. Also contains location on the cube.
class Edge:
    def __init__(self, colors, index):
        self.colors = colors
        edge_points = [n for n in range(8)]
        edge_points[0] = [[-1],[-1],[1]]
        edge_points[1] = [[1],[-1],[1]]
        edge_points[2] = [[1],[-1],[-1]]
        edge_points[3] = [[-1],[-1],[-1]]
        edge_points[4] = [[-1],[1],[-1]]
        edge_points[5] = [[1],[1],[-1]]
        edge_points[6] = [[1],[1],[1]]
        edge_points[7] = [[-1],[1],[1]]
        self.points = edge_points
        self.index = index
        self.orientation = 0
        return
    
    def set_index(self, num):
        self.index = num
    
    def set_orientation(self, num):
        self.orientation = num

# Center piece on the cube with 1 color and a fixed location on the cube.
class Center:
    def __init__(self, color, location):
        center_points = [n for n in range(8)]
        center_points[0] = [[-1],[-1],[1]]
        center_points[1] = [[1],[-1],[1]]
        center_points[2] = [[1],[-1],[-1]]
        center_points[3] = [[-1],[-1],[-1]]
        center_points[4] = [[-1],[1],[-1]]
        center_points[5] = [[1],[1],[-1]]
        center_points[6] = [[1],[1],[1]]
        center_points[7] = [[-1],[1],[1]]
        self.center_points = center_points
        self.color = color
        self.location = location

# A cube contains 8 corners, 12 edges, and 6 centers. 
class Cube:
    def __init__(self, window):
        self.window = window
        self.centers = [WHITE, RED, GREEN, ORANGE, BLUE, YELLOW]
        corners = [n for n in range(8)]
        # Top/Bottom, Front/Back, Left/Right
        corners[0] = Corner([WHITE,BLUE,ORANGE], 0)
        corners[1] = Corner([WHITE,RED,BLUE], 1)
        corners[2] = Corner([WHITE,GREEN,RED], 2)
        corners[3] = Corner([WHITE,ORANGE,GREEN], 3)
        corners[4] = Corner([YELLOW,GREEN,ORANGE], 4)
        corners[5] = Corner([YELLOW,RED,GREEN], 5)
        corners[6] = Corner([YELLOW,BLUE,RED], 6)
        corners[7] = Corner([YELLOW,ORANGE,BLUE], 7)
        corner_points = [n for n in range(8)]
        corner_points[0] = [[-1],[-1],[1]]
        corner_points[1] = [[1],[-1],[1]]
        corner_points[2] = [[1],[-1],[-1]]
        corner_points[3] = [[-1],[-1],[-1]]
        corner_points[4] = [[-1],[1],[-1]]
        corner_points[5] = [[1],[1],[-1]]
        corner_points[6] = [[1],[1],[1]]
        corner_points[7] = [[-1],[1],[1]]
        self.corner_points = corner_points
        self.corners = corners

        edges = [n for n in range(12)]
        edges[0] = Edge([WHITE,BLUE], 0)
        edges[1] = Edge([WHITE,RED], 1)
        edges[2] = Edge([WHITE,GREEN], 2)
        edges[3] = Edge([WHITE,ORANGE], 3)
        edges[4] = Edge([BLUE, ORANGE], 4)
        edges[5] = Edge([BLUE, RED], 5)
        edges[6] = Edge([GREEN, RED], 6)
        edges[7] = Edge([GREEN, ORANGE], 7)
        edges[8] = Edge([YELLOW, GREEN], 8)
        edges[9] = Edge([YELLOW, RED], 9)
        edges[10] = Edge([YELLOW, BLUE], 10)
        edges[11] = Edge([YELLOW, ORANGE], 11)
        self.edges = edges
        self.edge_position = [[[0],[-1],[1]], #0
                            [[1],[-1],[0]], #1
                            [[0],[-1],[-1]], #2
                            [[-1],[-1],[0]], #3
                            [[-1],[0],[1]], #4
                            [[1],[0],[1]], #5
                            [[1],[0],[-1]], #6
                            [[-1],[0],[-1]], #7
                            [[0],[1],[-1]], #8
                            [[1],[1],[0]], #9
                            [[0],[1],[1]], #10
                            [[-1],[1],[0]]] #11
        
        self.centers = [Center(WHITE, [[0],[-1],[0]]),
                        Center(GREEN, [[0],[0],[-1]]),
                        Center(ORANGE, [[-1],[0],[0]]),
                        Center(YELLOW, [[0],[1],[0]]),
                        Center(BLUE, [[0],[0],[1]]),
                        Center(RED, [[1],[0],[0]]),]
        self.center_points = [[[0],[-1],[0]],
                              [[0],[0],[-1]],
                              [[-1],[0],[0]],
                              [[0],[1],[0]],
                              [[0],[0],[1]],
                              [[1],[0],[0]]]
    
    # Stores each corners's position relative to the screen. Returns a list of each corner, its position, and its depth (the z axis)
    def get_corner_positions(self, rotation_x, rotation_y, rotation_z):
        points = [0 for _ in range(len(self.corner_points))]
        i = 0
        for point in self.corner_points:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            point_2d = multiply_m(projection_matrix,rotate_z)
            
            x = (point_2d[0][0]*scale) + Window_x/2
            y = (point_2d[1][0]*scale) + Window_y/2
            
            # Find the correct piece
            for corner in self.corners:
                if corner.index == i:
                    points[i] = [corner, [x,y,rotate_z[2][0]]]
                    break
            
            i += 1
        return points
    
    # Stores each edge's position relative to the screen. Returns a list of each edge, its position, and its depth (the z axis)
    def get_edge_positions(self, rotation_x, rotation_y, rotation_z):
        points = [0 for _ in range(len(self.edges))]
        i = 0
        for point in self.edge_position:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            point_2d = multiply_m(projection_matrix,rotate_z)
            
            x = (point_2d[0][0]*scale) + Window_x/2
            y = (point_2d[1][0]*scale) + Window_y/2
            
            # Find the correct piece
            for edge in self.edges:
                if edge.index == i:
                    points[i] = [edge, [x,y,rotate_z[2][0]]]
                    break
            i += 1
        return points
    
     # Stores each center's position relative to the screen. Returns a list of each center, its position, and its depth (the z axis)
    def get_center_positions(self, rotation_x, rotation_y, rotation_z):
        points = [0 for _ in range(len(self.centers))]
        i = 0
        for center in self.center_points:
            rotate_x = multiply_m(rotation_x,center)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            point_2d = multiply_m(projection_matrix,rotate_z)
            
            x = (point_2d[0][0]*scale) + Window_x/2
            y = (point_2d[1][0]*scale) + Window_y/2
            
            points[i] = [self.centers[i], [x,y,rotate_z[2][0]]]
            i += 1
        return points
    
    # Renders a corner. Determines which faces on the corner should be displaying colors and draws those colors on the screen.
    def RenderCorner(self, x, y, corner, rotation_x, rotation_y, rotation_z, local_scale):
        points = [0 for _ in range(len(self.corner_points))]
        face_points = [0 for _ in range(len(face_centers))]
        i = 0
        for point in corner.points:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            point_2d = multiply_m(projection_matrix,rotate_z)
            
            local_x = (point_2d[0][0]*local_scale)
            local_y = (point_2d[1][0]*local_scale)
            
            points[i] = (local_x + x,local_y + y)
            i += 1
        i = 0
        for point in face_centers:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            
            face_points[i] = rotate_z[2][0]
            i += 1
        
        # Determine which sides are showing
        showing = [0 for _ in range(3)]
        # Top/Bottom
        showing[1] = 0 if self.corner_points[corner.index][Y][0] < 0 else 3
        # Front/Back
        showing[2] = 1 if self.corner_points[corner.index][Z][0] < 0 else 4
        # Left/Right
        showing[0] = 2 if self.corner_points[corner.index][X][0] < 0 else 5
        # Determine the drawing order for the showing sides
        showing.sort(reverse=True, key=lambda e: face_points[e])
        orientation_offset = corner.orientation
        for i in showing:
            if i == 0: # Top
                draw_face(self.window, corner.colors[orientation_offset],[points[0], points[1], points[2], points[3]])
            elif i == 1: # Front
                color = 1 if self.corner_points[corner.index][X][0] + self.corner_points[corner.index][Y][0] == 0 else 2
                color = (orientation_offset + color) % 3
                draw_face(self.window, corner.colors[color],[points[3], points[2], points[5], points[4]])
            elif i == 2: # Left
                color = 1 if self.corner_points[corner.index][Y][0] + self.corner_points[corner.index][Z][0] != 0 else 2
                color = (orientation_offset + color) % 3
                draw_face(self.window, corner.colors[color],[points[0], points[3], points[4], points[7]])
            elif i == 3: # Bottom
                draw_face(self.window, corner.colors[orientation_offset],[points[4], points[5], points[6], points[7]])
                pass
            elif i == 4: # Back
                color = 1 if self.corner_points[corner.index][X][0] + self.corner_points[corner.index][Y][0] != 0 else 2
                color = (orientation_offset + color) % 3
                draw_face(self.window, corner.colors[color],[points[1], points[0], points[7], points[6]])
            else: # Right
                color = 1 if self.corner_points[corner.index][Y][0] + self.corner_points[corner.index][Z][0] == 0 else 2
                color = (orientation_offset + color) % 3
                draw_face(self.window, corner.colors[color],[points[1], points[2], points[5], points[6]])
        return
    
    # Renders an edge. Determines which faces on the edge should be showing colors and draws those colors on the screen.
    def RenderEdge(self, x, y, edge, rotation_x, rotation_y, rotation_z, local_scale):
        points = [0 for _ in range(len(self.edge_position))]
        face_points = [0 for _ in range(len(face_centers))]
        i = 0
        for point in edge.points:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            point_2d = multiply_m(projection_matrix,rotate_z)
            
            local_x = (point_2d[0][0]*local_scale)
            local_y = (point_2d[1][0]*local_scale)
            
            points[i] = (local_x + x,local_y + y)
            i += 1
        i = 0
        for point in face_centers:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            
            face_points[i] = rotate_z[2][0]
            i += 1
        # Determine which sides are showing
        showing = [0,0]
        if self.edge_position[edge.index][1][0] != 0: 
            showing[0] = 0 if self.edge_position[edge.index][1][0] < 0 else 3
            if self.edge_position[edge.index][0][0] != 0:
                showing[1] = 2 if self.edge_position[edge.index][0][0] < 0 else 5
            else:
                showing[1] = 1 if self.edge_position[edge.index][2][0] < 0 else 4
        else:
            showing[0] = 1 if self.edge_position[edge.index][2][0] < 0 else 4
            showing[1] = 2 if self.edge_position[edge.index][0][0] < 0 else 5
        
        orientation = edge.orientation
        showing.sort(reverse=True, key=lambda e: face_points[e])
        for i in showing:
            if i == 0: # Top
                draw_face(self.window, edge.colors[orientation],[points[0], points[1], points[2], points[3]])
            elif i == 1: # Front
                # Determines if this edge is a pole or not (only needed for front and back faces)
                color = 0 if self.edge_position[edge.index][1][0] == 0 else 1
                color = (color + orientation) % 2
                draw_face(self.window, edge.colors[color],[points[3], points[2], points[5], points[4]])
            elif i == 2: # Left
                draw_face(self.window, edge.colors[(orientation + 1) % 2],[points[0], points[3], points[4], points[7]])
            elif i == 3: # Bottom
                draw_face(self.window, edge.colors[orientation],[points[4], points[5], points[6], points[7]])
                pass
            elif i == 4: # Back
                color = 0 if self.edge_position[edge.index][1][0] == 0 else 1
                color = (color + orientation) % 2
                draw_face(self.window, edge.colors[color],[points[1], points[0], points[7], points[6]])
            else: # Right
                draw_face(self.window, edge.colors[(orientation + 1) % 2],[points[1], points[2], points[5], points[6]])
        
        return

    # Renders a center. Determines which face on the center should be displaying and draws the color on the screen.
    def RenderCenter(self, x, y, center, rotation_x, rotation_y, rotation_z, local_scale):
        points = [0 for _ in range(len(center.center_points))]
        location = center.location
        i = 0
        for point in center.center_points:
            rotate_x = multiply_m(rotation_x,point)
            rotate_y = multiply_m(rotation_y,rotate_x)
            rotate_z = multiply_m(rotation_z,rotate_y)
            point_2d = multiply_m(projection_matrix,rotate_z)
            
            local_x = (point_2d[0][0]*local_scale)
            local_y = (point_2d[1][0]*local_scale)
            
            points[i] = (local_x + x,local_y + y)
            i += 1
        if location[1][0] == -1: # Top
            draw_face(self.window, center.color,[points[0], points[1], points[2], points[3]])
        elif location[1][0] == 1: # Bottom
            draw_face(self.window, center.color,[points[4], points[5], points[6], points[7]])
        elif location[2][0] == -1: # Front
            draw_face(self.window, center.color,[points[3], points[2], points[5], points[4]])
        elif location[2][0] == 1: # Back
            draw_face(self.window, center.color,[points[1], points[0], points[7], points[6]])
        elif location[0][0] == -1: # Left
            draw_face(self.window, center.color,[points[0], points[3], points[4], points[7]])
        else: # Right
            draw_face(self.window, center.color,[points[1], points[2], points[5], points[6]])
    
    # Collects all piece locations and draws them. Further pieces are drawn first to create depth.
    def RenderCube(self, rotation_x, rotation_y, rotation_z):
        # Obtain all piece locations
        pieces = []
        for corner in self.get_corner_positions(rotation_x, rotation_y, rotation_z):
            pieces.append(corner)
        for edge in self.get_edge_positions(rotation_x, rotation_y, rotation_z):
            pieces.append(edge)
        for center in self.get_center_positions(rotation_x, rotation_y, rotation_z):
            pieces.append(center)
        # Sort pieces by their depth, furthest pieces first
        pieces.sort(reverse=True, key=getZ)

        # Render each piece as they occur.
        for i in range(len(pieces)):
            x = pieces[i][1][0]
            y = pieces[i][1][1]

            # Determine if a piece is a corner, edge, or center.
            # Only draws piece if the setting is enabled
            if isinstance(pieces[i][0], Corner):
                if render_corners:
                    self.RenderCorner(x,y,pieces[i][0], rotation_x, rotation_y, rotation_z, 50)
                else:
                    pygame.draw.circle(self.window, RED, (x,y), 5)
            elif isinstance(pieces[i][0], Edge):
                if render_edges:
                    self.RenderEdge(x,y,pieces[i][0], rotation_x, rotation_y, rotation_z, 50)
                else:
                    pygame.draw.circle(self.window, GREEN, (x,y), 5)
            else:
                if render_centers:
                    self.RenderCenter(x,y,pieces[i][0], rotation_x, rotation_y, rotation_z, 50)
                else:
                    pygame.draw.circle(self.window, WHITE, (x,y), 5)
        return
    
    def set_state(self, new_cube):
        for n in range(len(new_cube.cornerPermutation)):
            self.corners[new_cube.cornerPermutation[n]].index = n
            self.corners[new_cube.cornerPermutation[n]].orientation = new_cube.cornerOrientation[n]
        for m in range(len(new_cube.edgePermutation)):
            self.edges[new_cube.edgePermutation[m]].index = m
            self.edges[new_cube.edgePermutation[m]].orientation = new_cube.edgeOrientation[m]

# Given info regarding a piece, return it's z axis value.
def getZ(coordPacket):
    return coordPacket[1][2]

def multiply_m(a,b):
    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])
    # Dot product matrix dimentions = a_rows x b_cols
    product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print("Incompatible Matrix Size")
    return product

def draw_face(window, color, points, cube):
    coords = []
    for point in points:
        coords.append((cube[point][0], cube[point][1]))
    pygame.draw.polygon(window, color, coords)
    pygame.draw.polygon(window, (0,0,0), coords, 1)

def draw_face(window, color, points):
    pygame.draw.polygon(window, color, points)
    pygame.draw.polygon(window, (0,0,0), points, 1)

    