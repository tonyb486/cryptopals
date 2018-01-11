#!/usr/bin/env python3

from c21 import MT19937
import time, random


def get_token():
    time.sleep(random.randrange(40,1000))
    mt_rand = MT19937(int(time.time()))
    time.sleep(random.randrange(40,1000))
    return mt_rand.extractNumber()
    
if __name__ == '__main__':    
    token = get_token()
    
    # We know the PRNG was seeded in the past, say
    # 1000 seconds or so. So work backwards from the
    # present, until we generate the same token 
    
    now = int(time.time())
    for i in range(0,1500):
        mt_rand = MT19937(now-i)
        if token == mt_rand.extractNumber():
            print("Seed Found: %d" % (now-i))
            print("PRNG Was Seeded at %s" % time.strftime("%c", time.localtime(now-i)))
            break



