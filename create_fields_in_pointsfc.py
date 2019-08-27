# Import system modules
import arcpy
import os

#This script needs the table W1672519302687606168 inside geodatabase, with all the fields
#
# Set environment settings
#arcpy.env.workspace = "E:/mg2/PIG2019/final_project/ArcGISPro/Test.gdb/"
arcpy.env.workspace = "C:/PIG/Test.gdb"
arcpy.env.overwriteOutput = True

inFc = os.path.join(arcpy.env.workspace, "points_3857")

# Create a feature layer from the vegtype featureclass
arcpy.MakeFeatureLayer_management (inFc,  "myPointsLayer")

# Set the local parameters
join_table = os.path.join(arcpy.env.workspace, "W1672519302687606168")


# Join the feature layer to a table
arcpy.AddJoin_management ("myPointsLayer", "OBJECTID", join_table, "OBJECTID", "KEEP_ALL")


#This is to Join two FC o tables FOREVER
#arcpy.JoinField_management(inFc, "OBJECTID", join_table, "OBJECTID")
#arcpy.management.CalculateField("points", "points.timestamp_string", "!W1672519302687606168.timestamp_string!", "PYTHON3", None)

##arcpy.AddField_management(inFc, "distancemts_wm", "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.distancemts_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "distancemts_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'timestamp_string', 'TEXT', field_length=40, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.timestamp_string!"
##arcpy.CalculateField_management ("myPointsLayer", "timestamp_string", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'bird_name', 'TEXT', field_length=15, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.bird_name!"
##arcpy.CalculateField_management ("myPointsLayer", "bird_name", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'cuad_vel_wind', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.cuad_vel_wind!"
##arcpy.CalculateField_management ("myPointsLayer", "cuad_vel_wind", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'alpha_wind_e', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.alpha_wind_e!"
##arcpy.CalculateField_management ("myPointsLayer", "alpha_wind_e", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'alphavw_dir_wind_e', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.alphavw_dir_wind_e!"
##arcpy.CalculateField_management ("myPointsLayer", "alphavw_dir_wind_e", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vw_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vw_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vw_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'date', 'TEXT', field_length=15, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.date!"
##arcpy.CalculateField_management ("myPointsLayer", "date", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'time', 'TEXT', field_length=15, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.time!"
##arcpy.CalculateField_management ("myPointsLayer", "time", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'datetime', 'TEXT', field_length=30, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.datetime!"
##arcpy.CalculateField_management ("myPointsLayer", "datetime", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'deltatime_seg', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.deltatime_seg!"
##arcpy.CalculateField_management ("myPointsLayer", "deltatime_seg", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'month', 'TEXT', field_length=2, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.month!"
##arcpy.CalculateField_management ("myPointsLayer", "month", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'month_day', 'TEXT', field_length=6, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.month_day!"
##arcpy.CalculateField_management ("myPointsLayer", "month_day", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'season', 'TEXT', field_length=15, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.season!"
##arcpy.CalculateField_management ("myPointsLayer", "season", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'hour', 'TEXT', field_length=2, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.hour!"
##arcpy.CalculateField_management ("myPointsLayer", "hour", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'vel_we_bird_mtss_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_we_bird_mtss_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_we_bird_mtss_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'vel_sn_bird_mtss_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_sn_bird_mtss_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_sn_bird_mtss_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'vg_mtss_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vg_mtss_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "vg_mtss_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'vg_mtss_gcd', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vg_mtss_gcd!"
##arcpy.CalculateField_management ("myPointsLayer", "vg_mtss_gcd", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'vg_kmh_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vg_kmh_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "vg_kmh_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'vg_kmh_gcd', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vg_kmh_gcd!"
##arcpy.CalculateField_management ("myPointsLayer", "vg_kmh_gcd", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'dist_segment_bird_mts_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.dist_segment_bird_mts_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "dist_segment_bird_mts_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'dist_segment_bird_mts_gcd', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.dist_segment_bird_mts_gcd!"
##arcpy.CalculateField_management ("myPointsLayer", "dist_segment_bird_mts_gcd", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'dist_acum_bird_mts_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.dist_acum_bird_mts_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "dist_acum_bird_mts_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'dist_acum_bird_mts_gcd', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.dist_acum_bird_mts_gcd!"
##arcpy.CalculateField_management ("myPointsLayer", "dist_acum_bird_mts_gcd", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'dist_we_bird_mts_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.dist_we_bird_mts_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "dist_we_bird_mts_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'dist_sn_bird_mts_wm', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.dist_sn_bird_mts_wm!"
##arcpy.CalculateField_management ("myPointsLayer", "dist_sn_bird_mts_wm", calcExpression, "PYTHON")
##
##arcpy.AddField_management(inFc, 'cuad_dir_bird', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.cuad_dir_bird!"
##arcpy.CalculateField_management ("myPointsLayer", "cuad_dir_bird", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'alpha_dir_bird_e', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.alpha_dir_bird_e!"
##arcpy.CalculateField_management ("myPointsLayer", "alpha_dir_bird_e", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'alphavg_dir_bird_e', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.alphavg_dir_bird_e!"
##arcpy.CalculateField_management ("myPointsLayer", "alphavg_dir_bird_e", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'alpha_vg_vw', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.alpha_vg_vw!"
##arcpy.CalculateField_management ("myPointsLayer", "alpha_vg_vw", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ws_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ws_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "ws_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'wc_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.wc_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "wc_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'va_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.va_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "va_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'coordx_mts', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.coordx_mts!"
##arcpy.CalculateField_management ("myPointsLayer", "coordx_mts", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'coordy_mts', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.coordy_mts!"
##arcpy.CalculateField_management ("myPointsLayer", "coordy_mts", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ifdih_veg_cover', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ifdih_veg_cover!"
##arcpy.CalculateField_management ("myPointsLayer", "ifdih_veg_cover", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'lvytp_ntree_veg', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.lvytp_ntree_veg!"
##arcpy.CalculateField_management ("myPointsLayer", "lvytp_ntree_veg", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ifdpl_rel_hum_1000', "FLOAT", 8, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ifdpl_rel_hum_1000!"
##arcpy.CalculateField_management ("myPointsLayer", "ifdpl_rel_hum_1000", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'lvytp_tree_cover', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.lvytp_tree_cover!"
##arcpy.CalculateField_management ("myPointsLayer", "lvytp_tree_cover", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'elevation_mts', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.elevation_mts!"
##arcpy.CalculateField_management ("myPointsLayer", "elevation_mts", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ifdp_spec_hum_1000', "FLOAT", 8, 6, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ifdp_spec_hum_1000!"
##arcpy.CalculateField_management ("myPointsLayer", "ifdp_spec_hum_1000", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ifdp_temperature_1000', "FLOAT", 8, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ifdp_temperature_1000!"
##arcpy.CalculateField_management ("myPointsLayer", "ifdp_temperature_1000", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'lvit_ndvi', "FLOAT", 8, 6, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.lvit_ndvi!"
##arcpy.CalculateField_management ("myPointsLayer", "lvit_ndvi", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'lvytp_unvegetaded', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.lvytp_unvegetaded!"
##arcpy.CalculateField_management ("myPointsLayer", "lvytp_unvegetaded", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ifdi_low_veg_cover', "FLOAT", 8, 6, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ifdi_low_veg_cover!"
##arcpy.CalculateField_management ("myPointsLayer", "ifdi_low_veg_cover", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'ifd_soil_water_content', "FLOAT", 8, 6, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.ifd_soil_water_content!"
##arcpy.CalculateField_management ("myPointsLayer", "ifd_soil_water_content", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_1000_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_1000_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_1000_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_1000_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_1000_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_1000_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_850_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_850_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_850_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_850_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_850_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_850_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_600_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_600_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_600_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_600_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_600_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_600_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_500_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_500_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_500_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_500_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_500_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_500_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_400_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_400_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_400_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_400_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_400_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_400_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_200_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_200_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_200_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_200_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_200_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_200_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_sn_v_125_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_sn_v_125_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_sn_v_125_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'vel_wind_we_u_125_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.vel_wind_we_u_125_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "vel_wind_we_u_125_mtss", calcExpression, "PYTHON")
##arcpy.AddField_management(inFc, 'FID', "SHORT", field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.OBJECTID!"
##arcpy.CalculateField_management ("myPointsLayer", "FID", calcExpression, "PYTHON")

##arcpy.AddField_management(inFc, 'wswc_mtss', "DOUBLE", 12, 4, field_is_nullable="NULLABLE")
##calcExpression = "!W1672519302687606168.wswc_mtss!"
##arcpy.CalculateField_management ("myPointsLayer", "wswc_mtss", calcExpression, "PYTHON")


#this is useful to remove joins made with AddJoin_management
arcpy.RemoveJoin_management ("myPointsLayer", "W1672519302687606168")


