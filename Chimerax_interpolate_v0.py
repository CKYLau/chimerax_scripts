#!/usr/bin/env python shebang

###this script is to generate a script to interpolate a move-type command and appearance commands (like transparency) in chimeraX. It should read in a list of overall chimerax commands and spit out the required interpolation. written for chimerax1.1

#syntax is Chimerax_turnandwhat.py file.txt where file.txt is a list of the command you want to interpolate. For things like color, please put the starting color above the turn command, and the ending colour below. Currently have colors in rgb format "rgb(200,40,200)".

#current commands supported
    #move-type: move, turn, roll (one command per axis); zoom (one command). Requires at least one move-type command
    #appearance command: color change, transparency change. You can include any number of these, but only model specification per line. e.g. "#1,3/Y:1-24" is fine, but please split "#1/Y #2/A" over two lines.

# to do CLINTON:write out move and zoom and whatever commands up top of output file; allow wait type command for no movement


##setup

import sys
import math

#defining types of variables. add new variables here depending on expected arguments. Also add below.
colortype=["color"]
transparencytype=["transparency"]
turntype=["turn", "roll"]
movetype=["move"]
zoomtype=["zoom"]

#model-oriented commands - expecting initial and final values for each one.
colorcom={}
transparencycom={}

#camera/stage-oriented commands
turncom={}
movecom={}
zoomcom=[]

#calculator_for_number_of_frames

frame_list=[]

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
                #stores color variable as dictionary: key = model number, entries= [[initial rgb], [final rgb]]
                rgbcolor=listd[2]
                rgbvalue=rgbcolor[4:-1]
                newrgb=rgbvalue.split(",")
                if listd[1] in colorcom.keys():
                    colorcom[listd[1]].append(newrgb)
                else:
                    colorcom[listd[1]]=[]
                    colorcom[listd[1]].append(newrgb)
            elif variable in transparencytype :
                #stores transparency as dictionary: key = model number, entries= [initial transp, final transp]
                if listd[1] in transparencycom.keys():
                    transparencycom[listd[1]].append(listd[2])
                else:
                    transparencycom[listd[1]]=[]
                    transparencycom[listd[1]].append(listd[2])
            elif variable in turntype :
                #stores turn as dictionary: key = axis of turn, entries [turn, axis, deg per frame, frames]
                #turncom=[]
                turncom[listd[1]]=[]
                turncom[listd[1]].append(listd[0])
                turncom[listd[1]].append(listd[1])
                turncom[listd[1]].append(listd[2])
                turncom[listd[1]].append(listd[3])
                frame_list.append(listd[3])
            elif variable in movetype :
                #stores move as dictionary: key = axis of move, entries = [move, axis, distance, frames]
                movecom[listd[1]]=[]
                movecom[listd[1]].append(listd[0])
                movecom[listd[1]].append(listd[1])
                movecom[listd[1]].append(listd[2])
                movecom[listd[1]].append(listd[3])   
                frame_list.append(listd[3]) 
            elif variable in zoomtype :
                #stores zoom as list [zoom, zoom mag, frames]
                zoomcom.append(listd[0])
                zoomcom.append(listd[1])
                zoomcom.append(listd[2])
                frame_list.append(listd[2])
            else:
                print("boop")
        else :
            print("beep")

print(colorcom)
print(transparencycom)


#this picks the highest number of frames to template everything against.

number_of_frames=(max(frame_list))

#number_of_frames=turncom[3]

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
    for key in turncom :
        turnamount = float((float(turncom[key][2])*int(turncom[key][3]))/int(number_of_frames))
        newturncom = str(turncom[key][0]) + " " + str(turncom[key][1]) + " " + str(turnamount) + " 1"
        f.write(str(newturncom) + '\n')
    for key in movecom :
        #moveamount=1
        #moveamount = round_special((float((float(movecom[key][2])*int(movecom[key][3]))/int(number_of_frames))),3)
        moveamount = float((float(movecom[key][2])*int(movecom[key][3]))/int(number_of_frames))
        newmovecom = str(movecom[key][0]) + " " + str(movecom[key][1]) + " " + str(moveamount) + " 1"
        f.write(str(newmovecom) + '\n')
    if zoomcom != []:
        zoomamount = float((float(zoomcom[1]))**(1/float(number_of_frames)))
        newzoomcom = str(zoomcom[0]) + " " + str(zoomamount) + " 1"
        f.write(str(newzoomcom) + '\n')
    f.write("wait 1" + '\n')
    count += 1

f.close()




