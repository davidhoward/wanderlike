import random
import math

def roll(n,d):
    return sum((1 + random.randrange(d) for i in xrange(n)))

def roll_attack(n):
    return roll(1,20) + roll(2,n)

NUM_TRIALS = 500
levels = [4,6,8,10]
# for p in levels:
#     print "2d%d vs" % p
#     for k in levels:
#         s = 0
#         s2 = 0
#         for i in xrange(NUM_TRIALS):
#             t = roll(p)-roll(k)
#             s += t
#             s2 += t*t

#         mean = float(s)/NUM_TRIALS
#         var = float(s2)/NUM_TRIALS - (mean*mean)
#         print "\t 2d%d: mean %.4f, std %.4f" % (k, mean, math.sqrt(var))
def test_fight(p,k):
    ph = 5*p
    kh = 5*k
    while ph*kh > 0:
        pr = roll_attack(p)
        kr = roll_attack(k)
        if pr > kr:
            kh -= (pr-kr)
        else:
            ph -= (kr-pr)
    if ph > 0:
        return 1.0
    else:
        return 0.0

MIN_LEVEL=5
MAX_LEVEL=20
for p in xrange(MIN_LEVEL,MAX_LEVEL+1):
    print 'p strength', p
    for k in xrange(p, MAX_LEVEL+1):
        wins = 0.0
        for i in xrange(NUM_TRIALS):
            wins += test_fight(p,k)
        print '\t wins against strength %d: %.4f' % (k, wins/NUM_TRIALS)
        if wins == 0.0:
            break

            
