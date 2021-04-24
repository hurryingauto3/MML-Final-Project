import sys
import random

sys.setrecursionlimit(10**8)


class Node:

    def __init__(self, Point1, Point2, Data=None, Render=True):
        self.Top_Left_Front = Point(Point1)
        self.Bottom_Right_Back = Point(Point2)
        self.Data = Data
        self.Render = Render
        self.LeafNode = True

    def Change_Render_State(self):
        if not self.LeafNode:
            self.Render = False

    def Change_Data(self, Data):
        self.Data = Data


class Point:

    def __init__(self, x=None, y=None, z=None, faces=None):
        self.x = x
        self.y = y
        self.z = z
        self.in_faces = faces


class Octree:

    max_depth = 10
    number_of_cubes = 0

    def __init__(self, Point_1=None, Point_2=None, level=-1):
        self.level = level + 1
        Octree.number_of_cubes += 1
        self.Children = {'TLF': None, 'TRF': None, 'BRF': None, 'BLF': None, 'TLB': None, 'TRB': None,
                         'BRB': None, 'BLB': None}

        self.Top_Left_Front = None
        self.Bottom_Right_Back = None

        self.Root_Node = None
        if Point_1 == None and Point_2 == None:
            self.Root_Node = Point()

        elif Point_2 == None and Point_1 != None:
            self.Root_Node = Point_1

        elif Point_1 != None and Point_2 != None:
            self.Top_Left_Front = Point_1
            self.Bottom_Right_Back = Point_2
            # self.Children["TLF"] = Octree(Point_1)
            # self.Children["BRB"] = Octree(Point_1)

        self.Height = 0
        self.Max_Size = 0  # size to not be exceeed
        self.Total_Nodes = 1

        self.Position_Map = {
            'TLF': 0,   # top left front
            'TRF': 1,   # top right front
            'BRF': 2,   # bottom right front
            'BLF': 3,   # bottom left front
            "TLB": 4,   # top left back
            'TRB': 5,   # top right back
            'BRB': 6,   # bottom right back
            'BLB': 7    # bottom left back
        }

    def getVertices_Faces(self):
        vertices = []
        faces = []
        if self.Root_Node == None and self.Root_Node == (None, None, None):
            return vertices

        elif type(self.Root_Node) == Point:
            return [(self.Root_Node.x, self.Root_Node.y, self.Root_Node.z)], [self.Root_Node.in_faces]

        elif self.Root_Node == None and self.Top_Left_Front and self.Bottom_Right_Back:
            for key in self.Children:
                try:
                    v, f = self.Children[key].getVertices_Faces()
                    vertices += v
                    faces += f
                except:
                    pass
            return vertices, faces

    def getRegionLimits(self, Position: str) -> (Point, Point):
        if(Position == 'TLF'):
            return (self.Top_Left_Front, Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2, (self.Top_Left_Front.y + self.Bottom_Right_Back.y)/2, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2))

        elif Position == 'TLB':
            return (Point(self.Top_Left_Front.x, (self.Top_Left_Front.y + self.Bottom_Right_Back.y)/2, self.Top_Left_Front.z),
                    Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2,
                          self.Bottom_Right_Back.y, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2))

        elif Position == 'BRF':
            return (Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2, self.Top_Left_Front.y, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2),
                    Point(self.Bottom_Right_Back.x, (self.Top_Left_Front.y +
                                                     self.Bottom_Right_Back.y)/2, self.Bottom_Right_Back.z))

        elif Position == 'BLF':
            return (Point(self.Top_Left_Front.x, self.Top_Left_Front.y, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2),
                    Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2,
                          (self.Top_Left_Front.y + self.Bottom_Right_Back.y)/2, self.Bottom_Right_Back.z))

        elif Position == 'TRF':
            return (Point((self.Top_Left_Front.x+self.Bottom_Right_Back.x)/2, self.Top_Left_Front.y, self.Top_Left_Front.z), Point(self.Bottom_Right_Back.x, (self.Top_Left_Front.y + self.Bottom_Right_Back.y)/2, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2))

        elif Position == 'TRB':
            return (Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2, (self.Top_Left_Front.y + self.Bottom_Right_Back.y)/2, self.Top_Left_Front.z),
                    Point(self.Bottom_Right_Back.x, self.Bottom_Right_Back.y,
                          (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2))

        elif Position == 'BRB':
            return (Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2, (self.Top_Left_Front.y + self.Bottom_Right_Back.y)/2, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2), self.Bottom_Right_Back)

        elif Position == 'BLB':
            Point1 = Point(self.Top_Left_Front.x, (self.Top_Left_Front.y +
                                                   self.Bottom_Right_Back.y)/2, (self.Top_Left_Front.z + self.Bottom_Right_Back.z)/2)
            Point2 = Point((self.Top_Left_Front.x + self.Bottom_Right_Back.x)/2,
                           self.Bottom_Right_Back.y, self.Bottom_Right_Back.z)
            return (Point1, Point2)

    def Add(self, Point1: Point, parent=False):
       

        if parent and not check_bounds(Point1, self.Top_Left_Front, self.Bottom_Right_Back):
            # print("Not in Bounds")
            return False

        Mid_Point_x = (self.Top_Left_Front.x + self.Bottom_Right_Back.x) / 2
        Mid_Point_y = (self.Top_Left_Front.y + self.Bottom_Right_Back.y) / 2
        Mid_Point_z = (self.Top_Left_Front.z + self.Bottom_Right_Back.z) / 2

        if (Point1.x <= Mid_Point_x):
            if(Point1.y <= Mid_Point_y):
                if (Point1.z <= Mid_Point_z):
                    Position = 'BLB'
                else:
                    Position = 'TLB'
            else:
                if(Point1.z <= Mid_Point_z):
                    Position = 'BLF'
                else:
                    Position = 'TLF'
        else:
            if(Point1.y <= Mid_Point_y):
                if (Point1.z <= Mid_Point_z):
                    Position = 'BRB'
                else:
                    Position = 'TRB'
            else:
                if (Point1.z <= Mid_Point_z):
                    Position = 'BRF'
                else:
                    Position = 'TRF'

        if (self.Children[Position] != None):
            if self.Children[Position].Root_Node == None:
                self.Children[Position].Add(Point1)
            else:
                temp_point: Point = self.Children[Position].Root_Node
                self.Children[Position].Root_Node = None

                Point_TLF, Point_BRB = self.getRegionLimits(Position)

                if self.level == Octree.max_depth:
                    self.Children[Position].Root_Node = temp_point
                    return
                else:
                    self.Children[Position] = Octree(
                        Point_TLF, Point_BRB, level=self.level)
                # print(Point_TLF.x, Point_TLF.y, Point_TLF.z)
                # print(Point_BRB.x, Point_BRB.y, Point_BRB.z)
                # if(Position == 'TLF'):

                # elif Position == 'TLB':
                #     self.Children[Position] = Octree(Point(Mid_Point_x + 1, self.Top_Left_Front.y, self.Top_Left_Front.z),
                #                                      Point(self.Bottom_Right_Back.x, Mid_Point_y, Mid_Point_z))

                # elif Position == 'BRF':
                #     self.Children[Position] = Octree(Point(Mid_Point_x + 1, Mid_Point_y + 1, self.Top_Left_Front.z),
                #                                      Point(self.Bottom_Right_Back.x, self.Bottom_Right_Back.y, Mid_Point_z))

                # elif Position == 'BLF':
                #     self.Children[Position] = Octree(Point(self.Top_Left_Front.x, Mid_Point_y+1, self.Top_Left_Front.z),
                #                                      Point(Mid_Point_x, self.Bottom_Right_Back.y, Mid_Point_z))

                # elif Position == 'TLB':
                #     self.Children[Position] = Octree(Point(self.Top_Left_Front.x, self.Top_Left_Front.y, Mid_Point_z + 1),
                #                                      Point(Mid_Point_x, Mid_Point_y, self.Bottom_Right_Back.z))

                # elif Position == 'TRB':
                #     self.Children[Position] = Octree(Point(Mid_Point_x + 1, self.Top_Left_Front.y, Mid_Point_z + 1),
                #                                      Point(self.Bottom_Right_Back.x, Mid_Point_y, self.Bottom_Right_Back.z))

                # elif Position == 'BRB':
                #     self.Children[Position] = Octree(Point(Mid_Point_x + 1, Mid_Point_y+1, Mid_Point_z + 1),
                #                                      Point(self.Bottom_Right_Back.x, self.Bottom_Right_Back.y, self.Bottom_Right_Back.z))

                # elif Position == 'BLB':
                #     self.Children[Position] = Octree(Point(self.Top_Left_Front.x, Mid_Point_y+1, Mid_Point_z + 1),
                #                                      Point(Mid_Point_x, self.Bottom_Right_Back.y, self.Bottom_Right_Back.z))

                self.Children[Position].Add(temp_point)
                self.Children[Position].Add(Point1)

        elif self.Children[Position] == None:
            self.Children[Position] = Octree(Point1)

            # arrived at closest leaf node




def check_bounds(p1: Point, TLF: Point, BRB: Point):
    if ((p1.x < TLF.x or p1.x > BRB.x) or
        (p1.y > TLF.y or p1.y < BRB.y) or
            (p1.z > TLF.z or p1.z < BRB.z)):
        return False

    return True

def vertex_Sort(Lst):
      
    # Vector to store the distance
    # with respective elements
    vp = []
    p = Lst[0]
    n = len(Lst)
    # Storing the distance with its
    # distance in the vector Lstay
    for i in range(n):
          
        dist = pow((p[0] - Lst[i][0]), 2)+ pow((p[1] - Lst[i][1]), 2)+ pow((p[2] - Lst[i][2]), 2)
          
        vp.append([dist,[Lst[i][0],Lst[i][1]]])
          
    vp.sort()
    
    # Output
    out=[]
    for i in range(len(vp)):
        out.append( (vp[i][1][0],vp[i][1][1], vp[i][1][2] ))
    return out


def Vertex_Reduction(Lst,Alpha):

    for i in range(len(Lst)):



def main():

    with open("obj\\airboat.obj", "r") as file1:

        vertices = []
        faces = []

        for line in file1.readlines():
            if line[0:2] == "v ":
                line = line.split()
                v_tuple = (float(line[1]), float(line[2]), float(line[3]), [])
                vertices.append(v_tuple)
            if line[0:2] == "f ":
                face_tuple = list()
                line = line.split()
                for element in line[1:]:
                    element = element.split("/")
                    face_tuple.append(int(element[0]))
                face_tuple = tuple(face_tuple)
                for i in face_tuple:
                    vertices[i-1][3].append(len(faces))
                faces.append(face_tuple)

    m_octree = Octree(Point(-10, +10, +10),Point(+10, -+10, +-10))
    for i in vertices:
        m_octree.Add(Point(i[0], i[1], i[2], i[3]), True)
        
    vertices1, faces1 = m_octree.getVertices_Faces()
    print(len(vertices1) == len(faces1))
    face_dict = dict()
    faces = []
    for ver_in_faces in range(len(faces1)):
        for face in faces1[ver_in_faces]:
            if not face_dict.get(face):
                face_dict[face] = (ver_in_faces,)
            else:
                face_dict[face] = face_dict[face] + (ver_in_faces,)
    for key in face_dict:
        faces.append(tuple(face_dict[key]))
)

    # m_octree.Add(Point(0, 4, 4))
    # m_octree.Add(Point(4, 0, 0))
    # m_octree.Add(Point(0, 0, 4))
    # m_octree.Add(Point(0, 0, 0))
    # m_octree.Add(Point(0, 4, 0))
    # m_octree.Add(Point(4, 4, 0))
    # m_octree.Add(Point(4, 0, 4))
    # m_octree.Add(Point(4, 4, 4))
    # m_octree.Add(Point(3, 3, 1))
    # m_octree.Add(Point(1, 1, 1))
    # print(m_octree.Root_Node.x, m_octree.Root_Node.y, m_octree.Root_Node.z)
    # print(m_octree.Children)
    # print(m_octree.getVertices())
    # limit1, limit2 = m_octree.giveRegionLimits("TLF")
    # print(limit1.x, limit1.y, limit1.z)
    # print(limit2.x, limit2.y, limit2.z)


if __name__ == "__main__":
    main()
