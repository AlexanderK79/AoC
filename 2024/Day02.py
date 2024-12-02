import argparse

def processReport(fReport):
        fReport_status_asc  = [fReport[i] > fReport[i-1] for i in range(1,len(fReport))]
        fReport_status_desc = [fReport[i] < fReport[i-1] for i in range(1,len(fReport))]
        fReport_status_diff_asc  = [0 < (fReport[i]-fReport[i-1]) <= 3 for i in range(1,len(fReport))]
        fReport_status_diff_desc = [-3 <= (fReport[i]-fReport[i-1]) < 0 for i in range(1,len(fReport))]
        return (all(fReport_status_asc) is True or all(fReport_status_desc) is True) is True and (all(fReport_status_diff_asc) is True or all(fReport_status_diff_desc) is True)
        
def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()

    myReports = list()
    for line in fContent:
        thisReport = [int(i) for i in line.split()]
        thisReport_status_one = processReport(thisReport)

        for i in range(0,len(thisReport)):
            tmpReport = [j for j in thisReport]
            del tmpReport[i]
            thisReport_status_two = processReport(tmpReport)
            if thisReport_status_two: break

        myReports.append([thisReport, thisReport_status_one, thisReport_status_two])
        del thisReport, thisReport_status_one, thisReport_status_two
    pass

    result = len([i for i in myReports if i[1]])
    message = f'The answer to part 1 is (sample should be 2, answer should be 218): {result}\n'
    print(message)

    result = len([i for i in myReports if i[1] or i[2]])
    message = f'The answer to part 2 is (sample should be 4, answer should be 290): {result}\n'
    print(message)

    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '02'
fName = f'2024/input/{day}_sample.txt'
if args.production: fName = f'2024/input/{day}.txt'

debug = args.verbose

main(None)