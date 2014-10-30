#!/bin/python

import math
import re

characters = set(['WOMAN','SECRET SERVICE AGENT','AGENT','PROSECUTOR','JUDGE','MRS. MURPHY','DADE','NORM','COMMENTATOR','KID','GIRL','KATE','GUY','GEEK','TEACHER','PHREAK','JOEY','CEREAL','OPERATOR','CURTIS','PLAGUE','HAL','NIKON','BOTH','GILL','RAZOR','BLADE','ALL BUT DADE','SS AGENT',"JOEY\'S MOM",'ANOTHER AGENT','AGENT RAY','REPORTER','JENNIFER','MARGO','VIRUS','BOARD MEMBER','DUKE ELLINGSON','SUIT #1','SUIT #2','SECRET SERVICE AGENT BOB','AGENT BOB','LISA','VICKIE','HANK','CALLER','EMPLOYEE','COP','SYSOP','SOMEONE','STEWARDESS'])

INFILE = open('hackers.txt','r')
OUTFILE = open('hackers_parsed_4.txt','w')

# --- options --- #
ENCODING = 'utf-8'
MAXLENGTH, MINLENGTH = 135, 110
#
# --- functions --- #
def highest_before(seq, maximum):
    """
    Finds the largest entry in seq smaller than maximum.
    Seq must be a list of integers.
    Also returns the index of this entry.
    """
    for j in xrange(len(seq)):
        val = seq[j]
        if val > maximum:
            return j-1, seq[j-1]
    return len(seq), seq[-1]

def twitter_split(string, maxlen):
    """
    Takes a long string/sentence and a specified maximum length,
    splits it into multiple 'lines' suitable for tweeting,
    recording how many splits were made.
    """
    #find spaces
    spaces = [mm.start() for mm in re.finditer(' ', string)]
    # initialise some things
    oldcut, nsplit, newline = -1, 1, ''
    # find last space before the cutoff
    where, newcut = highest_before(spaces, maxlen)
    while not newcut == spaces[-1]:
        newbit = string[oldcut+1:newcut]+' ('+str(nsplit)+'/NSPLITZ)\n'
        newline = newline + newbit
        oldcut = newcut
        where, newcut = highest_before(spaces[where:], newcut + maxlen)
        nsplit += 1
    newbit = string[oldcut+1:]+'('+str(nsplit)+'/NSPLITZ)'
    newline = newline + newbit
    newline = re.sub('NSPLITZ', str(nsplit), newline)
    return newline

def record_sentence(string, ofile):
    """
    Saves a sentence/string to ofile.
    First checks if it is too long/short to tweet,
    splits up if too long.
    """
    print string
    print len(string)
    if len(string) > 3:
        # prep the string a little
        sen = string.lstrip(' ')
        if len(sen) < MAXLENGTH:
            # all goood!
            print sen.encode(ENCODING)
            ofile.write(sen.encode(ENCODING)+'\n')
        else:
            # need to split it up
            # find MAXLENGTH!
            nsplits = math.ceil(float(len(sen))/MAXLENGTH)
            temp_maxlen = int(math.floor(len(sen)/nsplits))
            split_sen = twitter_split(sen, temp_maxlen)
            print split_sen.encode(ENCODING)
            ofile.write(split_sen.encode(ENCODING)+'\n')
    return True

SENTENCE = ''
for line in INFILE:
    ldec = line.decode(ENCODING).strip()
    if len(ldec) == 0:
        # empty, probably paragraph break
        record_sentence(SENTENCE, OUTFILE)
        SENTENCE = ''
    else:
        if ldec in characters:
            print 'Character detected!', ldec
            record_sentence(SENTENCE, OUTFILE)
            SENTENCE = ldec+':'
        elif ldec == ldec.upper():
            if SENTENCE == SENTENCE.upper():
                # continuation of something...
                SENTENCE += ' '+ldec
            else:
                print 'Setting detected!', ldec
                record_sentence(SENTENCE, OUTFILE)
                record_sentence(ldec, OUTFILE)
                SENTENCE = ''
        else:
            # not empty
            # check length
            if len(ldec+SENTENCE) < MAXLENGTH:
                SENTENCE += ' '+ldec
            else:
                if '. ' in ldec or '? ' in ldec:
                    # find the . and ?
                    breakers = [m.start() for m in re.finditer('[.?] ', ldec)]
                    i = 0
                    # split on these
                    for fragment in re.split('[.?] ', ldec)[:-1]:
                        SENTENCE += ' '+fragment+ldec[breakers[i]]
                        i += 1
                        if len(SENTENCE) > MINLENGTH:
                            record_sentence(SENTENCE, OUTFILE)
                            SENTENCE = ''
                        else:
                            continue
                    record_sentence(SENTENCE, OUTFILE)
                    SENTENCE = re.split('[.?] ', ldec)[-1]

record_sentence(SENTENCE, OUTFILE)
OUTFILE.close()
