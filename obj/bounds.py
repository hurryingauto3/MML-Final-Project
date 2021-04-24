import math
with open("bugatti.obj", "r") as file1:
    xmin = ymin = zmin = math.inf
    xmax = ymax = zmax = -math.inf
    vertex = 0
    for line in file1.readlines():
        if line[:2] == "v ":
            vertex += 1
        line = line.split()[1:]

        for i in range(len(line)):
            line[i] = float(line[i])

        if line[0] < xmin:
            xmin = line[0]
        if line[1] < ymin:
            ymin = line[1]
        if line[2] < zmin:
            zmin = line[2]

        if line[0] > xmax:
            xmax = line[0]
        if line[1] > ymax:
            ymax = line[1]
        if line[2] > zmax:
            zmax = line[2]
    print((xmin, ymin, zmin), (xmax, ymax, zmax))
