# Import system modules
import arcpy
import os

# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
#arcpy.env.workspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "ArcGISPro", "Test.gdb")
arcpy.env.overwriteOutput = True


def unique_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

# Unique values in 'tag_ident'
inFc = os.path.join(arcpy.env.workspace, "points")
myValues = unique_values(inFc , 'tag_ident')
print (myValues)

#Add field distance
fieldName = "distancemts"
fieldType = "DOUBLE"
fieldPrecision = 12
fieldScale = 4

arcpy.AddField_management(inFc, fieldName, fieldType, fieldPrecision, fieldScale, field_is_nullable="NULLABLE")


#Calculate distance from 0
# to accumulate value inside each groups of point
# that belongs to speficic tag_ident
fields = ['tag_ident', 'DistanceMts', 'SHAPE@X', 'SHAPE@Y']
for value in myValues:
    whereClause = "\"tag_ident\" = '" + value + "'"
    cumulativeDistance = 0
    i = 0
    with arcpy.da.UpdateCursor(inFc, fields, whereClause) as cursor:
        for row in cursor:
            if (i != 0):
                currentX = row[2]
                currentY = row[3]
                partialDistance = math.sqrt(math.pow(currentX-previousX,2)+math.pow(currentY-previousY,2))
                cumulativeDistance +=  partialDistance
            row[1] = cumulativeDistance
            previousX = row[2]
            previousY = row[3]
            i += 1
            cursor.updateRow(row)
        
