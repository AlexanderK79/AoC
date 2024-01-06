def polygon_area(vertices):
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area

# Triangle with vertices (0,0), (0,1), and (1,0)
vertices = [(0,0), (0,1), (1,0)]
print(polygon_area(vertices)) # Output: 0.5
# Square with vertices (0,0), (0,1), (1,1), and (1,0)
vertices = [(0,0), (0,1), (1,1), (1,0)]
print(polygon_area(vertices)) # Output: 1.0
# Pentagon with vertices (0,0), (1,1), (2,0), (1,-1), and (-1,-1)
vertices = [(0,0), (1,1), (2,0), (1,-1), (-1,-1)]
print(polygon_area(vertices)) # Output: 4.0

pass