from PIL import Image
import predict_msvc
import itertools

def get_primary_colors(image, section, threshold=40):
    pixels = image.load()
    size = image.size
    colors = {}

    for x in range(section * size[0]//5, (section+1) * size[0]//5):
        for y in range(size[1]):
            if pixels[x, y] in colors.keys():
                colors[pixels[x, y]] += 1
            else:
                colors[pixels[x, y]] = 1

    primary = {color:count for (color, count) in colors.items() if count > threshold}
    return sorted(primary, key=primary.get)

def php_zts_lcg_next(state):
    return predict_msvc.lcg(state, 214013, 2531011, 2**31, 0)

PHP_RAND_MAX = 1<<15

def transform(n, a, b, M=PHP_RAND_MAX):
    return a + int((b-a+1)*n/(M+1));

image = Image.open("captcha.png")

colors = [get_primary_colors(image, i)[0] for i in range(5)]

values = []
for r,g,b,_ in colors[:-1]:
    values += [r, g, b]
    values += [None]*3 # three calls to rand() between color selection

values = values[:-1]

result=None
for i in range(2**16):
    if result is not None:
        break
    if transform(i, 0, 255) == values[0]:
        for j in range(2**16):
            a = i << 16
            a |= j

            next = php_zts_lcg_next(a)

            for v in values[1:]:
                if v is None:
                    next = php_zts_lcg_next(next)
                    continue

                if transform(next >> 16, 0, 255) == v:
                    next = php_zts_lcg_next(next)
                else:
                    break
            else:
                print(next)
                result=next
                break

CHARACTERS="2346789abcdefghjmnpqrtuxyzABCDEFGHJMNPQRTUXYZ"
state=732375767
for i in range(5):
    index = transform(state >> 16, 0, len(CHARACTERS)-1)
    print(CHARACTERS[index])
    state=php_zts_lcg_next(state)
