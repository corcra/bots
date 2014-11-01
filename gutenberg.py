#!/bin/python
# I eat books!
# I give you tweets!
# READ A BOOOK READ A BOOK
# READ A MOTHERFUCKING BOOK
import math
import re
import sys

if len(sys.argv)<2:
    sys.exit('USAGE: twittify.py filepath')
infile = open(sys.argv[1],'r')
outfile = open(sys.argv[1]+'.twit','w')

# --- options --- #
encoding = 'utf-8'
global MAXLENGTH, MINLENGTH
MAXLENGTH, MINLENGTH = 135, 50

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
        
def record_sentence(sentence, outfile):
    sentence = re.sub('  ',' ',sentence)
    if len(sentence) > 0:
        # prep the sentence a little
        sen = sentence.lstrip(' ') 
        if len(sen) < MAXLENGTH:
            # all goood!
            print 'RECORDING...', sen.encode(encoding)
            outfile.write(sen.encode(encoding)+'\n')
        else:
            # need to split it up
            split_sen = twitter_split(sen, MAXLENGTH-20)
            print 'RECORDING...', split_sen.encode(encoding)
            outfile.write(split_sen.encode(encoding)+'\n')
    return True

sentence = ''
for line in infile:
    ldec = line.decode(encoding).strip().strip(' ')
    if len(ldec) == 0:
        # empty, probably a paragraph break
        record_sentence(sentence, outfile)
        sentence = ''
    else:
        # not empty
        if '. ' in ldec or '? ' in ldec or '! ' in ldec:
            sentence += ' '
            # get until there
            punctuation = [-1] + [n.start() for n in re.finditer('[\.?!] ', ldec)] + [len(ldec)-1]
            fragments = [ldec[(punctuation[k-1]+1):(punctuation[k]+1)] for k in xrange(1,len(punctuation))]
            for f in xrange(len(fragments)):
                sentence += fragments[f]
                if not f == len(fragments)-1:
                    if len(sentence) > MINLENGTH:
                        print 'minlength!'
                        print sentence
                        print len(sentence)
                        record_sentence(sentence, outfile)
                        sentence = ''
                    if len(sentence)+len(fragments[f+1]) > MAXLENGTH:
                        print 'wayo'
                        print sentence
                        # record before we hit the max length
                        record_sentence(sentence, outfile)
                        sentence = ''
            print 'whut'
            print sentence
        else:
            # add to growing sentence!
            sentence += ' '+ldec
record_sentence(sentence, outfile)
outfile.close()
