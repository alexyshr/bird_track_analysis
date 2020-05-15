# Name CreateRoutes_Example3.py
# Description: Create routes from lines. The lines are in a file geodatabase.
# The ONE_FIELD option will be used to set the measures.

# Import system modules 
import arcpy

# Set environment settings
arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
#arcpy.env.workspace = os.path.join("E:\\", "mg2", "PIG2019", "final_project", "ArcGISPro", "Test.gdb")
arcpy.env.overwriteOutput = True
    
# Set local variables
in_lines = "lines"  # base_roads exists in the roads feature dataset
routeid = "tag_ident"
out_feature_class = "lines_routes_distancemts"  # write result to the roads feature dataset
measure_source = "LENGTH"
# Execute CreateRoutes
arcpy.CreateRoutes_lr(in_lines, routeid, out_feature_class, measure_source, None, None,
                      "UPPER_LEFT", 1, 0, "IGNORE", "INDEX") 
