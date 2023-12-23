blTesting = False
Debug = True
day=12

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')


x, y = 0, 0
D = 'E'
Ds =('N', 'E', 'S', 'W', 'N', 'E', 'S', 'W')
for instruction in data:
    #ship initial coordinates
    #ship direction
    #ship instruction
    print(instruction)
    a, i = instruction[0], int(instruction[1:]) 
    if a in ('L', 'R'):
        #change Direction D
        if a == 'L': D = Ds[4 + Ds.index(D) - i//90]
        if a == 'R': D = Ds[Ds.index(D) + i//90]
    else:
        #simple move
        if a == 'F': a=D
        if a == 'N': y += i
        if a == 'E': x += i
        if a == 'S': y -= i
        if a == 'W': x -= i

    #ship new coordinates

answer = abs(x) + abs(y)
print(f"The answer to part I for day {day} is: {answer}")



x, y = 0, 0
D = 'E'
Ds =('N', 'E', 'S', 'W', 'N', 'E', 'S', 'W')
wx, wy = 10, 1
for instruction in data:
    #ship initial coordinates
    #ship direction
    #ship instruction
    print(instruction)
    a, i = instruction[0], int(instruction[1:]) 
    if a in ('L', 'R'):
        #move the waypoint by the number of degrees
        if i == 180: 
            wx, wy = -1*wx, -1*wy
        if (a == 'L' and i == 90) or (a == 'R' and i == 270):
            wx, wy = -1*wy, wx 
        if (a == 'R' and i == 90) or (a == 'L' and i == 270):
            wx, wy = wy, -1*wx 
    elif a == 'F':
        x += i*wx
        y += i*wy
    else:
        #move the waypoint
        if a == 'N': wy += i
        if a == 'E': wx += i
        if a == 'S': wy -= i
        if a == 'W': wx -= i

    #ship new coordinates

answer = abs(x) + abs(y)

print(f"The answer to part II (286) for day {day} is: {answer}")
# 21882 too low