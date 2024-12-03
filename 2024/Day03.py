import argparse
import re

def processReport(fReport):
        fReport_status_asc  = [fReport[i] > fReport[i-1] for i in range(1,len(fReport))]
        fReport_status_desc = [fReport[i] < fReport[i-1] for i in range(1,len(fReport))]
        fReport_status_diff_asc  = [0 < (fReport[i]-fReport[i-1]) <= 3 for i in range(1,len(fReport))]
        fReport_status_diff_desc = [-3 <= (fReport[i]-fReport[i-1]) < 0 for i in range(1,len(fReport))]
        return (all(fReport_status_asc) is True or all(fReport_status_desc) is True) is True and (all(fReport_status_diff_asc) is True or all(fReport_status_diff_desc) is True)
        
def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myProgram = list()

    thisAction = 'do()'
    for i, line in enumerate(fContent):
        regex = re.finditer('(do\(\)|don\'t\(\))|(mul)\((\d{1,3}),(\d{1,3})\)', line.strip() )
        myProgram.append({'index': i, 'matches': regex, 'content': list()} )
        for j, m in enumerate(regex):
            thisContent = myProgram[i]['content']
            if m.group(1) is not None:
                 thisAction = m.group(1)
                 thisContent.append({'index': i, 'subindex': j, 'action': thisAction, 'result': 0})
                 continue
            else:
                thisContent.append({'index': i, 'subindex': j, 'action': thisAction, 'input_1': int(m.group(3)), 'input_2': int(m.group(4)), 'result': int})
                thisContent[j]['result'] = thisContent[j]['input_1'] * thisContent[j]['input_2']
        
        myProgram[i]['result'] = sum([r['result'] for r in thisContent])
        pass

    result = sum([r['result'] for r in myProgram])
    message = f'The answer to part 1 is (sample should be 161, answer should be 159833790): {result}\n'
    print(message)

    for c in myProgram:
        c['result2'] = sum([r['result'] for r in [i for i in c['content']] if r['action'] == "do()"])

    result = sum([r['result2'] for r in myProgram])
    message = f'The answer to part 2 is (sample should be 48, answer should be ?): {result}\n'
    # 91634027 too high
    print(message)

    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '03'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose

main(None)