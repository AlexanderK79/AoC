import argparse
import curses
from curses import wrapper
import glob
import math

def draw_Screen(header, Fmatrix_1, Fmatrix_2, Fmatrix_3):
    max_y, max_x = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
    begin_x, begin_y = 5, 1
    height, width = 3, 60
    winHeader = curses.newwin(height, width, begin_y, begin_x)

    begin_x, begin_y = 5, 5
    height, width = 25, 35
    ATTR = curses.color_pair(1)
    if debug: draw_Matrix(Fmatrix_1, begin_x, begin_y, height, width, ATTR)
    begin_x = 45
    if debug: draw_Matrix(Fmatrix_2, begin_x, begin_y, height, width, ATTR)
    begin_x = 85
    ATTR = curses.color_pair(2) + curses.A_BLINK
    draw_Matrix(Fmatrix_3, begin_x, begin_y, height, width, ATTR)

    winHeader.erase()
    winHeader.addstr(0, 0, header)
    winHeader.addstr(1, 0, 'Press any key for the next step...')
    winHeader.refresh()
    if not debug: stdscr.timeout(1000//500)
    keyInput = stdscr.getch()
    if keyInput in [0, 27]: exit()
    

def draw_Matrix(Fmatrix, begin_x, begin_y, height, width, ATTR):
    winMatrix = curses.newwin(height, width, begin_y, begin_x)
    winMatrix.erase()
    for y in range(0, len(Fmatrix)):
        conv = lambda i : i or '' # convert None to ''
        for x in range(0,len(Fmatrix[y])):
            winMatrix.addstr(2*y, 3*x, str(conv(Fmatrix[y][x])).strip(), ATTR)
    winMatrix.refresh()

def convertHex2Bin(FinputString):
    binparts = []
    for c in FinputString:
        binparts += bin(int(c, 16))[2:].zfill(4)
    return(''.join(binparts))

def readchars(FinputString, Fcursor, Flen):
    return(FinputString[Fcursor:Fcursor+Flen], min(len(FinputString), Fcursor+Flen))

def decodeBinString(FinputBinString):
    cursor = 0
    bin_parts = []
    last_bitgroup = False
    while not last_bitgroup:
        bitgroup, cursor = readchars(FinputBinString, cursor, 5)
        last_bitgroup = True if bitgroup[0] == '0' else False
        bin_parts += [bitgroup[1:]]
    literal_value = int(''.join(bin_parts), 2)
    return(literal_value, cursor)

def decode_packet(FinputString, max_num_of_packets):
    cursor, return_value = 0, []
    while cursor < len(FinputString) and len(return_value) < max_num_of_packets and int(FinputString[cursor:], 2) > 0:
        packet_version, cursor = readchars(FinputString, cursor, 3)
        packet_version         = int(packet_version, 2)
        type_ID       , cursor = readchars(FinputString, cursor, 3)
        type_ID                = int(type_ID, 2) # 4 = literal, others are operators that don't matter for now

        if type_ID != 4:
            length_type_id, cursor = readchars(FinputString, cursor, 1)
            if length_type_id == '0':
                # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
                subpackets_totallength, cursor = readchars(FinputString, cursor, 15)
                subpackets_totallength = int(subpackets_totallength, 2)
                subpacket_string, cursor = readchars(FinputString, cursor, subpackets_totallength)
                packet_value, cursor_tmp = decode_packet(subpacket_string, float('inf'))
                return_value += [{'version': packet_version, 'type_ID': type_ID, 'value': packet_value}]
            elif length_type_id == '1':  
                # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
                subpackets_contained, cursor  = readchars(FinputString, cursor, 11)
                subpackets_contained = int(subpackets_contained, 2)
                subpacket_string, cursor_tmp = readchars(FinputString, cursor, len(FinputString)) # read until end; it will stop, once it has found X packets
                packet_value, stringcursor = decode_packet(subpacket_string, subpackets_contained)
                cursor += stringcursor
                return_value += [{'version': packet_version, 'type_ID': type_ID, 'value': packet_value}]
            else:
                exit('illegal length_type')
        else:
            # type_ID == 4; following concatenation of binary strings is literal number
            # divide the rest of the string into groups of 5 bits; allowing padding zeroes at the end
            # last group marked by starting bit 0
            value_string, cursor_tmp    = readchars(FinputString, cursor, len(FinputString)) # we must keep reading and let decodeBinString return the cursor
            literal_value, stringcursor = decodeBinString(value_string)
            return_value  += [{'version': packet_version, 'type_ID': type_ID, 'value': literal_value}]
            cursor += stringcursor 
            # shouldn't we be processing the rest of the string?

    return(return_value, cursor)

def sum_version(Flist):
    i = 0
    # recursively sum all the values of version
    for item in Flist:
        i += item['version']
        if isinstance(item['value'], list):
            i += sum_version(item['value'])
    return (i)

def parsePacket(Flist):
    # Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. 
    #   If they only have a single sub-packet, their value is the value of the sub-packet.
    # Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. 
    #   If they only have a single sub-packet, their value is the value of the sub-packet.
    # Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    # Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    # Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. 
    #   These packets always have exactly two sub-packets.
    # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. 
    #   These packets always have exactly two sub-packets.
    # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. 
    #   These packets always have exactly two sub-packets.
    values = []
    for item in Flist:
        if item['type_ID'] == 0:
            values += [parsePacket(item['value'])]
            values[-1] = sum(values[-1])
        elif item['type_ID'] == 1:
            values += [parsePacket(item['value'])]
            values[-1] = math.prod([1] + values[-1])
        elif item['type_ID'] == 2:
            values += [parsePacket(item['value'])]
            values[-1] = min(values[-1])
        elif item['type_ID'] == 3:
            values += [parsePacket(item['value'])]
            values[-1] = max(values[-1])
        elif item['type_ID'] == 4:
            values += [item['value']]
        elif item['type_ID'] == 5:
            values += [parsePacket(item['value'])]
            values[-1] = 1 if values[-1][0] > values[-1][1] else 0
        elif item['type_ID'] == 6:
            values += [parsePacket(item['value'])]
            values[-1] = 1 if values[-1][0] < values[-1][1] else 0
        elif item['type_ID'] == 7:
            values += [parsePacket(item['value'])]
            values[-1] = 1 if values[-1][0] == values[-1][1] else 0
        else:
            exit('why do we get here?')

    return(values)

def main(stdscr):
    day = 16
    # f = open(f'input/{day}_sampleA.txt', 'r+')
    # f = open(f'input/{day}.txt', 'r+')

    filepath = f'input/{day}*.txt'
    # filepath = f'input/{day}.txt'
    txt = glob.glob(filepath)
    for textfile in txt:
        fl = open(textfile, 'r+')
        inputFile = fl.read().splitlines()
        fl.close()


        inputString = inputFile[0]
        inputString = convertHex2Bin(inputString)
        cursor = None

        message, cursor = decode_packet(inputString, float('inf'))

        # parse the sum of all version numbers in result
        result_sum = sum_version(message)
        print('The answer to part 1 is (sample should be XXX)', textfile, result_sum)

    # f = open(f'input/{day}_sampleII.txt', 'r+')
    # f = open(f'input/{day}.txt', 'r+')
    inputFile = f.read().splitlines()
    f.close()
    for line in inputFile:
        inputString = line
        inputString = convertHex2Bin(inputString)
        cursor = None

        message, cursor = decode_packet(inputString, float('inf'))
        # if debug: print(message)
        result = parsePacket(message)

        # parse the sum of all version numbers in result
        print('\n'.join(['The answer to part 2 is (sample should be XXX)', line, str(result), str(message)]))

# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = 16
f = open(f'input/{day}_sampleII.txt', 'r+')
if args.production: f = open(f'input/{day}.txt', 'r+')

debug = args.verbose
draw = args.draw

# stdscr = curses.initscr()
# curses.start_color()
# curses.use_default_colors()
# stdscr.scrollok(True)
# winHeader = curses.newwin(1,1,1,1)
# winMatrix_1 = curses.newwin(1,1,2,1)

# wrapper(main)

main(None)