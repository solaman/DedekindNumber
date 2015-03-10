#=============================================================================================
# Main program: exploring the possible worlds by giving the number of input constraints 
# Including "save_all_worlds" post-processing asp program 
# Input: The number of input constraints 
# Output: All possible worlds, lattice, worlds-assignment, summary view
# Usage: python world-explorer.py N 
# Contacts: Shizhuo Yu
#=============================================================================================
from __future__ import division
from subprocess import call
import sys

# experate all pws
numOfCons = sys.argv[1]
fIn = open("expWorlds.asp","w")
fIn.write("% Define the domain (universe of discourse): 1,2,...\n")
fIn.write("u(1.."+numOfCons+").\n")
fIn.write("% every element is either in or out\n")
fIn.write("i(X) :- u(X), not o(X).\n")
fIn.write("o(X) :- u(X), not i(X).\n")
fIn.close()

# Save all worlds
call("dlv -silent -filter=i,o expWorlds.asp > expWorlds.asp.out", shell=True)
fIn = open("expWorlds.asp.out", "r")
fOut = open("expWorlds_aw.asp", "w")
outList = []
not_EOF = True
line = fIn.readline()
i= 0

while not_EOF:
    preds = []
    #print "i=", i, "line=", line[1:-2]
    preds = line[1:-2].split(", ")
    # print preds
    
    for pred in preds:
        try:
            index = pred.index("(")
            outStr = pred[:index+1] + str(i) + "," + pred[index+1:]
            outList.append(outStr)
        except ValueError:
            print "*WARNING* World", i, "is empty!"
        
    i = i + 1
    line = fIn.readline()    
    if len(line) == 0:
        not_EOF = False

for e in outList:
    fOut.write(e+".\n")

fIn.close()
fOut.close()    

call("dlv -silent -filter=r,g "+ "expWorlds_aw.asp" + " wexp-colors.asp" + " > " + "expWorlds_colors.asp", shell=True)
call("dlv -silent -filter=up "+ "expWorlds_aw.asp" + " wexp-up.asp" + " > " + "expWorlds_up.asp", shell=True)

# generate all lattice
edges = ""
fIn = open("expWorlds_up.asp")
line = fIn.readline()
ups = line[1:-2].split(", ")
for up in ups:
    edges += up.split(",")[0][3:] + "->" + up.split(",")[1][0:-1] + "\n"


color = { "r":"#FF0000", "g":"#00FF00" } 

infile = open("expWorlds_colors.asp", "r")
fAll = open("world_all.dot", "w")
fAll.write("""digraph{
rankdir=BT
node[shape=circle,style=filled,label=""]
edge[dir=none]\n""")

i = 0
rcnt = []
for line in infile:
    outfile = open("world_"+str(i)+".dot", "w")
    outfile.write("""digraph{
rankdir=BT
node[shape=circle,style=filled,label=""]
edge[dir=none]\n""")
    preds = line[1:-2].split(", ")
    if len(rcnt) == 0:
        for e in range(len(preds)):
            rcnt.append(0)
#    print(preds)
    for pred in preds:
        index = pred.index("(")
        outfile.write(pred[index+1:-1] + '[color="' + color[pred[0]] + '"]\n')
        if pred[0] == "r":
            rcnt[preds.index(pred)] += 1
            
    outfile.write(edges + "}")
    outfile.close()
#    call("dot -Tpng " + "world_"+str(i)+".dot" + " -o " + "world_"+str(i)+".png", shell=True)
    i = i + 1

for e in range(len(rcnt)):
    ratio = rcnt[e]/i*100
    if ratio > 50:
        fAll.write(str(e) + "[label=\"red "+ "%.2f"%(ratio) +"%\",color=red]\n")
    elif ratio == 50:
        fAll.write(str(e) + "[label=\""+ "%.2f"%(ratio) +"% of r/g\",color=yellow]\n")
    else:
        fAll.write(str(e) + "[label=\"green "+ "%.2f"%(100-ratio) +"%\",color=green]\n")
fAll.write(edges + "}")
infile.close()
fAll.close()
call("dot -Tpng " + "world_all.dot" + " -o " + "world_all.png", shell=True)
#print rcnt
print "Number of constraints: ", numOfCons
print "Number of possible worlds (Nodes in lattice): ", 2**int(numOfCons)
print "Number of lattice: ", i
print ""