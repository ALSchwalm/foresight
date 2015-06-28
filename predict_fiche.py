import predict_msvc
import itertools

# 7584    -> 24
# 19164   -> 12
# 25795   -> 19
# 22125   -> 21

# 5828
# 23405
# 27477

values = [24, 12, 19]

possible = [[] for v in values]

for i, l in enumerate(possible):
    for x in range(0, 2**16):
        if x % 36 == values[i]:
            l.append(x)

print [len(l) for l in possible]

for p1 in possible[0]:
    for p2 in possible[1]:
        for p3 in possible[2]:
            if next(predict_msvc.generate_values([p1, p2, p3], a=214013, c=2531011, m=2**31, masked_bits=16, noexcept=True)):
                print("Values: ", p1, p2, p3)

# for i in itertools.islice(:
#     print i
