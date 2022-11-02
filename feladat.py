import random
import re
import time

"""

Időmérés: 

start_time = time.monotonic()

do_something

print('seconds: ', time.monotonic() - start_time)

"""

PAIR_REGEX = "([2-9TJQKA])[schd].*\\1[schd]"
TWO_PAIR_REGEX = "([2-9TJQKA])[schd].\1[schd].([2-9TJQKA])[schd].*\2[schd]"
DRILL_REGEX = "([2-9TJQKA])[schd].*\\1[schd].*\\1[schd]"
POKER_REGEX = "([2-9TJQKA])[schd](?:.*\\1[schd]){3}"
FLUSH_REGEX = "[2-9TJQKA]([schd])(?:.*[2-9TJQKA]\\1){4}"
DECODER_REGEX = "([0-9])(?=\\w)(\\w)"


def generateInput():
    result = ""
    n = 0
    while n < 40:
        for _ in range(5):
            value = random.choice("23456789TJQKA")
            char = random.choice("schd")
            result += str(value) + char
        result = result + "\n"
        writeFile("input.txt", result)
        n += 1


def readFile(filename):
    result = list()
    with open(filename, "r") as file:
        line = file.readline()
        while line:
            result.append(line.rstrip())
            line = file.readline()
    return result


def count(regex, lista, filename):
    result = {"count": 0, "sorok": []}
    for line in lista:
        if re.search(regex, line):
            result["count"] += 1
            result["sorok"].append(line)
    writeFile(filename, result)


def decoder(regex,lista, filename):
    result = list()
    for line in lista:
        search = re.search(regex, line)
        if search:
            matches = search.group(0)
            first_group = search.group(1)
            second_group = search.group(2)
            replaced_str = ""
            for i in range(int(first_group)):
                replaced_str += second_group
            replaced = line.replace(matches, replaced_str)
            result.append(replaced)
    writeFile(filename, result)


def writeFile(filename, data):
    with open(filename, "w") as file:
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, int):
                    file.write(f"{value} db.\n")
                if isinstance(value, list):
                    for item in value:
                        file.write(f"{item}\n")
        elif isinstance(data, list):
            for item in data:
                file.write(f"{item}\n")
        else:
            file.write(f"{data}")


if __name__ == "__main__":
    generateInput()
    lista = readFile("input.txt")
    count(PAIR_REGEX, lista, "par.txt")
    count(TWO_PAIR_REGEX, lista, "ketpar.txt")
    count(FLUSH_REGEX, lista, "flush.txt")
    count(POKER_REGEX, lista, "poker.txt")
    count(DRILL_REGEX, lista, "drill.txt")
    decoder(DECODER_REGEX, lista, "dekodoltKartyak.txt")

