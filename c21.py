#!/usr/bin/env python3

# Psuedocode from wikipedia (old version; removed): 
# https://en.wikipedia.org/w/index.php?title=Mersenne_Twister&oldid=209555438
 
class MT19937:
    def _uint32(self, i):
        return i&0xffffffff
        
    def __init__(self, seed):
        self.index = 0
        self.MT = [0]*624
        self.MT[0] = self._uint32(seed)
        for i in range(1,624):            
            self.MT[i] = self._uint32( 0x6c078965*( self.MT[i-1] ^ (self.MT[i-1]>>30) ) + i )

    def set_state(self, MT):
        self.MT = MT

    def temper(self, y):
        y = y^(y>>11)
        y = y^(y<<7)  & 0x9d2c5680
        y = y^(y<<15) & 0xefc60000
        y = y^(y>>18)
        return y
        
    def extractNumber(self):
        if self.index == 0:
            self.generateNumbers()
            
        y = self.temper(self.MT[self.index])
        self.index = (self.index+1)%624
        return y
        
    def generateNumbers(self):
        for i in range(624):
            y = (self.MT[i] & 0x80000000) + ((self.MT[(i+1)%624])&0x7fffffff)
            self.MT[i] = self.MT[(i+397)%624]^(y>>1)
            if y%2!=0: self.MT[i] = self.MT[i]^0x9908b0df
   
if __name__ == '__main__':
    mt_rand = MT19937(123456)
    data = [mt_rand.extractNumber() for i in range(1000)]
    expected = [int(i.strip()) for i in open("c21_data.txt").readlines()]
    assert data == expected





