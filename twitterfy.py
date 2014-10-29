#!/bin/python
# I eat books!
# I give you tweets!
# READ A BOOOK READ A BOOK
# READ A MOTHERFUCKING BOOK
import math
import re
import sys

if len(sys.argv)<2:
    sys.exit('USAGE: twitterfy.py filepath')
infile = open(sys.argv[1],'r')
outfile = open(sys.argv[1]+'.twit','w')

# --- options --- #
encoding = 'utf-8'
global maxlength, minlength
maxlength, minlength = 135, 80

# --- functions --- #
def highest_before(seq, maximum):
    for i in xrange(len(seq)):
        val = seq[i]
        if val > maximum:
            return i-1, seq[i-1]
    return len(seq), seq[-1]

def twitter_split(sentence, maxlen):
    # find spaces
    spaces = [m.start() for m in re.finditer(' ', sentence)]
    # initialise some things
    oldcut, nsplit, newline = -1, 1, ''
    # find last space before the cutoff
    where, newcut = highest_before(spaces, maxlen)
    while not newcut == spaces[-1]:
        newline = newline + sentence[oldcut+1:newcut]+' ('+str(nsplit)+'/NSPLITZ)\n'
        oldcut = newcut
        where, newcut = highest_before(spaces[where:], newcut + maxlen)
        nsplit += 1
    newline = newline + sentence[oldcut+1:]+'('+str(nsplit)+'/NSPLITZ)'
    newline = re.sub('NSPLITZ',str(nsplit),newline)
    return newline

def record_sentence(sentence, outfile):
    if len(sentence) > 3:
        # prep the sentence a little
        sen = sentence.lstrip(' ') 
        if len(sen) < maxlength:
            # all goood!
            print sen.encode(encoding)
            outfile.write(sen.encode(encoding)+'\n')
        else:
            # need to split it up
            # find maxlength!
            nsplits = math.ceil(float(len(sen))/maxlength)
            temp_maxlen = int(math.floor(len(sen)/nsplits))
            split_sen = twitter_split(sen, temp_maxlen)
            print split_sen.encode(encoding)
            outfile.write(split_sen.encode(encoding)+'\n')
    return True

# --- do things ! --- #
sentence = ''
for line in infile:
    ldec = line.decode(encoding).strip()
    if len(ldec) == 0:
        # empty, probably a paragraph break
        record_sentence(sentence, outfile)
        sentence = ''
    else:
        # not empty
        if '. ' in ldec or '? ' in ldec:
            # find the . and ?
            breakers = [m.start() for m in re.finditer('[.?] ', ldec)]
            i = 0
            # split on these
            for fragment in re.split('[.?] ',ldec)[:-1]:
                sentence += ' '+fragment+ldec[breakers[i]]
                i+=1
                #'.'
                if len(sentence) > minlength:
                    record_sentence(sentence, outfile)
                    sentence = ''
                else: 
                    continue
            sentence = re.split('[.?] ',ldec)[-1]
        else:
            # add to growing sentence!
            sentence += ' '+ldec
record_sentence(sentence, outfile)
outfile.close()
