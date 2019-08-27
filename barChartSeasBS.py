import arcpy
import matplotlib
from matplotlib import pyplot as plt2
import numpy as np
import os

#Get the speed of bird
def autolabel(labelsarray, rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    count = 0
    for rect in rects:        
        height = rect.get_height()
        name = labelsarray[count]
##        ax.annotate('{}'.format(name),
##                    xy=(rect.get_x() + rect.get_width() / 2, height),
##                    xytext=(0, 3),  # 3 points vertical offset
##                    textcoords="offset points",
##                    ha='center', va='bottom')
        ax.text(rect.get_x() + rect.get_width() / 2, height, '{}'.format(name), ha="center", va="bottom", rotation=90, size=6)
        count += 1
        
def dataArr(wspace, myFieldList, at):
    cursor = arcpy.da.SearchCursor(wspace, myFieldList)
    speed = []
    birdname = []
    for row in cursor:
        if row[0] == at:
            speed.append(row[1])
            birdname.append(row[2])
    return speed, birdname

def fixArrays(baselabelsarray, tofixlabelsarray, tofixvaluesarray):
    adjustedvaluesarray = []
    for baslabel in baselabelsarray:
        print("baslabel = ", baslabel)
        found = False
        newvalue = 0
        countfix = 0
        if len(tofixlabelsarray) > 0:
            for fixlabel in tofixlabelsarray:
                print("fixlabel = ", fixlabel)
                if fixlabel == baslabel:
                    barValue = tofixvaluesarray[countfix]
                    print("barValue = ", barValue)
                    found = True
                    newvalue = barValue
                countfix += 1
        adjustedvaluesarray.append(newvalue)
    return adjustedvaluesarray


def createBarChartBirdsSeason (wspace, myFieldList, my_new_file, horizontallabel, verticallabel, mainlabel):
    plt2.style.use('ggplot')    
    at = "Autumn"
    sp = "Spring"
    sm = "Summer"
    wn = "Winter"
    barWidth = 0.25
    VA, birdname = dataArr(wspace, myFieldList, at)
    print("VA = ", VA)
    print("birdname = ", birdname)
    
    VS, birdname1 = dataArr(wspace, myFieldList, sp)
    print("VS = ", VS)
    print("birdname1 = ", birdname1)
    print("Len of VS = ", len(VS))
    
    VSM, birdname2 = dataArr(wspace, myFieldList, sm)
    print("VSM = ", VSM)
    print("birdname2 = ", birdname2)
    
    VWM, birdname3 = dataArr(wspace, myFieldList, wn)
    print("VWM = ", VA)
    print("birdname3 = ", birdname3)
    
    birdnameslist = [birdname, birdname1, birdname2, birdname3]
    print("birdnameslist =", birdnameslist)
    datalist = [VA, VS, VSM, VWM]
    print("datalist =", datalist)
    #maxBirdNameList = max((x) for x in birdnameslist)
    maxBirdNameList = max(birdnameslist, key=len)
    #maxBirdNameList = max(birdnameslist, key=lambda coll: len(coll))
    print("maxBirdNameList =", maxBirdNameList)
    maxLength = max(len(x) for x in datalist)
    print("maxLength = ", maxLength)
    
    VA = fixArrays(maxBirdNameList, birdname, VA)
    print("VA = ", VA)
    VS = fixArrays(maxBirdNameList, birdname1, VS)
    print("VS = ", VS)
    VSM = fixArrays(maxBirdNameList, birdname2, VSM)
    print("VSM = ", VSM)
    VWM = fixArrays(maxBirdNameList, birdname3, VWM)
    print("VWM = ", VWM)
    
    #position of bars on X
    #p1 = np.arange(len(VA))
    p1 = np.arange(maxLength)
    print("p1 =", p1)
    p2 = [x + barWidth for x in p1]
    print("p2 =", p2)
    p3 = [x + barWidth for x in p2]
    print("p3 =", p3)
    p4 = [x + barWidth for x in p3]
    print("p4 =", p4)

    # Make the plot
    g = plt2.figure(0)
    
    plt2.bar(p1, VA, color='#7f6d5f', width=barWidth, edgecolor='white', label='Autumn')
    plt2.bar(p2, VS, color='#557f2d', width=barWidth, edgecolor='white', label='Spring')
    plt2.bar(p3, VSM, color='#2d7f5e', width=barWidth, edgecolor='white', label='Summer')
    plt2.bar(p4, VWM, color='#2d447f', width=barWidth, edgecolor='white', label='Winter')
     
    # Add xticks on the middle of the group bars
    plt2.xlabel(horizontallabel, fontweight='bold')
    plt2.ylabel(verticallabel, fontweight='bold')
    plt2.title(mainlabel, fontweight='bold')
    plt2.xticks([r + 2 * barWidth for r in range(len(VA))], maxBirdNameList)
     
    # Create legend & Show graphic
    plt2.legend()
    #plt.show()
    if arcpy.Exists(my_new_file):
        arcpy.Delete_management(my_new_file)
    g.savefig(my_new_file, dpi = 300)
    plt2.close()

def createBarChartSeasonBirds (wspace, myFieldList, my_new_file, horizontallabel, verticallabel, mainlabel):
    plt2.style.use('ggplot')    
    at = "Autumn"
    sp = "Spring"
    sm = "Summer"
    wn = "Winter"
    
    VA, birdname = dataArr(wspace, myFieldList, at)
    print("VA = ", VA)
    print("birdname = ", birdname)
    
    VS, birdname1 = dataArr(wspace, myFieldList, sp)
    print("VS = ", VS)
    print("birdname1 = ", birdname1)
    print("Len of VS = ", len(VS))
    
    VSM, birdname2 = dataArr(wspace, myFieldList, sm)
    print("VSM = ", VSM)
    print("birdname2 = ", birdname2)
    
    VWM, birdname3 = dataArr(wspace, myFieldList, wn)
    print("VWM = ", VA)
    print("birdname3 = ", birdname3)
    
    birdnameslist = [birdname, birdname1, birdname2, birdname3]
    print("birdnameslist =", birdnameslist)
    datalist = [VA, VS, VSM, VWM]
    print("datalist =", datalist)
    #maxBirdNameList = max((x) for x in birdnameslist)
    maxBirdNameList = max(birdnameslist, key=len)
    #maxBirdNameList = max(birdnameslist, key=lambda coll: len(coll))
    
    print("maxBirdNameList array abajo", maxBirdNameList)
    maxLength = max(len(x) for x in datalist)
    print("maxLength = ", maxLength)
    
    VA = fixArrays(maxBirdNameList, birdname, VA)
    print("VA = ", VA)
    VS = fixArrays(maxBirdNameList, birdname1, VS)
    print("VS = ", VS)
    VSM = fixArrays(maxBirdNameList, birdname2, VSM)
    print("VSM = ", VSM)
    VWM = fixArrays(maxBirdNameList, birdname3, VWM)
    print("VWM = ", VWM)
    
    #position of bars on X
    #p1 = np.arange(len(VA))
    #for val in np.arange(maxLength):
    #    locals()["p"+str(val)] = [val + x for x in range (1/(maxLength+2), 1]
    p1 = [0 + x for x in np.linspace(1/(maxLength+2), 1, maxLength, endpoint=False)]
    print("p1 =", p1)
    p2 = [1 + x for x in np.linspace(1/(maxLength+2),1, maxLength, endpoint=False)]
    print("p2 =", p2)
    p3 = [2 + x for x in np.linspace(1/(maxLength+2),1, maxLength, endpoint=False)]
    print("p3 =", p3)
    p4 = [3 + x for x in np.linspace(1/(maxLength+2),1, maxLength, endpoint=False)]
    print("p4 =", p4)

    barWidth = 1/(maxLength+2)
    
    # Get some pastel shades for the colors
    #colors = plt.cm.BuPu(np.linspace(0, 0.5, maxLength))
   
##    for val in np.arange(maxLength):
##        plt2.bar(eval("p"+str(val)), VA, color='#7f6d5f', width=barWidth, edgecolor='white', label='Autumn')
##
##
##    
##    p1 = np.arange(maxLength)
##    print("p1 =", p1)
##    p2 = [x + barWidth for x in p1]
##    print("p2 =", p2)
##    p3 = [x + barWidth for x in p2]
##    print("p3 =", p3)
##    p4 = [x + barWidth for x in p3]
##    print("p4 =", p4)

    # Make the plot
    h, ax = plt2.subplots()
    
    ax1 = plt2.bar(p1, VA, color='#7f6d5f', width=barWidth, edgecolor='white', label='Autumn')
    autolabel(maxBirdNameList, ax1, ax)
    ax2 = plt2.bar(p2, VS, color='#557f2d', width=barWidth, edgecolor='white', label='Spring')
    autolabel(maxBirdNameList, ax2, ax)
    ax3 = plt2.bar(p3, VSM, color='#2d7f5e', width=barWidth, edgecolor='white', label='Summer')
    autolabel(maxBirdNameList, ax3, ax)
    ax4 = plt2.bar(p4, VWM, color='#2d447f', width=barWidth, edgecolor='white', label='Winter')
    autolabel(maxBirdNameList, ax4, ax)
     
    # Add xticks on the middle of the group bars
    plt2.xlabel(horizontallabel, fontweight='bold')
    plt2.ylabel(verticallabel, fontweight='bold')
    plt2.title(mainlabel, fontweight='bold')
    #plt2.xticks([r + 2 * barWidth for r in range(len(VA))], maxBirdNameList)
    plt2.xticks([0.5,1.5,2.5,3.5,4.5], ["Autumn", "Spring", "Summer", "Winter"])
     
    # Create legend & Show graphic
    plt2.legend()
    #plt.show()
    if arcpy.Exists(my_new_file):
        arcpy.Delete_management(my_new_file)
    h.savefig(my_new_file, dpi = 300)
    plt2.close()

##arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
##arcpy.env.overwriteOutput = True
####
##
##myFieldList = ['season', 'MEAN_vg_mtss', 'bird_name']
##
####Output file locations
##theRunName = 'head_all_3857'
##
##wspace = os.path.join(arcpy.env.workspace, theRunName + '_season_sum_stat')
##if not arcpy.Exists(wspace):
##    print ("Imposible to continue, the file" + wspace + " does not exist!")
##
##
####my_path = folder
##my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
##my_new_dir = os.path.join(my_path, theRunName)
####
##if not os.path.exists(my_new_dir):
##    os.makedirs(my_new_dir)
##
##my_new_file = os.path.join(my_path, theRunName, theRunName + "_barchartbirdseason.png")
##my_new_file2 = os.path.join(my_path, theRunName, theRunName + "_barchartseasonbird.png")
##          
##horizontallabel = 'Seasons'
##verticallabel = 'Vg - Bird Ground Speed'
##mainlabel = 'Bird Speed with seasons of a year - main'
##birds = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']
###birds = ['72364', '72413', '72417', '73053','73054', '79694', '79698']
##
##createBarChartBirdsSeason (wspace, myFieldList, my_new_file, horizontallabel, verticallabel, mainlabel, birds)
##createBarChartSeasonBirds (wspace, myFieldList, my_new_file2, horizontallabel, verticallabel, mainlabel, birds)
##
          
