import argparse
from math import lcm

class pulseMap:
    def __init__(self) -> None:
        self.content = list()
        self.pulseCounter = {'low': 0, 'high': 0}
        self.queue = []
        self.modules = {}
        pass
    def build(self, fContent):
        self.content = fContent
        # build all pulseModules
        for thisLine in fContent:
            for (src, dest) in [thisLine.split(' -> ')]:
                if src[0] in ('%', '&'):
                    thisName = src[1:]
                    if   src[0] == '%': thisType = 'ff'
                    elif src[0] == '&': thisType = 'cj'
                    else: thisType = None
                else:
                    thisName = src
                    if src == 'broadcaster': thisType = 'bc'
                    else: thisType = None
                pass
                self.modules[thisName] = pulseModule(self, thisName, thisType, dest)
            pass
        # create all destinations that do not exist yet, these are output queues
        for dests in list(filter(None, [[d for d in pm.destinations_text if d not in self.modules.keys()] for pm in self.modules.values()])):
            for dest in dests:
                self.modules[dest] = pulseModule(self, dest, 'output', '')
            pass
        del dest, dests
        
        # now all modules are built, make the crossreferences
        for pm in self.modules.values():
            for dest in pm.destinations_text:
                if dest == '': continue
                pm.destinations.append(self.modules[dest])
                self.modules[dest].sources.append(pm)
        pass
    def process(self, thisPM, thisVal):
        # process the queue
        self.queue.append((thisPM,thisVal))
        while len(self.queue) > 0:
            if args.verbose: print(' - '.join([i[0].name for i in self.queue]))
            pm, thisPulse = self.queue.pop(0)
            pm.process(thisPulse)
            pass

class pulseModule:
    def __init__(self, fParent, fName, fType, fDest) -> None:
        self.parent = fParent
        self.name = fName
        self.type = fType # bc (broadcaster), ff (flipflop %), cj (conjunction &)
        self.state = None if self.type in ('bc', 'cj') else 'off'
        self.destinations_text = [i.strip() for i in fDest.split(',')]
        self.destinations = [] # references to destination modules
        self.sources = [] # references to source modules
        self.lastPulse = 'low'
        self.intervalHigh = 0 if fType == 'cj' else None
        self.counter={'low': 0, 'high': 0}
    def process(self, fPulse):
        self.parent.pulseCounter[fPulse] += 1
        self.counter[fPulse] += 1
        if self.type == 'ff':
            # If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
            if fPulse == 'high':
                outPulse = None
            elif fPulse == 'low':
                # However, if a flip-flop module receives a low pulse, it flips between on and off. 
                if self.state == 'off':
                    # If it was off, it turns on and sends a high pulse. 
                    self.state = 'on'
                    outPulse = 'high'
                elif self.state == 'on':
                    # If it was on, it turns off and sends a low pulse.
                    self.state = 'off'
                    outPulse = 'low'
            pass
        elif self.type == 'cj':
            #if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
            if set([pm.lastPulse for pm in self.sources]) == set({'high'}):
                outPulse = 'low'
            else:
                outPulse = 'high'
                if self in self.parent.modules['rx'].sources[0].sources:
                    # it turns out to be an easy interval, starting at 0 and stable, from the start
                    if self.intervalHigh == 0:
                        self.intervalHigh=sum(self.parent.modules['broadcaster'].counter.values())
                    print(self.name, self.intervalHigh)
            pass
        elif self.type == 'bc':
            # When it receives a pulse, it sends the same pulse to all of its destination modules.
            outPulse = fPulse
            pass
        elif self.type == "output":
            self.state = fPulse
            outPulse = None
            pass
        # now queue the pulse
        if outPulse is not None:
            self.lastPulse = outPulse # only active pulses are stored for a cj
            for pm in self.destinations:
                pass
                self.parent.queue.append((pm, outPulse))
        pass

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    
    """
    myMap = pulseMap()
    result = myMap.build(fContent=fContent)
    for i in range(1, 1001):
        myMap.process(myMap.modules['broadcaster'], 'low')
        if args.verbose: print('\n')
        if args.verbose: [print(i, pm.name, pm.state) for pm in myMap.modules.values() if pm.state is not None]
        if args.verbose: print('\n')
    result = myMap.pulseCounter['low'] * myMap.pulseCounter['high']

    message = f'The answer to part 1 is (sample should be 11687500, answer should be 681194780): {result}'
    print(message)

    print(20 * '*')
    """

    myMap_p2 = pulseMap()
    result = myMap_p2.build(fContent=fContent)
    i = 0
    # analyze the flow; rx will receive a low signal, if there is one input for rx
    # this is bq: a conjunction module
    # this will send a low signal, if all of it's inputs are high
    # check out https://mermaid.live/view#pako:eNplVMFy2yAQ_RUPh56cyI4dO_Ghh06vPbWnyj1IQoAthCUgKmHH_14QqwyT-sDIj-Xt290HQJobbcmJMHn724hK29Wvb2e1Cr96LIt6PJ__rB4evq60S6ix77IN_1bsIuVJtzTBioKi9zmSmQSNEkaZoNEniHvgPkHTlCDJQfIEebf6spKYx2qwOuEGc0wKJoWEMoQurB2HDikcQuYK5pogjnIEA8EwqkfCCaYpQf0YCGmNMhlwDGUq0-QteIuaOmxSD3WfIBnlN0PCmwGaIcP5Qm2AGxQ2ZjWYAQzG0zrgV4H8AmqR8E5nEl0Nrl6aG_BJJZw5YA5xhilH4GMW6haKARym9LHKpc1CgsC5WZ3hpgPTJVwh1AvoUZ0zWejoyyJUhtZRNG5d49LFVgxxaaJoERZvcRi8LCa-nAnGS0kFGMwwYKuuAq5LSzg6YCiLbvh8lg_AlwIxCW_KgjefAx0Dt1hjmd8EzbTYL6gUMuG0LoswAyToeCwq1tPFhbl5crG8xZoaOr2MFZN5cHgHvMkmygwwk43JXDG-B4cO60RmxpHByDLHLCmZAoa3pEafdwI6kZsRnTEJmESWkmPx_Qg9OqYWmUSvwCN1g9fXTGCwT45lDpAC5EdKbJ0Eir6SeSHegXeZOoHqBg-Dz0bQoMUbBY3KcINSnAGHDTR4e3gNvM6oKU7RurKw7j-v0bII-hHto0YbT5n4NVc33xOHD4oMJPKDZH4oRAyaoikkOtMb8CabEsOia32raFMZ2-r0HIrFSTIe70MBZE36VvfVhYbnGeKxM7Gi7dszOYVPWunuTM7qHuKqN3v7-a4acmKVNO2avA20su33S8V11X-gLb3Ym_6RHvz53V-ToVLkBMSR0-7p-LjZHw6bzW6_Pb4eXtfknZyOj_vtbvO8DxtP--Pz8-t9TfztFki3j0_H7fG4374cdi-bl91hN7P9njetfmvv_wDLldnM
    # for a flowchart of this pulseMap

    bq_inputs = [pm.intervalHigh for pm in myMap_p2.modules['rx'].sources[0].sources if pm.intervalHigh>0]
    while len(bq_inputs)<4:
        i += 1
        myMap_p2.process(myMap_p2.modules['broadcaster'], 'low')
        if i % 1000 == 0: print('processing cycle', i)
        bq_inputs = [pm.intervalHigh for pm in myMap_p2.modules['rx'].sources[0].sources if pm.intervalHigh>0]
    print ('cycle', i, 'bq_inputs', bq_inputs)
    result = lcm(*bq_inputs)

    message = f'The answer to part 2 is (there is no sample, answer should be 238593356738827, 115446164960 is too low): {result}'
    
    print(message)
    pass


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '20'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)