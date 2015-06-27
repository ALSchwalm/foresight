
# from password.c
#   max_value = 0x3FFFFFFFL
#   max_value_dbl=(double) rand_st->max_value;

# from my_rnd.cc
#   rand_st->seed1= (rand_st->seed1*3+rand_st->seed2) % rand_st->max_value;
#   rand_st->seed2= (rand_st->seed1+rand_st->seed2+33) % rand_st->max_value;
#   return (((double) rand_st->seed1) / rand_st->max_value_dbl);

# simplified:
#   seed1 = (seed1 * 3 + seed2) % 0x3FFFFFFFL
#   seed2 = (seed1 + seed2 + 33) % 0x3FFFFFFFL
#   return seed1 / 0x3FFFFFFFL

#                                  start of execution
# 0.61914388706828 -> 664800686    seed1 = ?            seed2 = ?
# 0.93845168309142 -> 1007654821   seed1 = 664800686    seed2 = 86994586
# 0.83482678498591 -> 896388434    seed1 = 1007654821   seed2 = 1094649440

# (664800686 * 3 + x) % 0x3FFFFFFFL = 1007654821
# seed2 = 86994586

# output3 = (1007654821 * 3 + 1094649440) mod 0x3FFFFFFF

values = [0.61914388706828, 0.93845168309142]
values = [v * 0x3FFFFFFF for v in values]

seed1 = values[0]
seed2 = None

for x in range(2**30):
    if (seed1 * 3 + x) % 0x3FFFFFFF == values[1]:
        seed2 = x
        break

print seed1, seed2

def find_second_seed(seed1, output2):
    for i in range(100000):
        possible = i * 0x3FFFFFFF + output2
        if  (seed1 * 3 + possible) % 0x3FFFFFFF == output2:
            print possible
