#!/usr/bin/env python shebang

###this script is to generate a script to interpolate a turn and other commands (like transparency) in chimeraX. It should read in a list of overall chimerax commands and spit out the required interpolation. written for chimerax1.1

#syntax is 20210219_Chimerax_turnandwhat.py file.txt where file.txt is a list of the command you want to interpolate. For things like color, please put the starting color above the turn command, and the ending colour below. Currently have colors in rgb format "rgb(200,40,200)".

# to do CLINTON: add functionality for simultaneous turn-like commands (move, zoom).


##setup

import sys
import math

#defining types of variables. add new variables here depending on expected arguments. Also add below.
colortype=["color"]
transparencytype=["transparency"]
turntype=["turn", "roll"]
zoomtype=["zoom"]

#model-oriented commands - expecting initial and final values for each one.
colorcom={}
transparencycom={}

#camera/stage-oriented commands
turncom={}
zoomcom={}

#rounding function

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def round_special(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)


## read inputs

#add check in case no input supplied

with open(sys.argv[1], 'r') as input_com:
    for line in input_com:
        listd = line.split()
        if listd != []:
            variable = listd[0]
            if variable in colortype :
                rgbcolor=listd[2]
                rgbvalue=rgbcolor[4:-1]
                newrgb=rgbvalue.split(",")
                if listd[1] in colorcom.keys():
                    colorcom[listd[1]].append(newrgb)
                else:
                    colorcom[listd[1]]=[]
                    colorcom[listd[1]].append(newrgb)
            elif variable in transparencytype :
                if listd[1] in transparencycom.keys():
                    transparencycom[listd[1]].append(listd[2])
                else:
                    transparencycom[listd[1]]=[]
                    transparencycom[listd[1]].append(listd[2])
            elif variable in turntype :
                turncom=[]
                turncom.append(listd[0])
                turncom.append(listd[1])
                turncom.append(listd[2])
                turncom.append(listd[3])
            #elif variable in zoomtype :
            #    zoomcom[listd[0]]=[]
            #    zoomcom[listd[0]].append(listd[1])
            #    zoomcom[listd[0]].append(listd[2])
            else:
                print("boop")
        else :
            print("bap")

print(colorcom)
print(transparencycom)





number_of_frames=turncom[3]
print(str(number_of_frames))


##variable output

f = open("output.txt", "w")
count=1

while count <= int(number_of_frames):
    for key in colorcom :
        coloroutred = int(round_special(int(str(colorcom[key][0][0]))+((float(str(colorcom[key][1][0]))-float(str(colorcom[key][0][0])))/int(str(number_of_frames)))*int(count), 0))
        coloroutgreen = int(round_special(int(str(colorcom[key][0][1]))+((float(str(colorcom[key][1][1]))-float(str(colorcom[key][0][1])))/int(str(number_of_frames)))*int(count), 0))
        coloroutblue = int(round_special(int(str(colorcom[key][0][2]))+((float(str(colorcom[key][1][2]))-float(str(colorcom[key][0][2])))/int(str(number_of_frames)))*int(count), 0))
        coloroutcom = "color " + str(key) + " rgb(" + str(coloroutred) + "," + str(coloroutgreen) + "," + str(coloroutblue) + ")"
        f.write(str(coloroutcom) + '\n')
    for key in transparencycom :
        newtransparency = int(round_special(int(str(transparencycom[key][0]))+(((float(str(transparencycom[key][1]))-float(str(transparencycom[key][0])))/float(str(number_of_frames)))*int(count)), 0))
        transparencyoutcom = "transparency " + str(key) + " " + str(newtransparency)
        f.write(str(transparencyoutcom) + '\n')
    turnamount = int(turncom[3])/int(str(number_of_frames))*int(count)
    newturncom = str(turncom[0]) + " " + str(turncom[1]) + " " + str(turncom[2]) + " 1"
    f.write(str(newturncom) + '\n')
    count += 1




f.close()




