#!/usr/bin/env python3

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode

# Frequency of letters in the english language
# From http://www.data-compression.com/english.html
# ( Well, https://web.archive.org/web/20170918020907/http://www.data-compression.com/english.html )
freqs={'a':0.0651738,'b':0.0124248,'c':0.0217339,'d':0.0349835,'e':0.1041442,'f':0.0197881,'g':0.0158610,'h':0.0492888,'i':0.0558094,'j':0.0009033,'k':0.0050529,'l':0.0331490,'m':0.0202124,'n':0.0564513,'o':0.0596302,'p':0.0137645,'q':0.0008606,'r':0.0497563,'s':0.0515760,'t':0.0729357,'u':0.0225134,'v':0.0082903,'w':0.0171272,'x':0.0013692,'y':0.0145984,'z':0.0007836,' ':0.1918182}

def frequency_error_chi2(string):
    global freqs

    # Get a list of lowercase letters only
    #letters = bytes([i for i in string.lower() if chr(i) in freqs])
    letters = string.lower()    

    # If there are no letters, call it a a -1
    if len(letters) == 0: return -1

    #return sum([freqs[chr(i)] for i in letters if chr(i) in freqs])
    # Calculate the chi^2 error
    # Sum of:  (Diff^2)/Expected
    error = 0
    for i in freqs:
        observed = len([x for x in letters if chr(x) == i])
        expected = (freqs[i])*len(string)
        difference = observed-expected
        error += ((difference**2) / expected) 
    
    return error

def frequency_sum(string):
    global freqs

    # Get a list of lowercase letters only
    letters = bytes([i for i in string.lower() if chr(i) in freqs])
    
    # If there are no letters, call it a a -1
    if len(letters) == 0: return -1

    # Sum of the frequency of each letter
    return sum([freqs[chr(i)] for i in letters if chr(i) in freqs])

def break_single_xor(ciphertext):
    scores = []
    for b in range(0, 255):
        plaintext = bytes([b^i for i in ciphertext])    
        scores.append((frequency_sum(plaintext),b,plaintext))  
        
    winner = max([i for i in scores if i[0]>=0], key = lambda x: x[0])
    return(winner[1])

if __name__ == "__main__":
    ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    ciphertext = unhexlify(ciphertext)
    key = break_single_xor(ciphertext)
    print(bytes([b^key for b in ciphertext]).decode("ascii"))

#print("SCORE\tKEY\tPLAINTEXT\n")
#for i in scores[-5:]:
#     print("%0.2f\t0x%02x\t%s" % (i[0], i[1], i[2]))
