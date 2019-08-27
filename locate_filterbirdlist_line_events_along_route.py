import arcpy
import os
from datetime import datetime
import numpy as np
from pass_birdlist_return_numpyarray import pass_birdlist_return_numpyarray

# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
arcpy.env.overwriteOutput = True

inFcRoutes = os.path.join(arcpy.env.workspace, "lines_routes_distancemts_3857")
inFcPoints = os.path.join(arcpy.env.workspace, "points_3857")

##Fields to query in points FC
##inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']
##theStringUserTime = '2007-01-31 19:30:00'
##theStringUserTime = '2007-01-31 16:00:00'
#User given string list
##Both strings need to be BOTH inside range of MIN and MAX time in TAG_IDENT (each bird)
#theUserDistanceList = [0, 20000]
#theUserDistanceList = [195236.87548523, 781188.70459307]
#print(theStringUserTimeList)
##Field to construct WhereClause using FIELD IN (list)
#fieldDelimiter = 'tag_ident'
fieldDelimiter = 'bird_name'
##List of Birds Identifier. Used to Filter the Dataset
#fieldDelimiterList = ['72364', '72413','72417','73053','73054','79694','79698']
fieldDelimiterList = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']
inFields = [fieldDelimiter, 'timestamp', 'DistanceMts', 'OBJECTID']

## Unique values in fieldDelimiter
#myFieldDelimiterCompleteList = unique_values(inFc , fieldDelimiter)
#fields = [fieldDelimiter, 'distancemts']
## Max and min times in POINTS by TAG_IDENT. Every BIRD min and max times inside POINTS
#min_and_max_distance = min_max_distance(inFc, fields, myFieldDelimiterCompleteList)
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
#myNewFieldDelimiterList = []
#for eachValue in fieldDelimiterList:
#    min_max = min_and_max_distance[eachValue]
#    min_distance = min_max[0]
#    max_distance = min_max[1]
#    if ((theUserDistanceList[0] >= min_distance and theUserDistanceList[0] <= max_distance) \
#        and (theUserDistanceList[1] >= min_distance and theUserDistanceList[1] <= max_distance)):
#        myNewFieldDelimiterList.append(eachValue)

##myResutlNumpyArray,
#myResutlNumpyArray2, fieldForNexFilter, idsForNextFilter = pass_twodistance_return_time(inFc, fieldDelimiter, inFields, theUserDistanceList, myNewFieldDelimiterList)
#pass_birdlist_return_numpyarray(inFc, fieldDelimiter, inFields, fieldDelimiterList)
myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter = pass_birdlist_return_numpyarray(inFcPoints, fieldDelimiter, inFields, fieldDelimiterList)
##print (myResutlNumpyArray)
print (myResutlNumpyArray2)
print (fieldForNextFilter)
print (idsForNextFilter)
##print (myResutlNumpyArray2[0]['tag_ident'])
##print (myResutlNumpyArray2['tag_ident'])
##print (myResutlNumpyArray2['tag_ident'][0])
##print (myResutlNumpyArray2[0]['DistanceMts'])
##print (myResutlNumpyArray2['DistanceMts'])
##print (myResutlNumpyArray2['DistanceMts'][0])
##print (myResutlNumpyArray[0]['DistanceMts'])


theRunName = 'head_all_3857'
#Create a Feature Dataset with theRunName
theDataset = os.path.join(arcpy.env.workspace, theRunName)
if arcpy.Exists(theDataset):
    #arcpy.Delete_management(theDataset)
    print("Dataset exists!")
else:
    arcpy.CreateFeatureDataset_management(arcpy.env.workspace, theRunName, spatial_reference = inFcPoints)


### ONLY LINES TO ALLOCATE
outputLinesEventsTable = os.path.join(arcpy.env.workspace, theRunName + "_birds_lineevents_table_filter0")
if arcpy.Exists(outputLinesEventsTable):
    arcpy.Delete_management(outputLinesEventsTable)
#eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, r"memory\events")
eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, outputLinesEventsTable)

#create a table view from eventsTable
#fields= arcpy.ListFields(eventsTable)
#arcpy.MakeTableView_management(eventsTable, "eventsTableView", "", "", "")
#arcpy.MakeTableView_management(eventsTable, "eventsTableView")
# To persist the layer on disk make a copy of the view
#arcpy.CopyRows_management("crime_view", "C:/temp/newfreq.dbf")
#arcpy.CopyRows_management(eventsTable, outputPointEventsTable)


#myType = np.dtype([('tag_ident','U10'),('eventtype','U10'),('initialdistancemts','d'), ('finaldistancemts','d'), \
#                   ('initialptime','U30'), ('finalptime','U30'), ('initialpointid','i'), ('finalpointid','i')])


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
