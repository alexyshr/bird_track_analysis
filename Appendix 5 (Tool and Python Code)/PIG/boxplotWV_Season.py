import arcpy
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import os

#Get the speed of bird and speed of wind
def dataArr2(wspace, myFieldList, at):
    cursor = arcpy.da.SearchCursor(wspace, myFieldList)
    speed = []
    for row in cursor:
        if row[0] == at:
            speed.append(row[1])
    return speed


def createBoxPlotSeason (wspace, myFieldList, my_new_file, verticallabel, mainlabel): 
    plt.style.use('ggplot')
    #wspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/season_sum_stat"
    #myFieldList = ['season','MEAN_vg_mtss']
    at = "Autumn"
    sp = "Spring"
    sm = "Summer"
    wn = "Winter"

    VA = np.array(dataArr2(wspace, myFieldList, at))
    VS = np.array(dataArr2(wspace, myFieldList, sp))
    VSM = np.array(dataArr2(wspace, myFieldList, sm))
    VWM = np.array(dataArr2(wspace, myFieldList, wn))

    Autumn_mean = np.mean(VA)
    Spring_mean = np.mean(VS)
    Summer_mean = np.mean(VSM)
    Winter_mean = np.mean(VWM)

    Autumn_std = np.std(VA)
    Spring_std = np.std(VS)
    Summer_std = np.std(VSM)
    Winter_std = np.std(VWM)

    seasons = ['VA', 'VS', 'VSM', 'VWM']
    x_pos = np.arange(len(seasons))
    means = [Autumn_mean, Spring_mean, Summer_mean, Winter_mean]
    error = [Autumn_std, Spring_std, Summer_std, Winter_std]
    xlabel = ['Autumn', 'Spring', 'Summer', 'Winter']
    #plot
    fig3, ax = plt.subplots()
    ax.bar(x_pos, means, yerr=error, align='center', alpha=0.5, ecolor='red', capsize=10)
    ax.set_ylabel(verticallabel) #'Speed of the wind')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xlabel)
    ax.set_title(mainlabel) #'Wind Speed and Seasons of a year')
    ax.yaxis.grid(True)
    # Save the figure and show
    plt.tight_layout()
    #plt.show()
    if arcpy.Exists(my_new_file):
        arcpy.Delete_management(my_new_file)    
    fig3.savefig(my_new_file)
    plt.close()

##arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
##arcpy.env.overwriteOutput = True
##
######Output file locations
##theRunName = 'head_all_3857'
####my_path = folder
##my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
##my_new_dir = os.path.join(my_path, theRunName)
####
##if not os.path.exists(my_new_dir):
##    os.makedirs(my_new_dir)
##    
##wspace = os.path.join(arcpy.env.workspace, theRunName + '_season_sum_stat')
###wspace = os.path.join(arcpy.env.workspace, 'season_sum_stat_Statistics')
##
##if not arcpy.Exists(wspace):
##    print ("Imposible to continue, the file" + wspace + " does not exist!")
##
##myFieldList = ['season', 'MEAN_vg_mtss', 'bird_name']
###myFieldList = ['season', 'MEAN_MEAN_vg_mtss']
##
##my_new_file = os.path.join(my_path, theRunName, theRunName + "_boxplotseason.png")
##
##verticallabel1 = 'Bird Ground Speed - Vg - [Mts/seg]'
##
##mainlabel1 = 'Average and St. Dev of Vg by Season'
##
##createBoxPlotSeason (wspace, myFieldList, my_new_file, verticallabel1, mainlabel1)
