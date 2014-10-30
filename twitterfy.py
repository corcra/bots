#!/bin/python
"""
I eat books!
I give you tweets!
READ A BOOOK READ A BOOK
READ A MOTHERFUCKING BOOK
"""
import math
import re
import sys

if len(sys.argv) < 2:
    sys.exit('USAGE: twitterfy.py filepath')
INFILE = open(sys.argv[1], 'r')
OUTFILE = open(sys.argv[1]+'.twit', 'w')

# --- options --- #
ENCODING = 'utf-8'
MAXLENGTH, MINLENGTH = 135, 80

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
    # find spaces
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

# --- do things ! --- #
SENTENCE = ''
for line in INFILE:
    ldec = line.decode(ENCODING).strip()
    if len(ldec) == 0:
        # empty, probably a paragraph break
        record_sentence(SENTENCE, OUTFILE)
        SENTENCE = ''
    else:
        # not empty
        if len(ldec+SENTENCE) < MAXLENGTH:
            # proceed as normal
            SENTENCE += ' '+ldec
        else:
            # need to split it somewhere, look for full stops...
            if '. ' in ldec or '? ' in ldec:
                # find the . and ?
                breakers = [m.start() for m in re.finditer('[.?] ', ldec)]
                i = 0
                # split on these
                for fragment in re.split('[.?] ', ldec)[:-1]:
                    SENTENCE += ' '+fragment+ldec[breakers[i]]
                    i += 1
                    #'.'
                    if len(SENTENCE) > MINLENGTH:
                        record_sentence(SENTENCE, OUTFILE)
                        SENTENCE = ''
                    else:
                        continue
                record_sentence(SENTENCE, OUTFILE)
                SENTENCE = re.split('[.?] ', ldec)[-1]
            else:
                # add to growing sentence!
                SENTENCE += ' '+ldec
record_sentence(SENTENCE, OUTFILE)
OUTFILE.close()
