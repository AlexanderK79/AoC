import re
import math
import numpy as np

blTesting = False
Debug = False
day='14b'

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

def removeMSB(i):
    #this function returns the number i with the most significant bit removed
    if i < 1: return 0 
    j = int(math.log(i,2))
    return (i-(2**j))
def justMSB(i):
    #this function returns the number i with just the most significant bit
    if i < 1: return 0 
    j = int(math.log(i,2))
    return 2**j

# keep running the program
#mem = 16 * [0] # a list is too small for part 2
#mem = np.arange(16, dtype=np.int64)
mem ={}

for line in data:
    #print(line)
    pgm_line = line.split(' = ')
    if pgm_line[0] == 'mask':
        mask = pgm_line[1]
        # convert the mask to new masks - mask0 will change the positions to zero in the result
        #mask0 replaces the 0 with 1 and the rest to zero; zero's do not change a mem address
        mask0 = mask.replace('1', 'Y').replace('0','1').replace('X', '0').replace('Y', '0')
        #mask1 keeps the 1's and changes X to 0; 1's will always be a one in a mem address
        mask1 = mask.replace('X', '0')
        #maskX changes the X into 0's; X's take on both values in the mem address
        maskX = mask.replace('1', '0').replace('X', '1')
        mask0 = int(mask0, 2)
        mask1 = int(mask1, 2)
        maskX = int(maskX, 2)
        mem_addr, mem_value = 2 * [None]
    else:
        mem_addr = re.match('^mem\[(.+)\]$', pgm_line[0] )
        if mem_addr is None:
            mem_addr = -1
            quit
        else:
            mem_addr = np.int64(mem_addr.groups()[0])
            mem_addrOrg = mem_addr
            mem_value = np.int64(pgm_line[1])
            if Debug:
                print(f"{mask:>40} mask")
                #print(f"{mem_value:>40b} value to write")
                print(f"{mem_addrOrg:>40b} mem_addrOrg")
        # apply the mask0 to remove any 1's if present and change them to zeroes
        #mem_addr = (mem_addr|mask0) ^ mask0 
        #mask0 does not really have an effect in this situation
        #mem_addr = np.int64(mem_addr | mask0)
        # apply the mask1 to force any 1's
        mem_addr = np.int64(mem_addr | mask1)
        # apply the maskX to calculate every possible mem_addr
        mem_addr = np.int64(mem_addr|maskX)
        mem_addrs = [mem_addr]
        # build the list of mem addresses to write
        maskXloop = maskX
        while maskXloop > 0:
            for mem_addr in tuple(mem_addrs):
                mem_addrs.append(np.int64(mem_addr - justMSB(maskXloop)))
            maskXloop = removeMSB(maskXloop)

        for mem_addr in reversed(sorted(mem_addrs)):
            # write the value to memory; enlarge mem if necessary
            # if mem_addr >= len(mem):
            #     np.pad(mem, mem_addr)
            mem[mem_addr] = mem_value
            if Debug:
                print(f"{mem_addr:>40b} mem_addr")
                #print(mask, f"{mem_value:>10}{mem_addr:>10}{mem_addr:>10b}")

answer = sum(mem.values())
print (f'The answer to part 2 of day {day} is: {answer}')
