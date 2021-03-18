This script is to generate a script to interpolate a move-type command and appearance commands (like transparency) in ChimeraX. It will read in a list of overall chimerax commands and spit out the required interpolation. Written for UCSF ChimeraX1.1.

Syntax is "ChimeraX_interpolate_v0.py file.txt", where file.txt is a list of the command you want to interpolate. 

For appearance commands like color, please put the starting color above the turn command, and the ending colour below. Currently have colors in rgb format "rgb(200,40,200)". Please see testcom.txt for an example of input commands to interpolate.

Current commands supported
    move-type: move, turn; zoom (one command). Requires at least one move-type command
    appearance command: color, transparency. You can include any number of these, but only model specification per line. e.g. "#1,3/Y:1-24" is fine, but please split "#1/Y #2/A" over two lines.


Written by Clinton Lau, clau@mrc-lmb.cam.ac.uk.
