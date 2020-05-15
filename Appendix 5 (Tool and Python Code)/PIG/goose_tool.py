##
##Libraries
##
import arcpy
import os
from datetime import datetime
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
#Filter by bird (Filter 0)
from pass_birdlist_return_numpyarray import pass_birdlist_return_numpyarray

#Filter by distance and bird (Filter 1)
from pass_twodistances_return_twotimes_tagIdentList_numpyarray import pass_twodistance_return_time
from min_max_distance_by_fielddelimiter import min_max_distance
from min_max_distance_by_fielddelimiter import unique_values
#Filter by time and bird (Filter 1)
from pass_twotimes_return_twodistances_tagIdentList_numpyarray import pass_twotime_return_distance
from min_max_timestamp_by_fielddelimiter import min_max_timestamp
from min_max_timestamp_by_fielddelimiter import unique_values
#Filter by attributes and bird (Filter 2)
from filter_by_attributes_structured_array import filter_by_fields_where
#Create Scatter & Histogram Plot - Hassan Omar 
from scatter_histo import scatter_histo
#Statistics - Som Chaudhuri
from linear_regression import my_lnreg
from correlation import my_cor
from summary_stats import my_stat
from season_summary import my_sumattrb

#Graphics by season - Alexys H Rodriguez
from barChartSeasBS import fixArrays
from barChartSeasBS import autolabel
from barChartSeasBS import createBarChartSeasonBirds

#Graphics by season - Senaid Meles
from barChartSeasBS import dataArr
from barChartSeasBS import createBarChartBirdsSeason
from boxplotWV_Season import dataArr2
from boxplotWV_Season import createBoxPlotSeason

##
##From the tool, get parameters of the user
##
scenario = arcpy.GetParameterAsText(0)
#arcpy.AddIDMessage("INFORMATIVE", 12, "scenario = " + scenario)
#print(scenario)

folder = arcpy.GetParameterAsText(1)
#print(folder)

workspace = arcpy.GetParameterAsText(2)
#print(workspace)

routes = arcpy.GetParameterAsText(3)
#print(routes)

points = arcpy.GetParameterAsText(4)
#print(points)

field = arcpy.GetParameterAsText(5)
#print(field)

birds = eval(arcpy.GetParameterAsText(6))
#print(birds)

infields = eval(arcpy.GetParameterAsText(32))

query0type = arcpy.GetParameterAsText(7)
#query0type = 'Distance'
#query0type = 'Time'
#query0type = 'None'
#print(query0type)

queryrange = eval(arcpy.GetParameterAsText(8))
#print(queryrange)

field1 = arcpy.GetParameterAsText(9)
#print(field1)

whereclause1 = arcpy.GetParameterAsText(10)
#print(whereclause1)

field2 = arcpy.GetParameterAsText(11)
#print(field2)

whereclause2 = arcpy.GetParameterAsText(12)
#print(whereclause2)

segmenttrack = arcpy.GetParameterAsText(13)
#print(segmenttrack)

###Hassan
fieldlistscatterhist = eval(arcpy.GetParameterAsText(14))
#print(fieldlistscatterhist)

horizontallabel = arcpy.GetParameterAsText(15)
#print(horizontallabel)

verticallabel = arcpy.GetParameterAsText(16)
#print(verticallabel)

mainlabel = arcpy.GetParameterAsText(17)
#print(mainlabel)

###Som
#>>> Linear Regression
integeruniqueid = arcpy.GetParameterAsText(18)
dependentvariable = arcpy.GetParameterAsText(19)
independentvariables = eval(arcpy.GetParameterAsText(20))

#>>> Correlation
fieldlistcorrelation = eval(arcpy.GetParameterAsText(28))
#>>> Summary Statistics
summarystatistics = arcpy.GetParameterAsText(29)
#>>> Season Summary Statistics
fieldlistseasonsum2 = eval(arcpy.GetParameterAsText(30))
summarystatistics2 = eval(arcpy.GetParameterAsText(31))

###Senaid Meles
#>>> Graphics by season
fieldsforcursor = eval(arcpy.GetParameterAsText(21))
horizontallabel1 = arcpy.GetParameterAsText(22)
verticallabel1 = arcpy.GetParameterAsText(23)
mainlabel1 = arcpy.GetParameterAsText(24)
fieldsforcursor2 = eval(arcpy.GetParameterAsText(25))
verticallabel2 = arcpy.GetParameterAsText(26)
mainlabel2 = arcpy.GetParameterAsText(27)


##
##Input
##

# Set environment settings
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

inFcRoutes = routes
inFcPoints = points

theRunName = scenario
#Create a Feature Dataset with theRunName
theDataset = os.path.join(workspace, theRunName)
if arcpy.Exists(theDataset):
    #arcpy.Delete_management(theDataset)
    print("Dataset exists!")
else:
    arcpy.CreateFeatureDataset_management(workspace, theRunName, spatial_reference = inFcPoints)


##
##Filter 0: Birds. Happend when in Filter 1 = None, this is query0type = None
##
    
fieldDelimiter = field
#arcpy.AddIDMessage("INFORMATIVE", 12, "infields = " + ", ".join (map(str,infields)))
infields.insert(0, fieldDelimiter)
inFields = infields
#arcpy.AddIDMessage("INFORMATIVE", 12, "inFields = " + ", ".join (map(str,inFields)))
#For 'Distance', 'Time' and 'Attributes' is:
#       inFields = ['bird_name', 'timestamp', 'DistanceMts', 'OBJECTID']
#       inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']


if query0type == 'None': #Only if the user choose 'None'
    #birds = eval(birds)
    #For 'None' in Filter 1, when we are proccessing Filter 0
    #   fieldDelimiterList = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']
    #   fieldDelimiterList = ['72364', '72413', '72417', '73053','73054', '79694', '79698']
    

    myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter = pass_birdlist_return_numpyarray(inFcPoints, fieldDelimiter, inFields, birds)
    ##print (myResutlNumpyArray)
    #print (myResutlNumpyArray2)
    #print (fieldForNextFilter)
    #print (idsForNextFilter)
    #arcpy.AddIDMessage("INFORMATIVE", 12, "inFcPoints = " + str(inFcPoints))
    #arcpy.AddIDMessage("INFORMATIVE", 12, "fieldDelimiter = " + fieldDelimiter)
    #arcpy.AddIDMessage("INFORMATIVE", 12, "myResutlNumpyArray2 = " + ", ".join (map(str,myResutlNumpyArray2)))
    #arcpy.AddIDMessage("INFORMATIVE", 12, "idsForNextFilter = " + ", ".join (map(str,idsForNextFilter)))
    #arcpy.AddIDMessage("INFORMATIVE", 12, "alex-fieldForNextFilter = " + fieldForNextFilter)
    
    ##print (myResutlNumpyArray2[0]['tag_ident'])
    ##print (myResutlNumpyArray2['tag_ident'])
    ##print (myResutlNumpyArray2['tag_ident'][0])
    ##print (myResutlNumpyArray2[0]['DistanceMts'])
    ##print (myResutlNumpyArray2['DistanceMts'])
    ##print (myResutlNumpyArray2['DistanceMts'][0])
    ##print (myResutlNumpyArray[0]['DistanceMts'])

    ##
    ##Save Results of Filter 0: Birds
    ##

    ### ONLY LINES TO ALLOCATE
    outputLinesEventsTable = os.path.join(arcpy.env.workspace, theRunName + "_birds_lineevents_table_filter0")
    if arcpy.Exists(outputLinesEventsTable):
        arcpy.Delete_management(outputLinesEventsTable)
    #eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, r"memory\events")
    eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, outputLinesEventsTable)

    #Create Route Event Layer
    rid = fieldDelimiter 
    props = fieldDelimiter + " LINE initialdistancemts finaldistancemts"
    lyr = theRunName + "_birds_lineevents_lyr_filter0" 

    # Execute MakeRouteEventLayer
    arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, outputLinesEventsTable, props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")
    #arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, "memory\events", props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")

    outputLineFC = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_birds_lineevents_fc_filter0")
    if arcpy.Exists(outputLineFC):
        arcpy.Delete_management(outputLineFC)
    arcpy.CopyFeatures_management(lyr, outputLineFC)

##
##Filter 1 : Filter 0 (Birds) + Filter based on Time or Distance)
##
    
#fieldDelimiter = field
#inFields = [fieldDelimiter, 'timestamp', 'DistanceMts', 'OBJECTID']
#inFields = infields.insert(0, fieldDelimiter)

#For 'Distance', 'Time' and 'Attributes' is:
#       inFields = ['bird_name', 'timestamp', 'DistanceMts', 'OBJECTID']
#       inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']


if query0type != 'None': #Only if the user choose 'Time' or 'Distance'
    #queryrange = eval(queryrange)
    #For 'Distance' is for instance:
    #   theUserDistanceList = [0, 20000]
    #For 'Time' is for instance:
    #   theStringUserTimeList = ['2007-02-01 11:00:00', '2007-03-01 11:00:00']
    if query0type == 'Time':
        queryrangedatetime = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in queryrange]

    #birds = eval(birds)
    #For 'Distance' and 'Time 'is for instance:
    #   fieldDelimiterList = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']
    #   fieldDelimiterList = ['72364', '72413','72417','73053','73054','79694','79698']

    ## Unique values in fieldDelimiter
    myFieldDelimiterCompleteList = unique_values(inFcPoints , fieldDelimiter)
    print(myFieldDelimiterCompleteList)
    if query0type == 'Distance':
        fields = [fieldDelimiter, 'distancemts']
        ## Max and min times in POINTS by 'fieldelimiter'. Every BIRD min and max times inside POINTS
        min_and_max_distance = min_max_distance(inFcPoints, fieldDelimiter, fields, myFieldDelimiterCompleteList)
    elif query0type == 'Time':
        fields = [fieldDelimiter, 'timestamp']
        min_and_max_timestamp = min_max_timestamp(inFcPoints, fieldDelimiter, fields, myFieldDelimiterCompleteList)


    #print(min_and_max_distance)
    ##print(min_and_max_timestamp)
    ##Change string time to datetime
    ##theUserTime = datetime.strptime(theStringUserTime, '%Y-%m-%d %H:%M:%S')
    ##dates_list = [dt.datetime.strptime(date, '"%Y-%m-%d"').date() for date in dates]
    ##theUserTimeList = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in theStringUserTimeList]
    #print (theUserTimeList)
    ##CheckOut tag_idents  with the theUserTimeList outside its time range (min - max)
    ##Both dates given by the user, need to be inside range (min - max)
    ##With this code we will create a new list with only
    ##     the TAG_IDENTS whose time values have inside theUserTime
    ##
    myNewFieldDelimiterList = []
    for eachValue in birds:
        if query0type == 'Distance':
            min_max = min_and_max_distance[eachValue]
            min_distance = min_max[0]
            max_distance = min_max[1]
            if ((queryrange[0] >= min_distance and queryrange[0] <= max_distance) \
                and (queryrange[1] >= min_distance and queryrange[1] <= max_distance)):
                myNewFieldDelimiterList.append(eachValue)        
        elif query0type == 'Time':
            min_max = min_and_max_timestamp[eachValue]
            min_date = datetime.strptime(min_max[0], '%Y-%m-%d %H:%M:%S')
            max_date = datetime.strptime(min_max[1], '%Y-%m-%d %H:%M:%S')
            if ((queryrangedatetime[0] >= min_date and queryrangedatetime[0] <= max_date) and \
                (queryrangedatetime[1] >= min_date and queryrangedatetime[1] <= max_date)):
                myNewFieldDelimiterList.append(eachValue)
        
    #Here the list of birds change with filter by min and max of time or distance
    birds = myNewFieldDelimiterList
    
    ##myResutlNumpyArray,
    if query0type == 'Distance':
        myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter = pass_twodistance_return_time(inFcPoints, \
                            fieldDelimiter, inFields, queryrange, birds)
    elif query0type == 'Time':
        myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter = pass_twotime_return_distance(inFcPoints, \
                            fieldDelimiter, inFields, queryrange, birds)
                        
    ##print (myResutlNumpyArray)
    print (myResutlNumpyArray2)
    print (fieldForNextFilter)
    print (idsForNextFilter)
    arcpy.AddIDMessage("INFORMATIVE", 12, "myResutlNumpyArray2 = " + ", ".join (map(str,myResutlNumpyArray2)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "idsForNextFilter = " + ", ".join (map(str,idsForNextFilter)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "alex-fieldForNextFilter = " + fieldForNextFilter)

    ##print (myResutlNumpyArray2[0]['tag_ident'])
    ##print (myResutlNumpyArray2['tag_ident'])
    ##print (myResutlNumpyArray2['tag_ident'][0])
    ##print (myResutlNumpyArray2[0]['DistanceMts'])
    ##print (myResutlNumpyArray2['DistanceMts'])
    ##print (myResutlNumpyArray2['DistanceMts'][0])
    ##print (myResutlNumpyArray[0]['DistanceMts'])

    ##
    ##Save Results of Filter 0: Birds & Filter 1: Time/Distance/None
    ##

## ONLY LINES TO ALLOCATE
if query0type != 'None':   #Only if the user choose 'Time' or 'Distance' 
    if query0type == 'Distance':
        outputLinesEventsTable = os.path.join(arcpy.env.workspace, theRunName + "_distance_lineevents_table_filter1")
    elif query0type == 'Time':
        outputLinesEventsTable = os.path.join(arcpy.env.workspace, theRunName + "_time_lineevents_table_filter1")

    if arcpy.Exists(outputLinesEventsTable):
        arcpy.Delete_management(outputLinesEventsTable)
    #eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, r"memory\events")
    eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, outputLinesEventsTable)

    #Create Route Event Layer
    rid = fieldDelimiter 
    props = fieldDelimiter + " LINE initialdistancemts finaldistancemts"
    if query0type == 'Distance':
        lyr = theRunName + "_time_lineevents_lyr_filter1" 
    elif query0type == 'Time':
        lyr = theRunName + "_time_lineevents_lyr_filter1" 

    # Execute MakeRouteEventLayer
    arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, outputLinesEventsTable, props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")
    #arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, "memory\events", props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")

    if query0type == 'Distance':
        outputLineFC = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_distance_lineevents_fc_filter1")
    elif query0type == 'Time':
        outputLineFC = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_time_lineevents_fc_filter1")

    if arcpy.Exists(outputLineFC):
        arcpy.Delete_management(outputLineFC)
    arcpy.CopyFeatures_management(lyr, outputLineFC)


##
##Filter 2: Filter based on Attributes. Does not include parameters for list of birds to filter!
##
#if query0type == 'None': #'None' means no Filter 1: Time/Distance/None
                         #If the user choose 'None' there is no previous filter (Filter 1: Time/Distance/None)
                         #this is, there is not list of IDS to use as filter here, comming from previous filter
                         #beaware that here in this filter 'Filter 0 - Birds' will be repeated
    #fieldDelimiter2 = ""
    #fieldDelimiterList2 = []
#else: #Only if the user choose 'Time' or 'Distance'
#fieldDelimiter2 = fieldForNextFilter
#fieldDelimiterList2 = idsForNextFilter

if field1 != "": #and whereclause1 != "": #This filter is done, only if the user fill 'field1' and 'whereclause1'
    #field1 = "ws_mtss"
    condition1 = whereclause1
    arcpy.AddIDMessage("INFORMATIVE", 12, "condition1= " + condition1)
    #field2 = "ws_mtss"
    condition2 = whereclause2

    #def pass_twodistance_return_time(inFc, fieldDelimiter, inFields, theUserDistanceList, fieldDelimiterList):
    #def filter_by_fields_where(inFc, fieldDelimiter, inFields, fieldDelimiterList, fieldDelimiter2 = "", fieldDelimiterList2 = [], field1="", condition1="", field2="", condition2=""):
                         #fieldForNextFilter, idsForNextFilter
    fieldDelimiter2 = fieldForNextFilter
    fieldDelimiterList2 = idsForNextFilter

    arcpy.AddIDMessage("INFORMATIVE", 12, "inFcPoints = " + str(inFcPoints))
    arcpy.AddIDMessage("INFORMATIVE", 12, "fieldDelimiter = " + fieldDelimiter)
    arcpy.AddIDMessage("INFORMATIVE", 12, "inFields = " + ", ".join (map(str,inFields)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "birds = " + ", ".join (map(str,birds)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "fieldDelimiter2 alexysh = " + fieldDelimiter2)
    arcpy.AddIDMessage("INFORMATIVE", 12, "fieldDelimiterList2 = " + ", ".join (map(str,fieldDelimiterList2)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "field1 = " + field1)
    arcpy.AddIDMessage("INFORMATIVE", 12, "condition1 = " + condition1)
    arcpy.AddIDMessage("INFORMATIVE", 12, "field2 = " + field2)
    arcpy.AddIDMessage("INFORMATIVE", 12, "condition2 = " + condition2)

    #               (inFc, fieldDelimiter, inFields, fieldDelimiter2 = "", fieldDelimiterList2 = [], field1="", condition1="", field2="", condition2="")
    myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter, myWhere, myTotal = filter_by_fields_where(\
                    inFcPoints, fieldDelimiter, inFields, fieldDelimiter2, fieldDelimiterList2, field1, condition1, field2, condition2)
    print (myResutlNumpyArray2)
    print (fieldForNextFilter)
    print (idsForNextFilter)
    arcpy.AddIDMessage("INFORMATIVE", 12, "myResutlNumpyArray2 = " + ", ".join (map(str,myResutlNumpyArray2)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "idsForNextFilter = " + ", ".join (map(str,idsForNextFilter)))
    arcpy.AddIDMessage("INFORMATIVE", 12, "myWhere = " + myWhere)
    arcpy.AddIDMessage("INFORMATIVE", 12, "myTotal = " + str(myTotal))
    ##
    ##Save Results of Filter 0: Birds & Filter 2: Attributes. 
    ##

    ### LOCATE LINES
    outputLinesEventsTable = os.path.join(arcpy.env.workspace, theRunName+"_attributes_lineevents_table_filter2")
    if arcpy.Exists(outputLinesEventsTable):
        arcpy.Delete_management(outputLinesEventsTable)
    #eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, r"memory\events")
    myResutlNumpyArray2Lines = myResutlNumpyArray2[myResutlNumpyArray2["eventtype"] == "LINE"]

    linesEventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2Lines, outputLinesEventsTable)

    #Create Route Event Layer
    rid = fieldDelimiter
    props = fieldDelimiter + " LINE initialdistancemts finaldistancemts"
    lyr = theRunName + "_attributes_lineevents_lyr_filter2" 

    # Execute MakeRouteEventLayer
    arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, outputLinesEventsTable, props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")
    #arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, "memory\events", props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")

    outputLineFC = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_attributes_lineevents_fc_filter2")
    if arcpy.Exists(outputLineFC):
        arcpy.Delete_management(outputLineFC)
    arcpy.CopyFeatures_management(lyr, outputLineFC)

    ### LOCATE POINTS
    outputPointsEventsTable = os.path.join(arcpy.env.workspace, theRunName + "_attributes_pointevents_table_filter2")
    if arcpy.Exists(outputPointsEventsTable):
        arcpy.Delete_management(outputPointsEventsTable)
    #eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, r"memory\events")
    myResutlNumpyArray2Points = myResutlNumpyArray2[myResutlNumpyArray2["eventtype"] == "POINT"]

    pointsEventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2Points, outputPointsEventsTable)

    #Create Route Event Layer
    rid = fieldDelimiter
    props = fieldDelimiter + " POINT initialdistancemts"
    lyr = theRunName + "_attributes_pointevents_lyr_filter2" 

    # Execute MakeRouteEventLayer
    arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, outputPointsEventsTable, props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")
    #arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, "memory\events", props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")

    outputPointFC = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_attributes_pointevents_fc_filter2")
    if arcpy.Exists(outputPointFC):
        arcpy.Delete_management(outputPointFC)
    arcpy.CopyFeatures_management(lyr, outputPointFC)

##
##Filter 3: Segmenting Trajectories
##

##
##Hassan Graphics - Use always Filter 0: Birds
##

fc_or_table = inFcPoints

my_path = folder
my_new_file = os.path.join(my_path, theRunName)

if not os.path.exists(my_new_file):
    os.makedirs(my_new_file)
#else:
#    os.rmdir(os.path.join("C:\\", "tmp"))
    
my_new_file = os.path.join(my_path, theRunName, theRunName+"_scatterplot_histo.png")

myFieldList = fieldlistscatterhist #['vg_mtss','ws_mtss'] #first is horizontal and second is vertical
myFieldToFilter = "" #fieldDelimiter #'tag_ident'
myListOfValuesToFilter = [] #birds #['72413', '79694', '79698']
varticalLabel = verticallabel # 'Wind Support (Ws)'
horizontalLabel = horizontallabel #'Bird Ground Velocity (Vg)'
#mainlabel = mainlabel # varticalLabel + " vs. " + horizontalLabel + '\n Histo-Scatter Plot '
field1 = "" #'vg_mtss'
condition1 = "" #whereclause1 #"< 10"
field2 = "" #"ws_mtss"
condition2 = "" #whereclause2 #"is not null and ws_mtss > 0"

myResutl = scatter_histo(fc_or_table, myFieldList, myFieldToFilter, myListOfValuesToFilter, \
                         varticalLabel, mainlabel + " (" + theRunName + ")", horizontalLabel, my_new_file, \
                         field1, condition1, field2, condition2, fieldForNextFilter, idsForNextFilter)

##
##Som Statistical Analysis
##

#>>> Linear Regression
# Unique ID (Created and stored manually in the DB)
u_id = integeruniqueid #'FID'

#Dependent variable
d_var = dependentvariable #'va_mtss'

#Independent variable
i_var = independentvariables # [["vw_mtss"], ["ws_mtss"], ["wc_mtss"], ["vg_mtss"]]

# Argumenets for filter
fc_or_table = points #os.path.join(arcpy.env.workspace, 'points')

## Variables for filter operation
myFieldToFilter = "" #fieldDelimiter #'tag_ident'
##myFieldToFilter = 'bird_name'

myListOfValuesToFilter = [] #birds #['72364', '72413', '72417', '73053', '73054', '79694', '79698']
##myListOfValuesToFilter = birds #['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']


# Output file locations
#theRunName = 'four'
my_path = folder
#my_path = r"C:\Users\SOM\Desktop\Study\WWU Study Notes\Python\Project\Stat Result\"
my_new_dir = os.path.join(my_path, theRunName)

if not os.path.exists(my_new_dir):
    os.makedirs(my_new_dir)
#else:
#    os.rmdir(os.path.join("C:\\", "tmp"))
#Create a Feature Dataset with theRunName
#arcpy.env.workspace = "C:/Users/SOM/Desktop/Study/WWU Study Notes/Python/Project/Data/Test.gdb/"
theDataset = os.path.join(arcpy.env.workspace, theRunName)
if arcpy.Exists(theDataset):
    #arcpy.Delete_management(theDataset)
    print("Dataset exists!")
else:
    arcpy.CreateFeatureDataset_management(arcpy.env.workspace, theRunName, spatial_reference = fc_or_table)
   

data_store = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_regression")
if arcpy.Exists(data_store):
    arcpy.Delete_management(data_store)

coeff_op = os.path.join(arcpy.env.workspace, theRunName + "_reg_coeff")
if arcpy.Exists(coeff_op):
    arcpy.Delete_management(coeff_op)
	
diag_op = os.path.join(arcpy.env.workspace, theRunName + "_reg_diag_op")
if arcpy.Exists(diag_op):
    arcpy.Delete_management(diag_op)
	
res_report = os.path.join(my_path, theRunName, theRunName + "_reg_result.pdf")
if arcpy.Exists(res_report):
    arcpy.Delete_management(res_report)


fieldDelimiter2 = fieldForNextFilter
#arcpy.AddIDMessage("INFORMATIVE", 12, "fieldForNextFilter = " + fieldForNextFilter)
fieldDelimiterList2 = idsForNextFilter
#arcpy.AddIDMessage("INFORMATIVE", 12, "idsForNextFilter = " + ", ".join (map(str,idsForNextFilter)))
# Function Call

mywhere = my_lnreg(fc_or_table, u_id, data_store, d_var, i_var, coeff_op, diag_op, res_report, \
         myFieldToFilter, myListOfValuesToFilter, fieldDelimiter2, fieldDelimiterList2)
#print ("Linear Regression calculated")

#arcpy.AddIDMessage("INFORMATIVE", 12, "mywhere = " + mywhere)

#>>> Correlation

## Variables for filter operation
myFieldList = fieldlistcorrelation #['vw_mtss','ws_mtss', 'wc_mtss', 'vg_mtss', 'va_mtss']
myFieldToFilter = ""
myListOfValuesToFilter = []
corr_report = os.path.join(my_path, theRunName, theRunName+"_correlation.txt")

if arcpy.Exists(corr_report):
    arcpy.Delete_management(corr_report)

#Function Call
cor_res = my_cor(fc_or_table, myFieldList, myFieldToFilter, myListOfValuesToFilter, fieldDelimiter2, fieldDelimiterList2)
##print(cor_res) 
##print(corr_report)
res_str = str(cor_res)
##print(res_str)
file = open(corr_report,"w")
file.write(str(myFieldList)+"\n")
file.write(res_str)
file.close() 
print("Correlation calculated")   

#>>> Summary Statistics
## Defining work environment

summary_report = os.path.join(my_path, theRunName, theRunName+"_summary_stat.csv")

summary_configuration = summarystatistics #"vw_mtss MEAN; vw_mtss MEDIAN; vw_mtss STD; vw_mtss VARIANCE; vg_mtss Mean; vg_mtss MEDIAN; vg_mtss STD; vg_mtss VARIANCE; va_mtss Mean; va_mtss MEDIAN; va_mtss STD; va_mtss VARIANCE"
#Function Call
my_stat(fc_or_table, myFieldToFilter, myListOfValuesToFilter, summary_report, summary_configuration, fieldDelimiter2, fieldDelimiterList2)
#print ("Summary Statistics Table created")

#>>> Season Summary Statistics

theTable = os.path.join(arcpy.env.workspace, theRunName + "_season_sum_stat")
if arcpy.Exists(theTable):
    arcpy.Delete_management(theTable)

## Variables for Summary statistics operation
summaryFields = fieldlistseasonsum2#["season","bird_name"]
summaryStatistics = summarystatistics2 #[["vw_mtss", "MEAN"], ["vw_mtss", "STD"], ["vw_mtss", "VARIANCE"], ["vg_mtss", "MEAN"], ["vg_mtss", "STD"], ["vg_mtss", "VARIANCE"], ["va_mtss", "MEAN"], ["va_mtss", "STD"], ["va_mtss", "VARIANCE"]]
myFieldToFilter = ""
myListOfValuesToFilter = ""
# Function Call
my_sumattrb(fc_or_table, myFieldToFilter, myListOfValuesToFilter, theTable, summaryStatistics, summaryFields, fieldDelimiter2, fieldDelimiterList2)
print ("Summary Statistics Table created")

##
##Senait & Alexys Graphics
##

## >>> Mean Bird Speed By Season By Bird - barChartSeasBS.py
wspace = os.path.join(arcpy.env.workspace, theRunName + "_season_sum_stat")
if not arcpy.Exists(wspace):
    print ("Imposible to continue, the file" + wspace + " does not exist!")

myFieldList = fieldsforcursor #['season', 'MEAN_vg_mtss', 'bird_name']

##Output file locations

my_path = folder
#my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
my_new_dir = os.path.join(my_path, theRunName)
##
if not os.path.exists(my_new_dir):
    os.makedirs(my_new_dir)

my_new_file = os.path.join(my_path, theRunName, theRunName + "_barchartbirdseason.png")
my_new_file2 = os.path.join(my_path, theRunName, theRunName + "_barchartseasonbird.png")

horizontallabel = horizontallabel1 #'Seasons'
verticallabel = verticallabel1 #'Vg - Bird Ground Speed'
mainlabel = mainlabel1 #'Bird Speed with seasons of a year - main'

createBarChartBirdsSeason (wspace, myFieldList, my_new_file, horizontallabel, verticallabel, mainlabel + " (" + theRunName + ")")
createBarChartSeasonBirds (wspace, myFieldList, my_new_file2, horizontallabel, verticallabel, mainlabel + " (" + theRunName + ")")

## >>> Mean Bird Speed and Std Dev by Season - barChartSeasBS.py


myFieldList = fieldsforcursor2 #['season', 'MEAN_vg_mtss', 'bird_name']

#my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
#my_new_dir = os.path.join(my_path, theRunName)
##
#if not os.path.exists(my_new_dir):
#    os.makedirs(my_new_dir)

my_new_file = os.path.join(my_path, theRunName, theRunName + "_boxplotseason.png")

verticallabel1 = verticallabel2 #'Bird Ground Speed - Vg - [Mts/seg]'
mainlabel1 = mainlabel2 #'Average and St. Dev of Vg by Season'

createBoxPlotSeason (wspace, myFieldList, my_new_file, verticallabel1, mainlabel1 + " (" + theRunName + ")")

##
##Damien Plots
##

##Removing Layers of Current Map
doc = arcpy.mp.ArcGISProject('current')
map_obj = doc.listMaps()[0]
for layer in map_obj.listLayers():
    #print (layer.name[0:5])
    if layer.name[0:5] != "Light":
         map_obj.removeLayer(layer)

##outputLineFCfilter0 = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_birds_lineevents_fc_filter0")
##if arcpy.Exists(outputLineFC):
##    layerFilter0 = os.path.join(folder, "lines_filter0.lyrx")
##    myFilter0Layer = map_obj.addDataFromPath(layerFilter0)
##    new_lyr_file = arcpy.mp.LayerFile(layerFilter0)
##    new_lyr = new_lyr_file.listLayers()[0]
##    old_lyr = myFilter0Layer
##    old_lyr_name = old_lyr.name
##    new_lyr.updateConnectionProperties(new_lyr.connectionProperties, old_lyr.connectionProperties)
##    new_lyr.name = old_lyr_name
##    new_lyr_file.save()
##    map_obj.insertLayer(old_lyr, new_lyr_file)
##    map_obj.removeLayer(old_lyr)

##if query0type == 'Distance':
##    outputLineFCfilter01 = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_distance_lineevents_fc_filter1")
##elif query0type == 'Time':
##    outputLineFCfilter01 = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_time_lineevents_fc_filter1")
##elif query0type == 'None':
##    outputLineFCfilter01 = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_birds_lineevents_fc_filter0")
##
##if arcpy.Exists(outputLineFCfilter01):
##    layerFilter01 = os.path.join(folder, "lines_filter0.lyrx")
##    myFilter01Layer = map_obj.addDataFromPath(layerFilter01)
##    new_lyr_file = arcpy.mp.LayerFile(layerFilter01)
##    new_lyr = new_lyr_file.listLayers()[0]
##    old_lyr = myFilter01Layer
##    old_lyr_name = old_lyr.name
##    new_lyr.updateConnectionProperties(new_lyr.connectionProperties, old_lyr.connectionProperties)
##    new_lyr.name = old_lyr_name
##    new_lyr_file.save()
##    map_obj.insertLayer(old_lyr, new_lyr_file)
##    map_obj.removeLayer(old_lyr)
##
##outputLineFCfilter2 = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_attributes_lineevents_fc_filter2")
##if arcpy.Exists(outputLineFCfilter2):
##    layerFilter2 = os.path.join(folder, "lines_flter2.lyrx")
##    myFilter2Layer = map_obj.addDataFromPath(layerFilter2)
##    new_lyr_file = arcpy.mp.LayerFile(layerFilter2)
##    new_lyr = new_lyr_file.listLayers()[0]
##    old_lyr = myFilter2Layer
##    old_lyr_name = old_lyr.name
##    new_lyr.updateConnectionProperties(new_lyr.connectionProperties, old_lyr.connectionProperties)
##    new_lyr.name = old_lyr_name
##    new_lyr_file.save()
##    map_obj.insertLayer(old_lyr, new_lyr_file)
##    map_obj.removeLayer(old_lyr)

##Adding Layers with symbology
#myRoutes = os.path.join(arcpy.env.workspace, "lines_routes_distancemts_3857")
#arcpy.MakeFeatureLayer_management(myRoutes, "routes_lyr")
#my_path = "E:/mg2/PIG2019/final_project/ArcGISPro/"
#layerFileRoutes = os.path.join(my_path, "lines_routes_distancemts.lyrx")
layerFileRoutes = os.path.join(folder, "lines_routes_distancemts.lyrx")
#myRoutesLayer = map_obj.addDataFromPath(myRoutes)
myRoutesLayer = map_obj.addDataFromPath(routes)
myRoutesLayer.name = "Birds Tracks"
#arcpy.ApplySymbologyFromLayer_management(myRoutesLayer, layerFileRoutes)

new_lyr_file = arcpy.mp.LayerFile(layerFileRoutes)
new_lyr = new_lyr_file.listLayers()[0]
old_lyr = myRoutesLayer
old_lyr_name = old_lyr.name
new_lyr.updateConnectionProperties(new_lyr.connectionProperties, old_lyr.connectionProperties)
new_lyr.name = old_lyr_name
new_lyr_file.save()
map_obj.insertLayer(old_lyr, new_lyr_file)
map_obj.removeLayer(old_lyr)

data_store = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_regression")
if arcpy.Exists(data_store):
    myRegressionLayer = map_obj.addDataFromPath(data_store)
    myRegressionLayer.name = "Regression"

for lyt in doc.listLayouts():
    for elm in lyt.listElements("TEXT_ELEMENT"):
       if elm.name == "mytext":
            elm.text = "Linear Regression - Std. Residual\n" + "Scenario: " + theRunName
    
    #dir = os.path.dirname(arcpy.env.workspace)
    mapframe = lyt.listElements("MAPFRAME_ELEMENT")[0]
    #ext = mapframe.camera.getExtent()
    myExt = mapframe.getLayerExtent (myRegressionLayer)
    mapframe.panToExtent(myExt)
    png_file = os.path.join(folder, theRunName, theRunName+ "_map.png")
    if arcpy.Exists(png_file):
        arcpy.Delete_management(png_file)
    lyt.exportToPNG(png_file, 300)
        
#for layer in map_obj.listLayers():
#    if layer.name == myRoutesLayer:
#        # "Refresh" the layer connection properties by setting the new connection = current connection
#        layer.updateConnectionProperties(myRoutesLayer, myRoutesLayer)
#        layer.updateConnectionProperties(myRoutesLayer.name, myRoutesLayer.name)

