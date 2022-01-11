import os
import re

# https://regex101.com/r/VkXRye/1

catalogue = {}
occurence = {}

regex = '(?:(^#define))\s+\w+\s+(?:(0{1}\s+)|(?:([+-]{1}\d+))|(?:([1-9]+\w?)))\s*'
path = "./"

def traverseDirectory(path):
    headercounter = 0
    filecounter = 0
    linesread = 0

    os.chdir(path)
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            # check if file is .h
            if '.h' in name:
                headercounter += 1
                # traverse file
                currFile = open(name)
                for line in currFile:
                    linesread += 1
                    if re.match(regex, line):
                        insertIntoCatalogue(name, line)
                        countoccurence(line)
            else:
                filecounter += 1

    printCatalogue(headercounter, filecounter, linesread)


def countoccurence(line):
    define = line.split()
    if define[1] in occurence:
        elm = occurence.get(define[1])
        occurence.update({define[1]: elm + 1})
    else:
        occurence[define[1]] = 1


def insertIntoCatalogue(file, line):
    define = line.split()
    vtuple = (path + file, define[1], define[2])
    # update entry
    if define[1] in catalogue:
        elm = catalogue.get(define[1])
        catalogue.update({define[1]: elm.append(vtuple)})
        # insert entry
    else:
        catalogue[define[1]] = [vtuple]


def printCatalogue(headercounter, filecounter, linesread):
    print("headerfiles found:", headercounter)
    print("files read:", filecounter)
    print("lines read:", linesread)
    print("entries in catalouge:", len(catalogue))
    print("catalogue:")
    for elm in catalogue:
        print(elm, ":", catalogue[elm])
    print("occurences:")
    for occ in occurence:
        print(occ, ":", occurence[occ])

    print()
    print(f'{"CONSTANT":30} {"H-FILE":55} {"VALUE":15}')
    print("=========================================================================================================")
    for cat in catalogue:
        print(f'{catalogue[cat][0][1]:30} {catalogue[cat][0][0]:55} {catalogue[cat][0][2]:15}')



traverseDirectory(path)
