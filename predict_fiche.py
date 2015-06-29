import predict_msvc
import itertools

# 365    -> 5
# 1216   -> 28
# 5415   -> 15
# 16704  -> 0

# 24504  -> 24
# 11254  -> 22
# 24698  -> 2
# 1702   -> 10

def msvc_lcg_next(state):
    return predict_msvc.lcg(state, 214013, 2531011, 2**31, 0)

values = [5, 28, 15, 0, 24, 22]

for i in range(2**16):
    if i % 36 == values[0]:
        for j in range(2**16):
            a = i << 16
            a |= j

            next = msvc_lcg_next(a)

            for v in values[1:]:
                if (next >> 16) % 36 == v:
                    next = msvc_lcg_next(next)
                else:
                    break
            else:
                print(next >> 16)
                break
