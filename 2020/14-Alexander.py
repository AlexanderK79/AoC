import re

blTesting = False
Debug = True
day=14

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

# keep running the program
mem = 16 * [0]
for line in data:
    #print(line)
    pgm_line = line.split(' = ')
    if pgm_line[0] == 'mask':
        mask = pgm_line[1]
        # convert the mask to two masks - mask0 will change the positions to zero in the result
        mask0 = mask.replace('1', 'Y').replace('0','1').replace('X', '0').replace('Y', '0')
        mask1 = mask.replace('X', '0')
        mask0 = int(mask0, 2)
        mask1 = int(mask1, 2)
        mem_addr, mem_value = 2 * [None]
    else:
        mem_addr = re.match('^mem\[(.+)\]$', pgm_line[0] )
        if mem_addr is None:
            mem_addr = -1
            quit
        else:
            mem_addr = int(mem_addr.groups()[0])
            mem_value = int(pgm_line[1])
        # apply the mask0 to remove any 1's if present and change them to zeroes
        mem_value = (mem_value|mask0) ^ mask0 
        # apply the mask1 to force any 1's
        mem_value = mem_value | mask1
        # write the mem_value; enlarge mem if necessary
        if mem_addr > len(mem):
            mem = mem + ((1+mem_addr - len(mem)) * [0])
        mem[mem_addr] = mem_value
        #print('Hello there', mask, mem_addr, mem_value)

answer = sum(mem)
print (f'The answer to part 1 of day {day} is: {answer}')
