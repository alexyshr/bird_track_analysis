from __future__ import division
import arcpy
import os
import matplotlib
from matplotlib import pyplot as plt


def scatter_histo(fc_or_table, myFieldList, myFieldToFilter, myListOfValuesToFilter, verticalLabel, mainlabel, \
                  horizontalLabel, my_new_file, field1="", condition1="", field2 = "",condition2= "", \
                  fieldDelimiter2 = "", fieldDelimiterList2 = []):
    whereClause = ""
    if myFieldToFilter != "":
        myStringOfValuesToFilter = "', '".join(myListOfValuesToFilter)
        #whereClause = myFieldToFilter + " IN (" + myStringOfValuesToFilter + ")"
        whereClause = whereClause + "{} IN ('{}')".format(myFieldToFilter, myStringOfValuesToFilter)
    if field1 != "" and condition1!= "":
        if whereClause != "":
            whereClause = whereClause + " And " + field1 + " " + condition1
        elif whereClause == "":
            whereClause = whereClause + field1 + " " + condition1
        if field2 != "" and condition2!= "":
            whereClause = whereClause + " And " + field2 + " " + condition2
        
    if fieldDelimiter2 != "": #and not fieldDelimiterList2: #Note that fieldDelimiter2 need to be INTEGER (not STRING)
        #delimIdFld2 = arcpy.AddFieldDelimiters (fc_or_table, fieldDelimiter2) 
        idStr2 = ", ".join (map(str,fieldDelimiterList2))
        whereClause2 = "{} IN ({})".format (fieldDelimiter2, idStr2) # ID IN (1, 2, 3)
        if whereClause != "":        
            whereClause = whereClause + " And " + whereClause2
        elif whereClause == "":
            whereClause = whereClause + whereClause2
            
    #whereClause = "\"lat\" = '" + my_values + "'"
    grid = plt.GridSpec(2, 3, wspace=0, hspace=0)
    cursor = arcpy.da.SearchCursor(fc_or_table, myFieldList, whereClause)
    horizontalAxes = []
    VerticalAxes = []

    for row in cursor:
        horizontalAxes.append(row[0])
        VerticalAxes.append(row[1])
        
    f = plt.figure(figsize=(6, 6))
    #Defining horizontal ranges
    hor_range = [float(x) for x in horizontalAxes]  
    hor_max = int(max(hor_range))
    hor_min = int(min(hor_range))
##    #Defining vartical ranges
    vart_range = [float(y) for y in VerticalAxes]
    vart_max = int(max(vart_range))
    vart_min = int(min(vart_range))

    
##    plt.style.use('dark_background')
    main_ax = f.add_subplot(grid[:-1, 1:])
    y_hist = f.add_subplot(grid[:-1, 0], xticklabels=[])
    x_hist = f.add_subplot(grid[-1, 1:], yticklabels=[])
    #Main graph
    main_ax.plot(horizontalAxes, VerticalAxes, 'ok', markersize=3, alpha=0.2)
    main_ax.set_yticklabels([])
    main_ax.set_xticklabels([])
    #horizontal graph
    x_hist.hist(horizontalAxes, bins=range(hor_min, hor_max), color='#0504aa', alpha=0.75, rwidth=0.85)
    x_hist.invert_yaxis()
    #vartical graph
    y_hist.hist(VerticalAxes, bins=range(vart_min, vart_max), orientation='horizontal', color='#0504aa', alpha=0.75, rwidth=0.85)
    y_hist.invert_xaxis()

##    tittle = verticalLabel + ' Versus ' + horizontalLabel + '\n Histo-Scatter Plot '
    tittle = mainlabel
##    main_ax.set_axis_bgcolor("lightslategray")
    y_hist.set_ylabel(verticalLabel, fontweight='bold', fontsize='14', horizontalalignment='center')
    x_hist.set_xlabel(horizontalLabel, fontweight='bold', fontsize='14', horizontalalignment='center')
    f.suptitle(tittle, fontsize=17, horizontalalignment='center', fontweight='bold', color = 'orange' )

    if arcpy.Exists(my_new_file):
        arcpy.Delete_management(my_new_file)
    f.savefig(my_new_file, dpi = 300)
    plt.close()

##        plt.show()
        #print('Your result has been saved in D:\GERMANY\MASTER\PYTHON\mine\GOOSE_WITH_WIND\Output')
##arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
##arcpy.env.overwriteOutput = True
##
##fc_or_table = os.path.join(arcpy.env.workspace, "points_3857")
##
###fc_or_table = 'D:/GERMANY/MASTER/PYTHON/project/goose/goose/Test.gdb/points'
##
##theRunName = 'head_all_3857'
#####my_path = folder
##my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
##my_new_dir = os.path.join(my_path, theRunName)
####
##if not os.path.exists(my_new_dir):
##    os.makedirs(my_new_dir)
##
##
##theRunName = 'head_all_3857'
##my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
##my_new_file = os.path.join(my_path, theRunName, theRunName+"_scatterplot_histo.png")
##
##    
##myFieldList = ['vg_mtss','ws_mtss'] #first ishorizontal and second is vertical
###myFieldToFilter = 'tag_ident'
##myFieldToFilter = 'bird_name'
###myListOfValuesToFilter = ['72413', '79694', '79698']
##myListOfValuesToFilter = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']
##verticalLabel = 'Wind Support - Ws [Mts/Sec]'
##horizontalLabel = 'Ground Velocity of the Bird - Vg [Mts/Sec]'
##mainlabel = "Ws vs Vg (" + theRunName + ")"
##field1 = 'ws_mtss'
##condition1 = "< 0"
##field2 = "vg_mtss"
##condition2 = "is not null"
####
##myResutl = scatter_histo(fc_or_table, myFieldList, myFieldToFilter, myListOfValuesToFilter, verticalLabel, mainlabel, horizontalLabel,my_new_file, field1, condition1,field2,condition2)
####    
##
