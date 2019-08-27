# Import system modules
import arcpy
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
from min_max_distance_by_fielddelimiter import min_max_distance
from min_max_distance_by_fielddelimiter import unique_values


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
def pass_twodistance_return_time(inFc, fieldDelimiter, inFields, theUserDistanceList, fieldDelimiterList):
    delimIdFld = arcpy.AddFieldDelimiters (inFc, fieldDelimiter)
    idStr = "', '".join (fieldDelimiterList)
    whereClause = "{} IN ('{}')".format (delimIdFld, idStr) # ID IN ('1', '2', '3')
    #print(whereClause)
    #whereClause = "\"tag_ident\" = '" + theTagIdent + "'"
    #theUserTime = datetime.strptime(theStringUserTime, '%Y-%m-%d %H:%M:%S')
    theUserDistanceInitial = theUserDistanceList[0]
    theUserDistanceFinal = theUserDistanceList[1]
    #theUserTimeList = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in theStringUserTimeList]
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
        previousTagIdent = -1  #First Row
        for row in cursor:
            theRowTimeStamp = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            theRowDistance = row[2]
            tagIdent = row[0]
            rowIdentifier = row[3]

            #Chequeando el primer punto
            if theUserDistanceList[0] == theRowDistance:
                equivalentTimeInitialString = theRowTimeStamp
                firstPoinIdInside = rowIdentifier
                flag1 = True
            if previousTagIdent != -1:
                if theRowDistance != previousRowDistance:
                    if previousTagIdent != tagIdent:
                        flag1 = False
                        flag2 = False
                        flag3 = False
                    if flag1 == False:
                        if theUserDistanceList[0] <= theRowDistance:
                            #print ("theRowTimeStamp", theRowTimeStamp)
                            #print ("previousRowTimeStamp", previousRowTimeStamp)
                            #print ("theRowDistance", theRowDistance)
                            #print ("previousRowDistance", previousRowDistance)
                            #print ("tagIdent", tagIdent)
                            #print ("previousTagIdent", previousTagIdent)
                            #print ("flag", flag)
                            timedeltaCurrPoint_PreviousPoint = (theRowTimeStamp - previousRowTimeStamp).total_seconds()
                            distanceCurrPoint_PreviousPoint = theRowDistance - previousRowDistance
                            deltaUserDistance_PreviousPoint = theUserDistanceList[0] - previousRowDistance
                            #proportionFPoint_UserTime = timedeltaUserTime_FPoint / timedeltaSPoint_FPoint
                            proportionUserDistance_PreviousPoint = deltaUserDistance_PreviousPoint / distanceCurrPoint_PreviousPoint
                            #distanceTpoint_FPoint = theRowDistance - previousRowDistance
                            #equivalentDistanceInitial = previousRowDistance + (proportionFPoint_UserTime*distanceSpoint_FPoint)
                            proportionDelta_UserDistance_PreviosPoint = timedelta(seconds=proportionUserDistance_PreviousPoint*timedeltaCurrPoint_PreviousPoint)
                            equivalentTimeInitial = previousRowTimeStamp + proportionDelta_UserDistance_PreviosPoint
                            equivalentTimeInitialString = equivalentTimeInitial.strftime('%Y-%m-%d %H:%M:%S')

                            #When passed times are both between two sequence points
                            if theUserDistanceList[1] >= theRowDistance:
                                firstPoinIdInside = rowIdentifier #Get ObjectID
                            else: #Points ARE between two sequence points
                                firstPoinIdInside = -1 #Nothing inside
                                
                            #val.append((tagIdent, equivalentDistance))
                            #row = np.array([(tagIdent, equivalentDistance)], dtype=myType)
                            #row = np.array([(tagIdent, equivalentDistance)], dtype=myType)
                            #myArr = np.row_stack((myArr, row))
                            #myArray[contador] = [tagIdent, equivalentDistance]
                            #myArray = numpy.row_stack((myArray, row)) 
                            flag1 = True
                            #contador += 1
                    if flag2 == False:
                        if theUserDistanceList[1] <= theRowDistance:
                            #print ("theRowTimeStamp", theRowTimeStamp)
                            #print ("previousRowTimeStamp", previousRowTimeStamp)
                            #print ("theRowDistance", theRowDistance)
                            #print ("previousRowDistance", previousRowDistance)
                            #print ("tagIdent", tagIdent)
                            #print ("previousTagIdent", previousTagIdent)
                            #print ("flag", flag)
                            #timedeltaSPoint_FPoint = (theRowTimeStamp - previousRowTimeStamp).total_seconds()
                            timedeltaCurrPoint_PreviousPoint = (theRowTimeStamp - previousRowTimeStamp).total_seconds()
                            distanceCurrPoint_PreviousPoint = theRowDistance - previousRowDistance
                            #timedeltaUserTime_FPoint = (theUserTimeList[1] - previousRowTimeStamp).total_seconds()
                            deltaUserDistance_PreviousPoint = theUserDistanceList[1] - previousRowDistance
                            #proportionFPoint_UserTime = timedeltaUserTime_FPoint / timedeltaSPoint_FPoint
                            proportionUserDistance_PreviousPoint = deltaUserDistance_PreviousPoint / distanceCurrPoint_PreviousPoint
                            #distanceSpoint_FPoint = theRowDistance - previousRowDistance
                            #equivalentDistanceFinal = previousRowDistance + (proportionFPoint_UserTime*distanceSpoint_FPoint)
                            proportionDelta_UserDistance_PreviosPoint = timedelta(seconds=proportionUserDistance_PreviousPoint*timedeltaCurrPoint_PreviousPoint)
                            equivalentTimeFinal = previousRowTimeStamp + proportionDelta_UserDistance_PreviosPoint
                            equivalentTimeFinalString = equivalentTimeFinal.strftime('%Y-%m-%d %H:%M:%S')

                            #When passed times are both between two sequence points
                            if theUserDistanceList[0] <= previousRowDistance:
                                if theUserDistanceList[1] == theRowDistance:
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
                val.append((tagIdent, "LINE", theUserDistanceList[0], theUserDistanceList[1], \
                            equivalentTimeInitialString, equivalentTimeFinalString, firstPoinIdInside, lastPoinIdInside))
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
##theStringUserTime = '2007-01-31 19:30:00'
##theStringUserTime = '2007-01-31 16:00:00'
#User given string list
##Both strings need to be BOTH inside range of MIN and MAX time in TAG_IDENT (each bird)
#theUserDistanceList = [0, 20000]
#theUserDistanceList = [195236.87548523, 781188.70459307]
#print(theStringUserTimeList)
##Field to construct WhereClause using FIELD IN (list)
#fieldDelimiter = 'tag_ident'
##List of Birds Identifier. Used to Filter the Dataset
#fieldDelimiterList = ['72364', '72413','72417','73053','73054','79694','79698']

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
##print (myResutlNumpyArray)
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
