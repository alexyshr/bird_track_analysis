# Import system modules
import arcpy
import os
import numpy as np
from datetime import datetime

def filter_by_fields_where(inFc, fieldDelimiter, inFields, fieldDelimiter2 = "", fieldDelimiterList2 = [], field1="", condition1="", field2="", condition2=""):
    #delimIdFld = arcpy.AddFieldDelimiters (inFc, fieldDelimiter) #Note that fieldDelimiter2 need to be STRING
    #idStr = "', '".join (fieldDelimiterList)
    #whereClause = "{} IN ('{}')".format (fieldDelimiter, idStr) # ID IN ('1', '2', '3')
    if fieldDelimiter2 != "": #and not fieldDelimiterList2: #Note that fieldDelimiter2 need to be INTEGER (not STRING)
        #delimIdFld2 = arcpy.AddFieldDelimiters (inFc, fieldDelimiter2) 
        idStr2 = ", ".join (map(str,fieldDelimiterList2))
        whereClause = "{} IN ({})".format (fieldDelimiter2, idStr2) # ID IN (1, 2, 3)
        #whereClause = whereClause + " And " + whereClause2

    if field1 != "" and condition1 != "":
        whereClause = whereClause + " And " + field1 + " " + condition1
        inFields.append(field1)
    if field2 != "" and condition2 != "":
        whereClause = whereClause + " And " + field2 + " " + condition2
        inFields.append(field2)

    result = []
    listOfIds = []
    valDistances = [] #To store inicial and final distances (some cases, when is POINT
                      #inicial distances is equal to final distance in this array)
    valDates = []   #To srore inicial and final dates (some cases, when is POINT
                      #inicial date is equal to final date in this array)
    valPointsIDs = []   #To srore inicial and final points ids (some cases, when is POINT
                      #inicial point id is equal to final point id in this array)
    
    #print (whereClause)
    #print (inFields)
    arcpy.MakeTableView_management(inFc, "myTableView", where_clause = whereClause)
    totalRowCount = int(arcpy.GetCount_management("myTableView").getOutput(0))
    
    #print(totalRowCount)
    counter = 0
    with arcpy.da.SearchCursor(inFc, inFields, whereClause) as cursor:
        previousrowIdentifier = -1
        previousTagIdent = -1
        tagIdentCounter = 0
        rowIdentifierCounter = 0 
        countersOfCumulativePoints = 0 #Count the amount of cumulative points (could be for POINT of LINE)
        
        for row in cursor:
            theRowTimeStamp = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            tagIdent = row[0]
            theRowDistance = row[2]
            rowIdentifier = row[3]
            #print(rowIdentifier)
            #print("--")

            #REMEMBER THAT THE WRITE DONE IN CURRENT RECORD CORRESPOND TO CASE OF PREVIOUS RECORD
            if previousrowIdentifier != -1: #We are not in the first row. This is for SECOND and NEXT rows
                if tagIdent == previousTagIdent: #Second and next rows with the same tagIdent as previous
                    tagIdentToWrite = tagIdent
                    if (rowIdentifier - previousrowIdentifier) == 1: #IDENTIFIERS CONSECUTUVES
                                                                     #Check if IDS are cosecutives, then is the case of a
                                                                     #LINE LINE
                        #if previousrowIdentifierCounter >= 1: #if s
                        if countersOfCumulativePoints == 0: #THE FISRT POINT OF LINE
                            startPoint = previousrowIdentifier
                            startDistance = previousRowDistance
                            startDate = previousRowTimeStamp
                        countersOfCumulativePoints += 1 #ACCUMULATE THE POINT FOR THE LINE
                    elif (rowIdentifier - previousrowIdentifier) != 1:  #IDENTIFIERS NO CONSECUTUVES
                                                                        #TWO OPTIONS:
                                                                        #   ONE POINT COLLECTED IN PREVIOUS ITERATION
                                                                        #   LINE FINISHING IN PREVIOUS ITERATION
                        if countersOfCumulativePoints == 0: #   ONE POINT COLLECTED IN PREVIOUS ITERATION
                            startPoint = previousrowIdentifier
                            startDistance = previousRowDistance
                            startDate = previousRowTimeStamp
                            endPoint = previousrowIdentifier
                            endDistance = previousRowDistance
                            endDate = previousRowTimeStamp
                            eventType = "POINT"
                        elif countersOfCumulativePoints != 0: #   LINE FINISHING IN PREVIOUS ITERATION
                            #print ("entro: countersOfCumulativePoints = " + str(countersOfCumulativePoints))
                            endPoint = previousrowIdentifier
                            endDistance = previousRowDistance
                            endDate = previousRowTimeStamp
                            eventType = "LINE"  
                        countersOfCumulativePoints = 0
                        if startPoint == endPoint: #Check is it is POINT
                            listOfIds.append(startPoint)
                        else: # It is LINE
                            myList = list(range(startPoint, endPoint+1))
                            #[listOfIds.append[id] for id in myList]
                            #for id in myList:
                            #    listOfIds.append[id]
                            listOfIds.extend(myList)
                        result.append((tagIdentToWrite, eventType, startDistance, endDistance, \
                                   startDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S'), startPoint, endPoint))                        
                elif tagIdent != previousTagIdent: #CHANGE OR tagIdent
                    tagIdentToWrite = previousTagIdent
                    if countersOfCumulativePoints == 0: #only one POINT that was collected in previos iteration
                        startPoint = previousrowIdentifier
                        startDistance = previousRowDistance
                        startDate = previousRowTimeStamp
                        endPoint = previousrowIdentifier
                        endDistance = previousRowDistance
                        endDate = previousRowTimeStamp
                        eventType = "POINT"
                    elif countersOfCumulativePoints != 0: #LINE ENDS in previous ITERATION
                        endPoint = previousrowIdentifier
                        endDistance = previousRowDistance
                        endDate = previousRowTimeStamp
                        eventType = "LINE"  
                    countersOfCumulativePoints = 0
                    if startPoint == endPoint: #Check is it is POINT
                        listOfIds.append(startPoint)
                    else: # It is LINE
                        myList = list(range(startPoint, endPoint+1))
                        #[listOfIds.append[id] for id in myList]
                        #for id in myList:
                        #    listOfIds.append[id]
                        listOfIds.extend(myList)
                    result.append((tagIdentToWrite, eventType, startDistance, endDistance, \
                               startDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S'), startPoint, endPoint))                        
                    #startPoint = rowIdentifier
                    #startDistance = theRowDistance
                    #startDate = theRowTimeStamp
                    #countersOfCumulativePoints += 1             
            #previousrowIdentifierCounter = rowIdentifierCounter
            counter += 1
            if counter == totalRowCount:
                tagIdentToWrite = tagIdent
                if (rowIdentifier - previousrowIdentifier) == 1: # then is one LINE that ENDs in last record
                    endPoint = rowIdentifier
                    endDistance = theRowDistance
                    endDate = theRowTimeStamp
                    eventType = "LINE"
                elif (rowIdentifier - previousrowIdentifier) != 1: # then is one POINT that STARS and ENDS in last record
                    startPoint = rowIdentifier
                    startDistance = theRowDistance
                    startDate = theRowTimeStamp
                    endPoint = rowIdentifier
                    endDistance = theRowDistance
                    endDate = theRowTimeStamp
                    eventType = "POINT"
                countersOfCumulativePoints = 0
                if startPoint == endPoint: #Check is it is POINT
                    listOfIds.append(startPoint)
                else: # It is LINE
                    myList = list(range(startPoint, endPoint+1))
                    #[listOfIds.append[id] for id in myList]
                    #for id in myList:
                    #    listOfIds.append[id]
                    listOfIds.extend(myList)
                result.append((tagIdent, eventType, startDistance, endDistance, \
                           startDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S'), startPoint, endPoint))
            previousrowIdentifier = rowIdentifier
            previousTagIdent = tagIdent
            previousRowTimeStamp = theRowTimeStamp
            previousRowDistance = theRowDistance
    myType = np.dtype([(fieldDelimiter,'U10'),('eventtype','U10'),('initialdistancemts','d'), ('finaldistancemts','d'), \
                        ('initialptime','U30'), ('finalptime','U30'), ('initialpointid','i'), ('finalpointid','i')])
    myArr2 = np.rec.fromrecords(result, dtype=myType)         
    #return result
    return myArr2, inFields[3], listOfIds, whereClause, totalRowCount
## Set environment settings
#arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
##arcpy.env.workspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "ArcGISPro", "Test.gdb")
#arcpy.env.overwriteOutput = True

# Unique values in 'tag_ident'
#inFcPoints = os.path.join(arcpy.env.workspace, "points")
#print(inFcPoints)
##fieldDelimiter = 'tag_ident'
#fieldDelimiter = 'bird_name'

##inFields = ['tag_ident', 'timestamp', 'DistanceMts', 'OBJECTID']
##inFields = ['bird_name', 'timestamp', 'DistanceMts', 'OBJECTID']
#inFields = [fieldDelimiter, 'timestamp', 'DistanceMts', 'OBJECTID']

#fieldDelimiterList = ['72364', '72413', '79694', '79698']
#fieldDelimiterList = ['Folkert', 'Kees', 'Ale', 'Jacob', 'Niki', '79694', '79698']

#fieldDelimiter2 = 'OBJECTID'
#fieldDelimiterList2 = list(range(1, 7364))
#fieldDelimiterList2 = list(range(1023, 2474))
#fieldDelimiterList2 = list(range(1023, 2024))
#fieldDelimiter2 = ""
#fieldDelimiterList2 = []

#field1 = "ws_mtss"
#condition1 = ">= 6"
#field2 = "ws_mtss"
#condition2 = "< 6.2"


#myResutlNumpyArray2, fieldForNextFilter, idsForNextFilter = filter_by_fields_where(inFcPoints, \
#                                        fieldDelimiter, inFields, \
#                                        fieldDelimiter2, fieldDelimiterList2, \
#                                        field1, condition1, field2, condition2)
#print (myResutlNumpyArray2)
#print (fieldForNextFilter)
#print (idsForNextFilter)

