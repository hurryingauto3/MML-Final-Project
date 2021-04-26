import sys
import random
import bpy

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


def Vertex_Reduction(Lst,Alpha,N):

    for j in range(N): 
        for i in range(len(Lst),1,-1):
            if pow(Lst[i][0]-Lst[i-1][0] , 2) + pow(Lst[i][1]-Lst[i-1][1] , 2) + pow(Lst[i][2]-Lst[i-1][2] , 2) <= Alpha:
                Lst.pop(i)
    return Lst

        
def point_cloud(ob_name, coords, faces=[], edges=[]):
    """Create point cloud object based on given coordinates and name.

    Keyword arguments:
    ob_name -- new object name
    coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]
    """

    # Create new mesh and a new object
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    # Make a mesh from a list of vertices/edges/faces
    me.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    ob.show_name = True
    me.update()
    return ob

def Partition(Lst,axis):
    if axis == "x":
        part = 1 
    elif axis == "y"
        part = 2
    else:
        part = 3
    Layer_Dict = {}
    for i in range(len(Lst)):
        if str(math.ciel(Lst[i][part]) +"-"+str(math.floor(math.ciel(Lst[i][part]))) not in Layer_Dict: # e.g if value of z = 2.5 put it in range of 2-3
                Layer_Dict[str(math.ciel(Lst[i][part]) +"-"+str(math.floor(math.ciel(Lst[i][part])))]= [(Lst[i][0],Lst[i][1],Lst[2])]
        else:
            Layer_Dict[str(math.ciel(Lst[i][part]) +"-"+str(math.floor(math.ciel(Lst[i][part])))].append((Lst[i][0],Lst[i][1],Lst[i][2]))

    #Layer_Dict is a dictionary with ranges as keys, each range holds all the codinates of that subspace


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
    
    new_vertex = []
    for i in range(len(vertices)):
        new_vertex.append( (vertices[i][0],vertices[i][1],vertices[i][2]) )
    # Create the object
    pc = point_cloud("",new_vertex,faces)
    bpy.context.collection.objects.link(pc)



if __name__ == "__main__":
    main()
