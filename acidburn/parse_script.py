#!/bin/python

import math
import re

characters = set(['WOMAN','SECRET SERVICE AGENT','AGENT','PROSECUTOR','JUDGE','MRS. MURPHY','DADE','NORM','COMMENTATOR','KID','GIRL','KATE','GUY','GEEK','TEACHER','PHREAK','JOEY','CEREAL','OPERATOR','CURTIS','PLAGUE','HAL','NIKON','BOTH','GILL','RAZOR','BLADE','ALL BUT DADE','SS AGENT',"JOEY\'S MOM",'ANOTHER AGENT','AGENT RAY','REPORTER','JENNIFER','MARGO','VIRUS','BOARD MEMBER','DUKE ELLINGSON','SUIT #1','SUIT #2','SECRET SERVICE AGENT BOB','AGENT BOB','LISA','VICKIE','HANK','CALLER','EMPLOYEE','COP','SYSOP','SOMEONE','STEWARDESS'])

infile = open('../hackers_script.txt','r')
outfile = open('hackers_parsed_3.txt','w')

def lowestbefore(seq, maximum):
    for i in xrange(len(seq)):
        val = seq[i]
        if val > maximum:
            return seq[i-1]
    # if it hasn't returned anything yet, then...
    # nothing in the sequence is larger than the maximum
    # so how did this happen?
    # why would this ever happen?
    # i am confused and hungry
    return None
        
def twittersplit(line):
    maxlength = 140
    if len(line)<maxlength:
        return line
    else:
        # find the spaces
        spaces = [m.start() for m in re.finditer(' ', line)]
        # initialise some stuff
        oldcut = -1
        nsplit = 1
        newline = ''
        # find the last space before the cutoff
        newcut = lowestbefore(spaces, maxlength)
        while newcut:
            newline = newline + line[oldcut+1:newcut]+'['+str(nsplit)+'/NSPLITZ]\n'
            oldcut = newcut
            newcut = lowestbefore(spaces[newcut:], (nsplit+1)*maxlength)
            nsplit += 1
        newline = newline + line[oldcut+1:newcut]+'['+str(nsplit)+'/NSPLITZ]\n'
        newline = re.sub('NSPLITZ',str(nsplit),newline)
        return newline

        #
#        nsplit = int(math.ceil(float(len(line))/(maxlength-10)))
#        newline = ''
#        for i in xrange(nsplit):
#            newline = newline+line[i*(maxlength-10):(i+1)*(maxlength-10)]+'['+str(i+#1)+'/'+str(nsplit)+']\n'
#        return newline.replace('\\','')

    # this bit here is the starts of the 'making it not cut up words' improvement
#    else:
#        spaces = [m.start() for m in re.finditer(' ',line#)]
#        breakpoints = [ 
#        newline = ''
#        for i in xrange(nsplit):
#            closest_space = 
#        newline = ''
#        stoppoint=0
#        for i in xrange(nsplit):
            
        
buffline = ''
line = infile.readline()
while line:
    lp = line.strip()
    if lp in characters:
        print 'Character detected!',lp
        # character is speaking!
        if len(buffline)>1: outfile.write(twittersplit(buffline)+'\n')
        buffline = lp+':'
        while len(line)>1:
            line = infile.readline()
            buffline += ' '+line.strip()
#    elif lp.upper() == lp and len(line)>1:
#        # must be a location!
#        print 'Location detected!',lp
#        if len(buffline)>1: outfile.write(twittersplit(buffline)+'\n')
#        buffline = lp
#        buffline = ''
#        while len(line)>1:
#            line = infile.readline()
#            buffline += ' '+line.strip()
    elif len(line)>1:
        # must be a description or something
        print 'Normal text detected!',lp
        if len(buffline)>1: outfile.write(twittersplit(buffline)+'\n')
        buffline = lp
        while len(line)>1:
            line = infile.readline()
            buffline += ' '+line.strip()
    line = infile.readline()

if len(buffline)>1: outfile.write(twittersplit(buffline)+'\n')
outfile.write(twittersplit(buffline)+'\n')
outfile.close()
