import os
import re
import sys

# https://regex101.com/r/VkXRye/1

catalogue = {}
occurence = {}
countoccurence = {}

regex = '(?:(^#define))\s+\w+\s+(?:(0{1}\s+)|(?:([+-]{1}\d+))|(?:([1-9]+\w?)))\s*'
path = "/usr/include"


def traverseDirectory(path):
    headercounter = 0
    filecounter = 0
    linesread = 0

    os.chdir(path)
    for root, dirs, files in os.walk(path):
        for name in files:
            # check if file is .h
            if name.endswith(".h"):
                headercounter += 1
                # traverse file
                try:
                    currFile = open(name)
                    for line in currFile:
                        linesread += 1
                        if re.match(regex, line):
                            insertIntoCatalogue(name, line)
                            countoccurence(line)
                        else:
                            filecounter += 1
                except FileNotFoundError:
                    pass
                    #print("File not found:", name)


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
    vtuple = (path + "/" + file, define[1], define[2])
    # update entry
    if define[1] in catalogue:
        elm = catalogue.get(define[1])
        elm.append(vtuple)
        # insert entry
    else:
        catalogue[define[1]] = [vtuple]


def printCatalogue(headercounter, filecounter, linesread):
    sys.stdout=open("/home/student/Dokumente/Labor6/info.log", "w")
    ctnr2 = 0
    print(f'{"Directory Path":75}', path)
    print(f'{"Number of h-files:":75}', headercounter)
    print(f'{"Files read:":75}', filecounter)
    print(f'{"Lines read:":75}', linesread)
    print(f'{"Number of different Constant identifiers:":75}', len(catalogue))

    printoccurences()
    printstats()

    sys.stdout.close()


def printstats():
    print()
    print(f'{"CONSTANT":40} {"H-FILE":55} {"VALUE":15}')
    print("=========================================================================================================")
    for cat in catalogue:
        cntr2 = 0
        for tac in catalogue[cat]:
            cntr2 += 1
            if cntr2 == 1:
                print(f'{tac[1]:40} {tac[0]:55} {tac[2]:15}')
            else:
                print(f'{"":40} {tac[0]:55} {tac[2]:15}')


def printoccurences():
    countoccurence = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for oc in occurence:
        if occurence[oc] >= 5:
            countoccurence[5] += 1
        if occurence[oc] == 4:
            countoccurence[4] += 1
        if occurence[oc] == 3:
            countoccurence[3] += 1
        if occurence[oc] == 2:
            countoccurence[2] += 1
        if occurence[oc] == 1:
            countoccurence[1] += 1

    for key in countoccurence:
        if key == 5:
            print(f'{"":5}{" - - - identifiers appearing ":1}{key:1}{"+ times:":5}{countoccurence[key]:37}')
        else:
            print(f'{"":5}{" - - - identifiers appearing ":1}{key:1}{"  times:":5}{countoccurence[key]:37}')

traverseDirectory(path)
