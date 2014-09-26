#!/bin/python

import math
import re

characters = set(['WOMAN','SECRET SERVICE AGENT','AGENT','PROSECUTOR','JUDGE','MRS. MURPHY','DADE','NORM','COMMENTATOR','KID','GIRL','KATE','GUY','GEEK','TEACHER','PHREAK','JOEY','CEREAL','OPERATOR','CURTIS','PLAGUE','HAL','NIKON','BOTH','GILL','RAZOR','BLADE','ALL BUT DADE','SS AGENT',"JOEY\'S MOM",'ANOTHER AGENT','AGENT RAY','REPORTER','JENNIFER','MARGO','VIRUS','BOARD MEMBER','DUKE ELLINGSON','SUIT #1','SUIT #2','SECRET SERVICE AGENT BOB','AGENT BOB','LISA','VICKIE','HANK','CALLER','EMPLOYEE','COP','SYSOP','SOMEONE','STEWARDESS'])

infile = open('hackers_script.txt','r')
outfile = open('hackers_parsed.txt','w')

def twittersplit(line):
    maxlength = 140
    if len(line)<maxlength:
        return line
    else:
        spaces = [m.start() for m in re.finditer(' ',line)]
        breakpoints = [ 
        nsplit = int(math.ceil(float(len(line))/(maxlength-10)))
        newline = ''
        for i in xrange(nsplit):
            closest_space = 
        newline = ''
        stoppoint=0
        for i in xrange(nsplit):
            
#        return ''
        newline = ''
        for i in xrange(nsplit):
            newline = newline+line[i*(maxlength-10):(i+1)*(maxlength-10)]+'['+str(i+1)+'/'+str(nsplit)+']\n'
        return newline.replace('\\','')

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
