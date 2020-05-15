# Name: Project_Example2.py

# Description: Project all feature classes in a geodatabase
# Requirements: os module

# Import system modules
import arcpy
import os

# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/movebank/goose/"
#arcpy.env.workspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "movebank", "goose")
arcpy.env.overwriteOutput = True

# Set local variables
outWorkspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
#outWorkspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "ArcGISPro", "Test.gdb")

try:
    # Use ListFeatureClasses to generate a list of inputs 
    for infc in arcpy.ListFeatureClasses():
        print (os.path.splitext(infc)[0])
        # Determine if the input has a defined coordinate system, can't project it if it does not
        dsc = arcpy.Describe(infc)
        print (dsc.spatialReference.Name)
        if dsc.spatialReference.Name == "Unknown":
            print('skipped this fc due to undefined coordinate system: ' + infc)
        else:
            # Determine the new output feature class path and name
            infc1 = os.path.join(arcpy.env.workspace, infc)
            print ("infc1:", infc1)
            outfc = os.path.join(outWorkspace, os.path.splitext(infc)[0])
            print ("outfc", outfc)
            # Set output coordinate system
            #outCS = arcpy.SpatialReference('WGS_1984_Web_Mercator_Auxiliary_Sphere')
            outCS = arcpy.SpatialReference(3857)
            print(outCS.name)
            # run project tool
            #arcpy.Project_management(infc1, outfc, outCS)
            print ("done")
            arcpy.Project_management(infc, outfc, outCS)
            
            # check messages
            print(arcpy.GetMessages())
            
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    
except Exception as ex:
    print(ex.args[0])
