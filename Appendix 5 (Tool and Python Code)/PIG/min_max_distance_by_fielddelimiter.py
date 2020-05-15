# Import system modules
import arcpy
import os
from datetime import datetime

# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
#arcpy.env.workspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "ArcGISPro", "Test.gdb")
arcpy.env.overwriteOutput = True


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


#Add field distance
#fieldName = "DistanceMts"
#fieldType = "DOUBLE"
#fieldPrecision = 12
#fieldScale = 4

#arcpy.AddField_management(inFc, fieldName, fieldType, fieldPrecision, fieldScale, field_is_nullable="NULLABLE")


#Calculate distance from 0
# to accumulate value inside each groups of point
# that belongs to speficic tag_ident
def min_max_distance (inFc, fieldDelimiter, fields, myValues):
    #tag_ident_min_max_dates = []
    result = {}
    for value in myValues:
        #whereClause = "\"tag_ident\" = '" + value + "'"
        whereClause = "\"" + fieldDelimiter + "\" = '" + value + "'"
        #print(whereClause)
        allDistances = []
        firstRecord = True
        with arcpy.da.SearchCursor(inFc, fields, whereClause) as cursor:
            for row in cursor:
                if firstRecord:
                    firstRecord = False
                    minValue = int(row[1])
                    maxValue = int(row[1])
                else:
                    minValue = min(row[1],minValue)
                    maxValue = max(row[1],maxValue)                     
                #myTimeStamp = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                #allTimeStamps.append(myTimeStamp)
            #minDate = min(allTimeStamps).strftime("%Y-%m-%d %H:%M:%S")
            #maxDate = max(allTimeStamps).strftime("%Y-%m-%d %H:%M:%S")
            #partialResult = [value, minDate, maxDate]
            result[value] = [minValue, maxValue]
            #tag_ident_min_max_dates.append(partialResult)
    return result

# Unique values in 'tag_ident'
#fieldDelimiter = 'tag_ident'
#inFc = os.path.join(arcpy.env.workspace, "points")
#myValues = unique_values(inFc , fieldDelimiter)
#print (myValues)
#fields = [fieldDelimiter, 'distancemts']
#min_max_distance = min_max_distance(inFc, fieldDelimiter, fields, myValues)
#print(min_max_distance)
