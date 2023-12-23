with open('06-Alexander-input.txt', 'r') as file: data = file.read().split('\n\n')

def part_A(data):
    newdata=[]
    count = 0 
    totalcount = 0
    for i in data:
        newdata.append(i.replace('\n', ''))

    for i in newdata:
        s=set(i)
        count = len(s)
        totalcount+=count
    return totalcount

def part_B(data):
    totalcountb = 0
    for i in data:
        newlist = []
        countb = 0
        newlist.append(i.split('\n'))
        for j in newlist:
            count = len(set.intersection(*[set(k) for k in j]))
            print(f"{''.join(sorted(set.intersection(*[set(k) for k in j])))},{count}")
            totalcountb +=count
    return totalcountb

print('Part A: The sum of the counts is: ', part_A(data))
print('Part B: The sum of the counts is: ', part_B(data))