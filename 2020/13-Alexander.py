blTesting = True
Debug = True
day=13

if blTesting:
    with open(f'{day}-sample-input1.txt', 'r') as file: data = file.read().split('\n')
    # with open(f'{day}-sample-input2.txt', 'r') as file: data = file.read().split('\n')
else:
    with open(f'{day}-Alexander-input.txt', 'r') as file: data = file.read().split('\n')

# 939
# 7,13,x,x,59,x,31,19

# find lowest lcf that is higher than timestamp 939

results ={}
earliestTime = int(data[0])
for i in data[1].split(','):
    if (i == 'x'): continue
    else: 
        i = int(i)
        results[i] = ((earliestTime//i)+1)*i

# find the key with the earliest possibility
earliestDepart = min(results.values()) 
bus = min([key for key in results if results[key] == earliestDepart] )

answer = (earliestDepart - earliestTime) * bus

print(f'The answer to part I for day {day} is {answer}; bus {bus} at {earliestDepart}')


# when is the time that all buses leave in the correct order
# seems like a case for LCM
# 7,13,x,x,59,x,31,19
# when does line 13 leave 1 minute after bus 7?
# to find the situation where they leave at the same time: lcm(7,13)
# timestamp  busnum       run  busnum     run
#     0         7           0      13       0
#    77                    11                 <== first time they match (init)
#    78                                     6 
#   168              11+13=24                 <== repeats every 13 (=other busnum) since init
#   169                                6+7=13 <== repeats every  7 (=other busnum) since init
#   259              24+13=37         13+7=20
#                   each step is 91, starting at 77
#
#                                       bus 59
#  350                    50                  <== first time they match (init)
#  354                                      6
#  763             50+59=109
#  767                                 6+7=13
# 1176            109+59=168
# 1180                                13+7=20
#                   each step is 413, starting at 350
#
#                                       bus 31
#   56                     8                  <== first time they match
#   62                                      2
#  273               8+31=39
#  279                                  2+7=9
#  490              39+31=70
#  496                                 9+7=16

#  timestamps where bus 7 and 13 match:
# (init + 13x) * 7 = 77, 168, 259, etc
#  timestamps where bus 7 and 59 match:
# (init + 59x) * 7 = 350, 763, 1176, etc
#  timestamps where bus 7 and 31 match:
# (init + 31x) * 7 = 56, 273, 490, etc
# (init + 19x) * 7 = 
# the magic number? the lowest number that is in all 4 sets ==> no easy python for that
# find the lcm where 


import numpy as np

busSchedule = data[1].split(',')
busScheduleInts = tuple(filter(lambda x: x not in ['x'], list(busSchedule)))
AllignedIntervals = []
for curBus in busSchedule:
    if curBus == 'x': continue
    diffFromOriginal = busSchedule.index(curBus)
    if diffFromOriginal == 0: 
        firstBus = curBus
        continue
    curBusPos, curBusPosInt = busSchedule.index(curBus), busScheduleInts.index(curBus)
    i = 1
    while not (i*int(curBus)) % int(firstBus) == diffFromOriginal % int(firstBus):
        i+=1 # the number of runs of this bus
        k = i # run of this bus
        j = (k - diffFromOriginal)//int(firstBus)  # init run number of the initial bus
    repeatInterval = (j+k)
    print(f'The buses {firstBus} and {curBus} have their desired interval {diffFromOriginal} for the first time at timestamp of firstBus {j}, timestamp of curBus {k}, which repeats every {repeatInterval} seconds')
    AllignedIntervals.append(repeatInterval)

curLCM = np.int64(0)
for item in AllignedIntervals:
    if curLCM == 0: curLCM = item
    curLCM = np.int64(np.lcm(curLCM, item))

answer = curLCM
for curBus in busScheduleInts:
    diffFromOriginal = busSchedule.index(curBus)
    print (curBus, (curLCM + diffFromOriginal)/ int(curBus)) 


print(f'The answer to part II for day {day} is {answer}')
