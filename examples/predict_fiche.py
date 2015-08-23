from predrng.glibc import rand_r

SYMBOLS = "abcdefghijklmnopqrstuvwxyz0123456789"


def main():
    path_1 = input("First path:")
    path_2 = input("Second path:")
    paths = path_1 + path_2
    outputs = [SYMBOLS.index(letter) for letter in paths]

    gen = rand_r.generate_from_outputs(outputs, len(SYMBOLS))
    print("Next path:", end="")
    for _ in range(4):
        print(SYMBOLS[next(gen)], end="")
    print()

if __name__ == "__main__":
    main()
