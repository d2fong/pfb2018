#!/usr/bin/env python3

# Python 08, problem 4
# ====================
# Now reverse complement each sequence and print out all six
# reading frames to a file called 'Python_08.codons-6frames.nt'

# In order to receive data in the script, given by the user
# from the command line, we need to first make sure we import
# the sys module to access information from the outside system
import sys


# Remember that sys.argv's first position (index 0) contains
# the script name, but we want the second position (index 1).
try:
    fasta_filename = sys.argv[1]
    # an IndexError is raised if sys.argv has fewer than two
    # items in it (i.e., the user has not given a file name)
    if not (fasta_filename.endswith('.fa') or
            fasta_filename.endswith('.nt') or
            fasta_filename.endswith('.fasta')):
        raise Exception("Filename does not end in either .nt, .fa, nor .fasta")

    fasta_filehandle = open(fasta_filename, 'r') 

except Exception as error:  
    print("Error: " + str(error), file=sys.stderr)
    sys.exit(1)

    
# Because python reads files line-by-line, and fasta sequences
# are arranged after their sequence IDs on different lines
# (and not the same lines as the IDs), we need to initialize
# global variables in order for our script to "remember" which
# sequence ID and sequence string we are working with when we
# get to each sequence line
sequence_id = None
sequence_string = ''

valid_nucleotides = set('ATCGN')
complement_table = str.maketrans({'A':'T','C':'G','T':'A','G':'C','N':'N'})

# In order to iterate over all sequences in our file, use a
# "for" loop to read line-by-line:
for line in fasta_filehandle:
    line = line.rstrip()  # strip of ending \n char

    if line.startswith('>'):
        # ...then it's a sequence definition/description line
        if len(sequence_string) > 0:
            # then we have already seen at least one sequence
            # and we must process the previously-stored sequence
            # before we can store the current one, otherwise
            # we will lose a sequence

            for frame in range(3):
                print(sequence_id + "-frame" + str(frame+1) + "-codons")
                
                # set codon seperator character, which adds a space
                # before the next codon. There is no space before the
                # first codon, so initialize to an empty string:
                sep = ''  

                # iterate over every third character in the sequence
                # and use string slicing to extract out three chars
                # at a time:
                for offset in range(0, len(sequence_string), 3):
                    if offset+frame+3 <= len(sequence_string):
                        print("{0}{1}".format(sep, sequence_string[offset+frame:offset+frame+3]), end='')
                        sep=' '
                
                print()  # prints a \n

            sequence_string = sequence_string[::-1].translate(complement_table)
                
            for frame in range(3):
                print(sequence_id + "-frame" + str(frame+4) + "-codons")
                
                # set codon seperator character, which adds a space
                # before the next codon. There is no space before the
                # first codon, so initialize to an empty string:
                sep = ''  

                # iterate over every third character in the sequence
                # and use string slicing to extract out three chars
                # at a time:
                for offset in range(0, len(sequence_string), 3):
                    if offset+frame+3 <= len(sequence_string):
                        print("{0}{1}".format(sep, sequence_string[offset+frame:offset+frame+3]), end='')
                        sep=' '
                
                print()  # prints a \n
                
                
        # and the first set of non-whitespace characters is the
        # sequence ID; everything after the first whitespace
        # represents the sequence comment/description:
        sequence_def = line.lstrip('>').split(' ', maxsplit=1)
        sequence_id = sequence_def[0]
        sequence_string = ''  # make empty again for new sequence
        
    else:
        # this is a sequence line, so let's append the sequence
        # to the sequence_string variable to "grow" out the full
        # sequence
        line = line.upper()
        
        for nucleotide in line:
            if nucleotide not in valid_nucleotides:
                raise Exception("Invalid nucleotide character in {0}: {1}".format(
                    sequence_id, nucleotide
                ))

        sequence_string += line
        

# We've reached the end of the file (EOF), so now print codons for
# the last sequence (if there were any sequences in the file at all):
if len(sequence_string) > 0:
    # then we have already seen at least one sequence
    # and we must process the previously-stored sequence
    # before we can store the current one, otherwise
    # we will lose a sequence
    for frame in range(3):
        print(sequence_id + "-frame" + str(frame+1) + "-codons")
    
        # set codon seperator character, which adds a space
        # before the next codon. There is no space before the
        # first codon, so initialize to an empty string:
        sep = ''  
        
        # iterate over every third character in the sequence
        # and use string slicing to extract out three chars
        # at a time:
        for offset in range(0, len(sequence_string), 3):
            if offset+frame+3 <= len(sequence_string):
                print("{0}{1}".format(sep, sequence_string[offset+frame:offset+frame+3]), end='')
                sep=' '
            
        print()

    sequence_string = sequence_string[::-1].translate(complement_table)
                
    for frame in range(3):
        print(sequence_id + "-frame" + str(frame+4) + "-codons")
        
        # set codon seperator character, which adds a space
        # before the next codon. There is no space before the
        # first codon, so initialize to an empty string:
        sep = ''  
        
        # iterate over every third character in the sequence
        # and use string slicing to extract out three chars
        # at a time:
        for offset in range(0, len(sequence_string), 3):
            if offset+frame+3 <= len(sequence_string):
                print("{0}{1}".format(sep, sequence_string[offset+frame:offset+frame+3]), end='')
                sep=' '
                
        print()  # prints a \n

