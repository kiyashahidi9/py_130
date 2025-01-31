'''
input: a DNA strand, another DNA strand
output: the hamming distance
    - the number of differences between the two

rules:
    - if the two letters are unequal, add to the hamming distance
    - Go only as far as the shorter strand

data/objct structure:

DNA
    __init__(self, strand)
        - self.strand
    
    hamming_distance(strand2)
        - hamming_distance var
        - determines and returns the hamming_distance

ALG:
1. take a DNA strand
2. take a second strand
3. find the len of the shorter one
4. iterate over a range from 0 to the shorter length
5. for each idx, if the letters are not the same, add to hamming_distance
6. return final hamming_distance count

step 3:
1. min(len(strand1), len(strand2))
'''

class DNA:
    def __init__(self, strand):
        self.strand = strand

    def hamming_distance(self, strand2):
        hamming_distance = 0
        shorter_len = min((len(self.strand), len(strand2)))
        
        for idx in range(0, shorter_len):
            if self.strand[idx] != strand2[idx]:
                hamming_distance += 1
        
        return hamming_distance