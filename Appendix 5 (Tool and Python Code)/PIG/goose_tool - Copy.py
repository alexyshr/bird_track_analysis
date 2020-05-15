##
##Libraries
##
import arcpy
import os
from datetime import datetime
import numpy as np
#Filter by distance
from pass_twodistances_return_twotimes_tagIdentList_numpyarray import pass_twodistance_return_time
from min_max_distance_by_fielddelimiter import min_max_distance
from min_max_distance_by_fielddelimiter import unique_values
#Filter by time
from pass_twotimes_return_twodistances_tagIdentList_numpyarray import pass_twotime_return_distance
from min_max_timestamp_by_fielddelimiter import min_max_timestamp
from min_max_timestamp_by_fielddelimiter import unique_values
#Filter by attributes
from filter_by_attributes_structured_array import filter_by_fields_where

##
##From the tool, get parameters of the user
##
scenario = arcpy.GetParameterAsText(0)
#arcpy.AddIDMessage("INFORMATIVE", 12, scenario)
arcpy.AddIDMessage("INFORMATIVE", 12, "scenario = " + scenario)
print(scenario)

folder = arcpy.GetParameterAsText(1)
print(folder)

workspace = arcpy.GetParameterAsText(2)
print(workspace)

routes = arcpy.GetParameterAsText(3)
print(routes)

points = arcpy.GetParameterAsText(4)
print(points)

field = arcpy.GetParameterAsText(5)
print(field)

birds = arcpy.GetParameterAsText(6)
print(birds)

query0type = arcpy.GetParameterAsText(7)
#query0type = 'Distance'
#query0type = 'Time'
#query0type = 'None'
print(query0type)

queryrange = arcpy.GetParameterAsText(8)
print(queryrange)

field1 = arcpy.GetParameterAsText(9)
print(field1)

whereclause1 = arcpy.GetParameterAsText(10)
print(whereclause1)

field2 = arcpy.GetParameterAsText(11)
print(field2)

whereclause2 = arcpy.GetParameterAsText(12)
print(whereclause2)

segmenttrack = arcpy.GetParameterAsText(13)
print(segmenttrack)
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
##Filter 0: Birds & Filter 1: Time/Distance/None
##
    
fieldDelimiter = field
inFields = [fieldDelimiter, 'timestamp', 'DistanceMts', 'OBJECTID']
#For 'Distance', 'Time' and 'Attributes' is:
#       inFields = ['bird_name', 'timestamp', 'DistanceMts', 'OBJECTID']
#       inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']


if query0type != 'None': #Only if the user choose 'Time' or 'Distance'
    queryrange = eval(queryrange)
    #For 'Distance' is for instance:
    #   theUserDistanceList = [0, 20000]
    #For 'Time' is for instance:
    #   theStringUserTimeList = ['2007-02-01 11:00:00', '2007-03-01 11:00:00']
    if query0type == 'Time':
        queryrangedatetime = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in queryrange]

    birds = eval(birds)
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
        

    ##myResutlNumpyArray,
    if query0type == 'Distance':
        myResutlNumpyArray2, fieldForNexFilter, idsForNextFilter = pass_twodistance_return_time(inFcPoints, \
                            fieldDelimiter, inFields, queryrange, myNewFieldDelimiterList)
    elif query0type == 'Time':
        myResutlNumpyArray2, fieldForNexFilter, idsForNextFilter = pass_twotime_return_distance(inFcPoints, \
                            fieldDelimiter, inFields, queryrange, myNewFieldDelimiterList)
                        
    ##print (myResutlNumpyArray)
    print (myResutlNumpyArray2)
    print (fieldForNexFilter)
    print (idsForNextFilter)

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
##Filter 0: Birds & Filter 2: Attributes. Be aware that Filter 0: Birds is repeated here!
##
if query0type == 'None': #'None' means no Filter 1: Time/Distance/None
                         #If the user choose 'None' there is no previous filter (Filter 1: Time/Distance/None)
                         #this is, there is not list of IDS to use as filter here, comming from previous filter
                         #beaware that here in this filter 'Filter 0 - Birds' will be repeated
    fieldDelimiter2 = ""
    fieldDelimiterList2 = []
else: #Only if the user choose 'Time' or 'Distance'
    fieldDelimiter2 = fieldForNexFilter
    fieldDelimiterList2 = idsForNextFilter

if field1 != "" and whereclause1 != "": #This filter is done, only if the user fill 'field1' and 'whereclause1'
    #field1 = "ws_mtss"
    condition1 = whereclause1
    #field2 = "ws_mtss"
    condition2 = whereclause1

    #def pass_twodistance_return_time(inFc, fieldDelimiter, inFields, theUserDistanceList, fieldDelimiterList):
    #def filter_by_fields_where(inFc, fieldDelimiter, inFields, fieldDelimiterList, fieldDelimiter2 = "", fieldDelimiterList2 = [], field1="", condition1="", field2="", condition2=""):
    myResutlNumpyArray2, fieldForNexFilter, idsForNextFilter = filter_by_fields_where(inFcPoints, \
                                            fieldDelimiter, inFields, birds, \
                                            fieldDelimiter2, fieldDelimiterList2, \
                                            field1, condition1, field2, condition2)
    print (myResutlNumpyArray2)
    print (fieldForNexFilter)
    print (idsForNextFilter)

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
##Senait Graphics
##

##
##Hassan Graphics
##

##
##Som Statistical Analysis
##


##
##Damien Plots
##

