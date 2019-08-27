import arcpy
import os
from datetime import datetime
import numpy as np
from filter_by_attributes_structured_array import filter_by_fields_where


# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
arcpy.env.overwriteOutput = True

inFcRoutes = os.path.join(arcpy.env.workspace, "lines_routes_distancemts_3857")
inFcPoints = os.path.join(arcpy.env.workspace, "points_3857")

## Unique values in 'tag_ident'
##Points FC

#fieldDelimiter = 'tag_ident'
fieldDelimiter = 'bird_name'


##Fields to query in points FC
##inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']
##inFields = ['bird_name', 'timestamp', 'DistanceMts', 'OBJECTID']
inFields = [fieldDelimiter, 'timestamp', 'DistanceMts', 'OBJECTID']

#fieldDelimiter = 'tag_ident'
fieldDelimiter = 'bird_name'

##fieldDelimiterList = ['72364', '72413', '79694', '79698']
##fieldDelimiterList = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']

fieldDelimiter2 = 'OBJECTID'
fieldDelimiterList2 = list(range(1, 7364))
#fieldDelimiterList2 = list(range(1023, 2474))
#fieldDelimiterList2 = list(range(1023, 2024))
#fieldDelimiter2 = ""
#fieldDelimiterList2 = []

field1 = "ws_mtss"
condition1 = "< 0"
field2 = "vg_mtss"
condition2 = "is not null"

#DO NOT NEEDED to check here MIN and MAX values

myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter, myWhere = filter_by_fields_where(inFcPoints, \
                                        fieldDelimiter, inFields, \
                                        fieldDelimiter2, fieldDelimiterList2, \
                                        field1, condition1, field2, condition2)
print (myResutlNumpyArray2)
print (fieldForNextFilter)
print (idsForNextFilter)
print (myWhere)
##print (myResutlNumpyArray2[0]['tag_ident'])
##print (myResutlNumpyArray2['tag_ident'])
##print (myResutlNumpyArray2['tag_ident'][0])
##print (myResutlNumpyArray2[0]['DistanceMts'])
##print (myResutlNumpyArray2['DistanceMts'])
##print (myResutlNumpyArray2['DistanceMts'][0])
##print (myResutlNumpyArray[0]['DistanceMts'])

#Scenario Name
theRunName = 'head_all_3857'
#Create a Feature Dataset with theRunName
theDataset = os.path.join(arcpy.env.workspace, theRunName)
if arcpy.Exists(theDataset):
    #arcpy.Delete_management(theDataset)
    print("Dataset exists!")
else:
    arcpy.CreateFeatureDataset_management(arcpy.env.workspace, theRunName, spatial_reference = inFcPoints)

### LOCATE LINES
outputLinesEventsTable = os.path.join(arcpy.env.workspace, theRunName+"_attributes_lineevents_table_filter2")
if arcpy.Exists(outputLinesEventsTable):
    arcpy.Delete_management(outputLinesEventsTable)
#eventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2, r"memory\events")
myResutlNumpyArray2Lines = myResutlNumpyArray2[myResutlNumpyArray2["eventtype"] == "LINE"]

linesEventsTable = arcpy.da.NumPyArrayToTable(myResutlNumpyArray2Lines, outputLinesEventsTable)

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
props = fieldDelimiter + " POINT initialdistancemts"
lyr = theRunName + "_attributes_pointevents_lyr_filter2" 

# Execute MakeRouteEventLayer
arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, outputPointsEventsTable, props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")
#arcpy.MakeRouteEventLayer_lr(inFcRoutes, rid, "memory\events", props, lyr, "#", "ERROR_FIELD", "ANGLE_FIELD")

outputPointFC = os.path.join(arcpy.env.workspace, theRunName, theRunName + "_attributes_pointevents_fc_filter2")
if arcpy.Exists(outputPointFC):
    arcpy.Delete_management(outputPointFC)
arcpy.CopyFeatures_management(lyr, outputPointFC)

