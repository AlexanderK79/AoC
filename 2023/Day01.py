import argparse
import re

class trebDoc:
    def __init__(self) -> None:
        self.content = list()
        self.lines = list()
        self.sum = 0
        pass
    def build(self, fContent):
        self.content = fContent
        return self
    def process(self, fPart):
        rownum = 0
        numbers2text = ['zerogeenmatchhier', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        for line in self.content:
            self.lines.append(dict({'rownum': rownum, 'line_org': line, 'line': line}))
            line_replaced = line
            if fPart == '1':
                regex = re.match('^.*?(\d).*(\d).*?$', line.strip() )
                if regex is None:
                    regex = re.match('^.*?(\d).*?$', line.strip() )
                if regex is None:
                    pass
                else:
                    self.lines[rownum]['firstDigit'] = regex.groups()[0]
                    self.lines[rownum]['lastDigit'] = regex.groups()[1] if regex.re.groups >= 2 else regex.groups()[0]
            elif fPart == '2':
                re_str_forward = '.*?(('+')|('.join(numbers2text)+')|(\d)).*'
                re_str_backward = '.*(('+')|('.join(numbers2text)+')|(\d)).*?'
                frstMatch = re.match(re_str_forward,  line_replaced).groups()[0]
                lastMatch = re.match(re_str_backward, line_replaced).groups()[0]
                self.lines[rownum]['firstDigit'] = frstMatch if len(frstMatch) == 1 else frstMatch.replace(frstMatch, str(numbers2text.index(frstMatch)))
                self.lines[rownum]['lastDigit']  = lastMatch if len(lastMatch) == 1 else lastMatch.replace(lastMatch, str(numbers2text.index(lastMatch)))
                pass

            self.lines[rownum]['concat'] = int(''.join((self.lines[rownum]['firstDigit'], self.lines[rownum]['lastDigit'])))
            rownum += 1
        return self
    def sumall(self):
        self.sum = sum([i['concat'] for i in self.lines])
        return self.sum

def main(stdscr):
    fName = f'2023/input/{day}_sample.txt'
    if args.production: fName = f'2023/input/{day}.txt'

    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    myDoc = trebDoc()
    result = myDoc.build(fContent=fContent)
    result = myDoc.process(fPart = '1')
    result = myDoc.sumall()

    message = f'The answer to part 1 is (sample should be 142, answer should be 56108): {result}'
    print(message)

    print(20 * '*')
    fName = f'2023/input/{day}_sample_part2.txt'
    if args.production: fName = f'2023/input/{day}.txt'
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    myDocPartTwo = trebDoc()
    result = myDocPartTwo.build(fContent=fContent)

    result = myDocPartTwo.process(fPart = '2')
    result = myDocPartTwo.sumall()

    message = f'The answer to part 2 is (sample should be 281, answer should be 55652): {result}'
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '01'

debug = args.verbose
draw = args.draw

main(None)