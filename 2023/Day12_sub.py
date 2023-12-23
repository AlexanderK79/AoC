import itertools
import re

re_str, g = '?###????????', (3,2,1)
re_str, g = '?????????..#?????', (3,5)
re_str, g = '????.?????', (1,2)
re_str, g = '????.######..#####.', (1,6,5)
c = '#'
s = [i*c for i in g ]
thisLen = len(re_str)
spaces = len(re_str) -sum(g) - len(g) + 1
re_str = '^' + re_str + '$'


spaceCombi = [(i+1) * '.' for i in range(spaces)]
allElements = [[''] + spaceCombi]
for thisG in s:
    allElements.append([''.join(i) for i in itertools.product([thisG], spaceCombi)])
    pass
re_pat_1 = '[\.]*' + '[\.]+'.join([f'([#.]{{{i}}}?)' for i in g]) +'[\.\$]+'
re_pat_2 = re_str.replace('$', '.$').replace('.', '\.').replace('?','[\.#]')
possibleCombi = list(sorted(set([''.join(i) for i in itertools.product(*allElements) if len(''.join(i)) == thisLen +1])))
pass
possibleCombi = [i[:-1] for i in possibleCombi if re.match(re_pat_1, i) and re.match(re_pat_2, i)]
pass

[print('*', ''.join(i), '*') for i in sorted(possibleCombi)]
print('thisLen', thisLen, 'combinations', len(possibleCombi))



pass
# [''.join(i) for i in itertools.combinations([thisG, ' ', '  ','   '], 2) if len(''.join(i).strip()) > 0]