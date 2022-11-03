import random
import re
from pathlib import Path

"""
10 pont: A program fájlon dolgozik fájlból olvas be egy listába és az eredményeket is fájlba írja ki mint absolute és relativ path-el.
10 pont: Van capturing group illesztés.
10 pont: Mivel van capturing group ahhoz kell backreferenc is és az is van.
10 pont: Van egy kártyalap dekóder amibe található pozitív lookahead.
Szerintem ez összesen 40 pont.
"""

PAIR_REGEX = "([2-9TJQKA])[schd].*\\1[schd]"
TWO_PAIR_REGEX = "([2-9TJQKA])[schd].\1[schd].([2-9TJQKA])[schd].*\2[schd]"
DRILL_REGEX = "([2-9TJQKA])[schd].*\\1[schd].*\\1[schd]"
POKER_REGEX = "([2-9TJQKA])[schd](?:.*\\1[schd]){3}"
FLUSH_REGEX = "[2-9TJQKA]([schd])(?:.*[2-9TJQKA]\\1){4}"
DECODER_REGEX = "([0-9])(?=\\w)(\\w)"

"""
Véletlenszerű input fájl generálás
""" 
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

"""
readFile függvény aminek a segítségével egy fájlból olvasunk be adatokat egy listába
:param filename: Fájl neve amiből olvasni szeretnénk
:return: lista amiben a fájlban lévő adatok vannak
"""
def readFile(filename):
    result = list()
    with open(filename, "r") as file:
        line = file.readline()
        while line:
            result.append(line.rstrip())
            line = file.readline()
    return result

"""
Count függvény aminek a segítségével egy listában olyan sorokat keresünk amelyre a megadott regex illeszkedik
:param regex: Az illeszteni kívánt regex
:param lista: Lista ami tartalmazza a kártya lapokat soronként
:param: filename: Fájl neve ahova beszeretnénk írni az eredményt
"""
def count(regex, lista, filename):
    result = {"count": 0, "sorok": []}
    for line in lista:
        if re.search(regex, line):
            result["count"] += 1
            result["sorok"].append(line)
    writeFile(filename, result)

"""
decoder függvény aminek a segítségével dekódoljuk a kártyalapokat
:param regex: Regex amire illeszteni szeretnénk a listába lévő sorokat
:param lista: Lista amibe a kártyalapok vannak eltárolva
:param filename: Fájl neve ahova az eredményt szeretnénk beírni 
"""
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

"""
writeFile függvény ami segítségével fájlba írunk ki adatokat
:param filename: A fájl neve amibe írni szeretnénk
:param data: Az adat amit kiszeretnénk írni ez lehet dictionary, lista vagy sima szöveg
"""
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
    """Abszolút path"""
    #path = Path('input.txt').absolute()
    #lista = readFile(path)
    lista = readFile("input.txt")
    count(PAIR_REGEX, lista, "par.txt")
    count(TWO_PAIR_REGEX, lista, "ketpar.txt")
    count(FLUSH_REGEX, lista, "flush.txt")
    count(POKER_REGEX, lista, "poker.txt")
    count(DRILL_REGEX, lista, "drill.txt")
    decoder(DECODER_REGEX, lista, "dekodoltKartyak.txt")
    

