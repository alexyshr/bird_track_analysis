# Import system modules
import arcpy
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
from min_max_distance_by_fielddelimiter import min_max_distance
from min_max_distance_by_fielddelimiter import unique_values
from min_max_timestamp_by_fielddelimiter import min_max_timestamp
from min_max_ids_by_fielddelimiter import min_max_ids

# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
#arcpy.env.workspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "ArcGISPro", "Test.gdb")
arcpy.env.overwriteOutput = True

#inFc >> Points FC
#fieldDelimiter >> Field to construct WhereClause using FIELD IN (list)
#inFields >> Fields to select inside the SearchCursor
#theStringUserTime >> String with time (User Given). This time need to be transfor to distance
#fieldDelimiterList >> Array with the list of tag_ident (birds identifier) to query for distance
#                   based in time. Is used to construct the filter (WhereClause) in SearchCursor
def pass_birdlist_return_numpyarray(inFc, fieldDelimiter, inFields, fieldDelimiterList):
    delimIdFld = arcpy.AddFieldDelimiters (inFc, fieldDelimiter)
    idStr = "', '".join (fieldDelimiterList)
    whereClause = "{} IN ('{}')".format (delimIdFld, idStr) # ID IN ('1', '2', '3')
    #print(whereClause)
    #whereClause = "\"tag_ident\" = '" + theTagIdent + "'"
    #theUserTime = datetime.strptime(theStringUserTime, '%Y-%m-%d %H:%M:%S')
    #theUserDistanceInitial = theUserDistanceList[0]
    #theUserDistanceFinal = theUserDistanceList[1]
    #theUserTimeList = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in theStringUserTimeList]
    val = []
    listOfIds = []
    #myType = np.dtype([('tag_ident','U10'),('EventType','U10'),('InitialDistanceMts','d'), ('FinalDistanceMts','d')])
    # declare empty array, zero rows but one column
    #myArr = np.empty([0,1],dtype=myType)
    #myArray = np.empty(0, dtype=myType) #, order='C')
    #contador = 0
    fields = [fieldDelimiter, 'OBJECTID']
    min_max_ids1 = min_max_ids(inFc, fieldDelimiter, fields, fieldDelimiterList)
    #print (min_max_ids1)
    fields = [fieldDelimiter, 'timestamp']
    min_and_max_timestamp1 = min_max_timestamp(inFc, fieldDelimiter, fields, fieldDelimiterList)
    #print (min_and_max_timestamp1)
    fields = [fieldDelimiter, 'distancemts']
    min_max_distance1 = min_max_distance(inFc, fieldDelimiter, fields, fieldDelimiterList)
    #print(min_max_distance1)

    #fieldDelimiter (bird id or name)
    #eventtype
    #initialdistancemts
    #finaldistancemts
    #initialptime
    #finalptime
    #initialpointid
    #finalpointid    
    val = []
    for each in min_max_ids1:
        myRow = (each, "LINE", min_max_distance1[each][0], min_max_distance1[each][1], \
                 min_and_max_timestamp1[each][0], min_and_max_timestamp1[each][1], \
                 min_max_ids1[each][0], min_max_ids1[each][1])
        val.append(myRow)
        #print (myRow)
    #print (val)

    with arcpy.da.SearchCursor(inFc, inFields, whereClause) as cursor:
        for row in cursor:
            rowIdentifier = row[3]
            listOfIds.append(rowIdentifier)
            
    myType = np.dtype([(fieldDelimiter,'U10'),('eventtype','U10'),('initialdistancemts','d'), ('finaldistancemts','d'), \
                           ('initialptime','U30'), ('finalptime','U30'), ('initialpointid','i'), ('finalpointid','i')])
    #myType = np.dtype([('tag_ident','U10'),('DistanceMts','d')])
    myArr2 = np.rec.fromrecords(val, dtype=myType)
    #return myArr, myArr2
    return myArr2, inFields[3], listOfIds
#### Unique values in 'tag_ident'
####Points FC
##inFcPoints = os.path.join(arcpy.env.workspace, "points_3857")
####Fields to query in points FC
####inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']
####theStringUserTime = '2007-01-31 19:30:00'
####theStringUserTime = '2007-01-31 16:00:00'
###User given string list
####Both strings need to be BOTH inside range of MIN and MAX time in TAG_IDENT (each bird)
###theUserDistanceList = [0, 20000]
###theUserDistanceList = [195236.87548523, 781188.70459307]
###print(theStringUserTimeList)
####Field to construct WhereClause using FIELD IN (list)
###fieldDelimiter = 'tag_ident'
##fieldDelimiter = 'bird_name'
####List of Birds Identifier. Used to Filter the Dataset
###fieldDelimiterList = ['72364', '72413','72417','73053','73054','79694','79698']
##fieldDelimiterList = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']
##inFields = [fieldDelimiter, 'timestamp', 'DistanceMts', 'OBJECTID']
##
#### Unique values in fieldDelimiter
###myFieldDelimiterCompleteList = unique_values(inFc , fieldDelimiter)
###fields = [fieldDelimiter, 'distancemts']
#### Max and min times in POINTS by TAG_IDENT. Every BIRD min and max times inside POINTS
###min_and_max_distance = min_max_distance(inFc, fields, myFieldDelimiterCompleteList)
###print(min_and_max_distance)
####print(min_and_max_timestamp)
##
####Change string time to datetime
####theUserTime = datetime.strptime(theStringUserTime, '%Y-%m-%d %H:%M:%S')
####dates_list = [dt.datetime.strptime(date, '"%Y-%m-%d"').date() for date in dates]
####theUserTimeList = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in theStringUserTimeList]
###print (theUserTimeList)
####CheckOut tag_idents  with the theUserTimeList outside its time range (min - max)
####Both dates given by the user, need to be inside range (min - max)
####With this code we will create a new list with only
####     the TAG_IDENTS whose time values have inside theUserTime
####
###myNewFieldDelimiterList = []
###for eachValue in fieldDelimiterList:
###    min_max = min_and_max_distance[eachValue]
###    min_distance = min_max[0]
###    max_distance = min_max[1]
###    if ((theUserDistanceList[0] >= min_distance and theUserDistanceList[0] <= max_distance) \
###        and (theUserDistanceList[1] >= min_distance and theUserDistanceList[1] <= max_distance)):
###        myNewFieldDelimiterList.append(eachValue)
##
####myResutlNumpyArray,
###myResutlNumpyArray2, fieldForNexFilter, idsForNextFilter = pass_twodistance_return_time(inFc, fieldDelimiter, inFields, theUserDistanceList, myNewFieldDelimiterList)
###pass_birdlist_return_numpyarray(inFc, fieldDelimiter, inFields, fieldDelimiterList)
##myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter = pass_birdlist_return_numpyarray(inFcPoints, fieldDelimiter, inFields, fieldDelimiterList)
####print (myResutlNumpyArray)
##print (myResutlNumpyArray2)
##print (fieldForNextFilter)
##print (idsForNextFilter)
####print (myResutlNumpyArray2[0]['tag_ident'])
####print (myResutlNumpyArray2['tag_ident'])
####print (myResutlNumpyArray2['tag_ident'][0])
####print (myResutlNumpyArray2[0]['DistanceMts'])
####print (myResutlNumpyArray2['DistanceMts'])
####print (myResutlNumpyArray2['DistanceMts'][0])
####print (myResutlNumpyArray[0]['DistanceMts'])
