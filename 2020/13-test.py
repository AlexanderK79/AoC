def part2(buses):
    mods = {}
    # store the list of buses in a dict with bus number and index (# of minutes after first bus)
    for idx, bus in enumerate(buses):
        if bus != 'x':
            bus = int(bus)
            mods[bus] = -idx % bus

    iterator = 0
    increment = 1
    for bus in mods.keys(): # go through all of the bus lines in the dict
        while iterator % bus != mods[bus]: # keep running as long as the iterator modulo bus number does not equal the index... 
            iterator += increment # add the current increment (=increment * previous bus number) to the iterator
        increment *= bus # multiply the increment by the bus number and continue with the next bus line

    return iterator

blTesting = False
Debug = True
day=13

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

print (part2(data[1].split(',')))
