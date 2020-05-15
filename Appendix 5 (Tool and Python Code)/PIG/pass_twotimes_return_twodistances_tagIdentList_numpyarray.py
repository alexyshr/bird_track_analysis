# Import system modules
import arcpy
import numpy as np
import os
from datetime import datetime
from min_max_timestamp_by_fielddelimiter import min_max_timestamp
from min_max_timestamp_by_fielddelimiter import unique_values


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
def pass_twotime_return_distance(inFc, fieldDelimiter, inFields, theStringUserTimeList, fieldDelimiterList):
    delimIdFld = arcpy.AddFieldDelimiters (inFc, fieldDelimiter)
    idStr = "', '".join (fieldDelimiterList)
    whereClause = "{} IN ('{}')".format (delimIdFld, idStr) # ID IN ('1', '2', '3')
    #print(whereClause)
    #whereClause = "\"tag_ident\" = '" + theTagIdent + "'"
    #theUserTime = datetime.strptime(theStringUserTime, '%Y-%m-%d %H:%M:%S')
    theStringUserTimeInitial = theStringUserTimeList[0]
    theStringUserTimeFinal = theStringUserTimeList[1]
    theUserTimeList = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in theStringUserTimeList]
    val = []
    listOfIds = []
    #myType = np.dtype([('tag_ident','U10'),('EventType','U10'),('InitialDistanceMts','d'), ('FinalDistanceMts','d')])
    # declare empty array, zero rows but one column
    #myArr = np.empty([0,1],dtype=myType)
    #myArray = np.empty(0, dtype=myType) #, order='C')
    #contador = 0
    with arcpy.da.SearchCursor(inFc, inFields, whereClause) as cursor:
        flag1 = False
        flag2 = False
        flag3 = False
        previousTagIdent = -1
        for row in cursor:
            theRowTimeStamp = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            theRowDistance = row[2]
            tagIdent = row[0]
            rowIdentifier = row[3]

            #Chequeando el primer punto
            if theUserTimeList[0] == theRowTimeStamp:
                equivalentDistanceInitial = theRowDistance
                firstPoinIdInside = rowIdentifier
                flag1 = True
            if previousTagIdent != -1:
                if theRowDistance != previousRowDistance:
                    if previousTagIdent != tagIdent:
                        flag1 = False
                        flag2 = False
                        flag3 = False
                    if flag1 == False:
                        if theUserTimeList[0] <= theRowTimeStamp:
                            #print ("theRowTimeStamp", theRowTimeStamp)
                            #print ("previousRowTimeStamp", previousRowTimeStamp)
                            #print ("theRowDistance", theRowDistance)
                            #print ("previousRowDistance", previousRowDistance)
                            #print ("tagIdent", tagIdent)
                            #print ("previousTagIdent", previousTagIdent)
                            #print ("flag", flag)
                            timedeltaSPoint_FPoint = (theRowTimeStamp - previousRowTimeStamp).total_seconds()
                            timedeltaUserTime_FPoint = (theUserTimeList[0] - previousRowTimeStamp).total_seconds()
                            proportionFPoint_UserTime = timedeltaUserTime_FPoint / timedeltaSPoint_FPoint
                            distanceSpoint_FPoint = theRowDistance - previousRowDistance
                            equivalentDistanceInitial = previousRowDistance + (proportionFPoint_UserTime*distanceSpoint_FPoint)

                            #When passed times are both between two sequence points
                            if theUserTimeList[1] >= theRowTimeStamp:
                                firstPoinIdInside = rowIdentifier #Get ObjectID
                            else: #Points ARE between two sequence points
                                firstPoinIdInside = -1 #Nothing inside
                            
                            #val.append((tagIdent, equivalentDistance))
                            #row = np.array([(tagIdent, equivalentDistance)], dtype=myType)
                            #row = np.array([(tagIdent, equivalentDistance)], dtype=myType)
                            #myArr = np.row_stack((myArr, row))
                            #myArray[contador] = [tagIdent, equivalentDistance]
                            #myArray = numpy.row_stack((myArray, row)) 
                            #contador += 1
                            flag1 = True
                    if flag2 == False:
                        if theUserTimeList[1] <= theRowTimeStamp:
                            #print ("theRowTimeStamp", theRowTimeStamp)
                            #print ("previousRowTimeStamp", previousRowTimeStamp)
                            #print ("theRowDistance", theRowDistance)
                            #print ("previousRowDistance", previousRowDistance)
                            #print ("tagIdent", tagIdent)
                            #print ("previousTagIdent", previousTagIdent)
                            #print ("flag", flag)
                            timedeltaSPoint_FPoint = (theRowTimeStamp - previousRowTimeStamp).total_seconds()
                            timedeltaUserTime_FPoint = (theUserTimeList[1] - previousRowTimeStamp).total_seconds()
                            proportionFPoint_UserTime = timedeltaUserTime_FPoint / timedeltaSPoint_FPoint
                            distanceSpoint_FPoint = theRowDistance - previousRowDistance
                            equivalentDistanceFinal = previousRowDistance + (proportionFPoint_UserTime*distanceSpoint_FPoint)
                            #When passed times are both between two sequence points
                            if theUserTimeList[0] <= previousRowTimeStamp:
                                if theUserTimeList[1] == theRowTimeStamp:
                                    lastPoinIdInside = rowIdentifier #Get ObjectID of current Row
                                else:
                                    lastPoinIdInside = previousrowIdentifier #Get ObjectID of Previous Row
                            else: #Points ARE between two sequence points
                                lastPoinIdInside = -1 #Nothing inside
                            #val.append((tagIdent, equivalentDistance))
                            #row = np.array([(tagIdent, equivalentDistance)], dtype=myType)
                            #row = np.array([(tagIdent, equivalentDistance)], dtype=myType)
                            #myArr = np.row_stack((myArr, row))
                            #myArray[contador] = [tagIdent, equivalentDistance]
                            #myArray = numpy.row_stack((myArray, row)) 
                            flag2 = True
                            #contador += 1
            #myType = np.dtype([('tag_ident','U10'),('EventType','U10'),('InitialDistanceMts','d'), ('FinalDistanceMts','d')])
            if flag1 == True and  flag2 == True and flag3 == False:
                val.append((tagIdent, "LINE", equivalentDistanceInitial, equivalentDistanceFinal, \
                            theStringUserTimeInitial, theStringUserTimeFinal, firstPoinIdInside, lastPoinIdInside))
                if firstPoinIdInside != -1 and lastPoinIdInside != -1:
                    if (lastPoinIdInside - firstPoinIdInside) == 0:
                        listOfIds.append(firstPoinIdInside)
                    else:
                        myList = list(range(firstPoinIdInside, lastPoinIdInside+1))
                        #[listOfIds.append[id] for id in myList]
                        #for id in myList:
                        #    listOfIds.append[id]
                        listOfIds.extend(myList)
                flag3 = True
            previousTagIdent = tagIdent
            previousRowTimeStamp = theRowTimeStamp
            previousRowDistance = theRowDistance
            previousrowIdentifier = rowIdentifier
        myType = np.dtype([(fieldDelimiter,'U10'),('eventtype','U10'),('initialdistancemts','d'), ('finaldistancemts','d'), \
                           ('initialptime','U30'), ('finalptime','U30'), ('initialpointid','i'), ('finalpointid','i')])
        #myType = np.dtype([('tag_ident','U10'),('DistanceMts','d')])
        myArr2 = np.rec.fromrecords(val, dtype=myType)
        #return myArr, myArr2
        return myArr2, inFields[3], listOfIds
## Unique values in 'tag_ident'
##Points FC
#inFc = os.path.join(arcpy.env.workspace, "points")
##Fields to query in points FC
#inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']
#User given string list
##Both strings need to be BOTH inside range of MIN and MAX time in TAG_IDENT (each bird)
##theStringUserTime = '2007-01-31 19:30:00'
##theStringUserTime = '2007-01-31 16:00:00'
#theStringUserTimeList = ['2007-02-01 11:00:00', '2007-03-01 11:00:00']
#theStringUserTimeList = ['2007-01-21 12:00:00', '2007-01-21 18:56:04']
#theStringUserTimeList = ['2008-02-19 08:00:00', '2008-02-19 08:34:21']
#theStringUserTimeList = ['2007-10-05 23:57:19', '2007-10-05 23:57:23']


#print(theStringUserTimeList)
##Field to construct WhereClause using FIELD IN (list)
#fieldDelimiter = 'tag_ident'
##List of Birds Identifier. Used to Filter the Dataset
#fieldDelimiterList = ['72364', '72413','72417','73053','73054','79694','79698']

## Unique values in fieldDelimiter
##myTagIdentCompleteList = unique_values(inFc , 'tag_ident')
#myFieldDelimiterCompleteList = unique_values(inFc , fieldDelimiter)
#fields = [fieldDelimiter, 'timestamp']
## Max and min times in POINTS by TAG_IDENT. Every BIRD min and max times inside POINTS
##min_and_max_timestamp = min_max_timestamp(inFc, fields, myTagIdentCompleteList)
#min_and_max_timestamp = min_max_timestamp(inFc, fields, myFieldDelimiterCompleteList)
##print(min_and_max_timestamp)

##Change string time to datetime
##theUserTime = datetime.strptime(theStringUserTime, '%Y-%m-%d %H:%M:%S')
##dates_list = [dt.datetime.strptime(date, '"%Y-%m-%d"').date() for date in dates]
#theUserTimeList = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in theStringUserTimeList]
#print (theUserTimeList)
##CheckOut tag_idents  with the theUserTimeList outside its time range (min - max)
##Both dates given by the user, need to be inside range (min - max)
##With this code we will create a new list with only
##     the fieldDelimiter whose time values have inside theUserTime
##
##myNewTagIdents = []
#myNewFieldDelimiterList = []
#for eachValue in fieldDelimiterList:
#    min_max = min_and_max_timestamp[eachValue]
#    min_date = datetime.strptime(min_max[0], '%Y-%m-%d %H:%M:%S')
#    max_date = datetime.strptime(min_max[1], '%Y-%m-%d %H:%M:%S')
#    if ((theUserTimeList[0] >= min_date and theUserTimeList[0] <= max_date) and \
#        (theUserTimeList[1] >= min_date and theUserTimeList[1] <= max_date)):
#        myNewFieldDelimiterList.append(eachValue)

##myResutlNumpyArray,
#myResutlNumpyArray2, fieldForNexFilter, idsForNextFilter = pass_twotime_return_distance(inFc, fieldDelimiter,inFields, theStringUserTimeList, myNewFieldDelimiterList)
#print (myResutlNumpyArray)
#print (myResutlNumpyArray2)
#print (fieldForNexFilter)
#print (idsForNextFilter)
##print (myResutlNumpyArray2[0]['tag_ident'])
##print (myResutlNumpyArray2['tag_ident'])
##print (myResutlNumpyArray2['tag_ident'][0])
##print (myResutlNumpyArray2[0]['DistanceMts'])
##print (myResutlNumpyArray2['DistanceMts'])
##print (myResutlNumpyArray2['DistanceMts'][0])
##print (myResutlNumpyArray[0]['DistanceMts'])
