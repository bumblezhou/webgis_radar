import os
os.environ["USE_PATH_FOR_GDAL_PYTHON"]="YES" # https://www.e-education.psu.edu/geog489/print/root1405.html --> Potential issues
from osgeo import gdal, osr
gdal.UseExceptions()

from pycwr.io import read_auto
import numpy as np

def convert_to_cog(input_file, output_file):
    # Open the source GeoTIFF file
    src_ds = gdal.Open(input_file, gdal.GA_ReadOnly)
    if src_ds is None:
        raise FileNotFoundError(f"Cannot open input file {input_file}")

    # Define the creation options for COG
    creation_options = [
        "COMPRESS=DEFLATE",     # Or use DEFLATE for compression
        "BIGTIFF=YES",          # Optional: Ensures file compatibility if it's large
        "BLOCKSIZE=1024"        # Block size for tiling
    ]

    # Convert to COG format
    gdal.Translate(
        output_file,
        src_ds,
        format="COG",
        creationOptions=creation_options
    )

    print(f"Conversion complete: {output_file}")

# Step 1: 读取雷达数据
PRD = read_auto("./temp/Z9411.20240501.145843.AR2.bz2")

# sitename = PRD.sitename
# altitude = PRD.scan_info.altitude
# end_time = PRD.scan_info.end_time
# fixed_angle = PRD.scan_info.fixed_angle
# frequency = PRD.scan_info.frequency
# latitude = PRD.scan_info.latitude
# longitude = PRD.scan_info.longitude

# fields = PRD.fields
# product = PRD.product

x1d = np.arange(-210000, 210001, 1000) ##x方向1km等间距， -210km～210km范围
y1d = np.arange(-210000, 210001, 1000) ##y方向1km等间距， -210km～210km范围
PRD.add_product_CR_xy(XRange=x1d, YRange=y1d)
cr_data = PRD.product
data_arr = cr_data.CR.data

# 3. Now, we have to define few parameters — Image geographical extent, resolution, width & height.
# width & height for any band
no_of_bands = 1
height = data_arr.shape[0]
width = data_arr.shape[1]
#sample geoextent & resolution - Update it according to your requirement
origin_x = x1d[0]    # Longitude of top-left corner
origin_y = y1d[-1]    # Latitude of top-left corner
pixel_width = (x1d.max()-x1d.min())/len(x1d)  # Approx. 1 km in degrees
pixel_height = (y1d.min()-y1d.max())/len(y1d)  # Negative to indicate top-down
print(f"no_of_bands: {no_of_bands}, origin:({origin_x}, {origin_y}), width: {width}, height: {height}, pixel_width: {pixel_width}, pixel_height: {pixel_height}")

try:
    # 4. Now that our sample data is ready, let’s start creating a tiff image. First, load the GTiff driver from gdal.
    driver = gdal.GetDriverByName('GTiff')

    output_file = './sample_02.tif'
    # 6. Update the GeoTransform of the dataset.
    out_ds = driver.Create(output_file, width, height, no_of_bands, gdal.GDT_Float32)

    transform = [origin_x, pixel_width, 0, origin_y, 0, pixel_height]
    # 5. Create the target dataset.
    out_ds.SetGeoTransform(transform)

    rotated_array = np.rot90(data_arr, k=1)  # k=-1 for clockwise, k=1 for counterclockwise
    rotated_array = np.nan_to_num(rotated_array, nan=-9999)  # Replace NaNs with 0 or any preferred value

    # 7. Write data array into dataset bands.
    band = out_ds.GetRasterBand(1)
    # color_table = gdal.ColorTable()
    # clevs = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0] #色标柱
    # cdict = ['#FFFFFF', '#01a0f6', '#00ecec', '#01ff00', '#00c800', '#019000', '#ffff00', '#e7c000', '#ff9000', '#ff0000', '#d60000', '#c00000', '#ff00f0', '#780084', '#ad90f0']
    # for (cl_index, color_level), (c_index, hex_color) in zip(enumerate(clevs), enumerate(cdict)):
    #     # rgb_color = hex_color.lstrip('#')
    #     # rgb_color = tuple(np.uint8(int(rgb_color[i:i+2], 16)) for i in (0, 2, 4))
    #     # color_table.SetColorEntry( int(color_level), rgb_color )
    #     if cl_index < len(clevs) - 1:
    #         rgb_color = hex_color.lstrip('#')
    #         start_color_level = int(color_level)
    #         start_rgb_color = tuple(np.uint8(int(rgb_color[i:i+2], 16)) for i in (0, 2, 4))

    #         raw_next_color_levle = clevs[cl_index + 1]
    #         raw_next_hex_color = cdict[cl_index + 1]
    #         raw_next_hex_color = raw_next_hex_color.lstrip('#')
    #         end_color_level = int(raw_next_color_levle)
    #         end_rgb_color = tuple(np.uint8(int(raw_next_hex_color[i:i+2], 16)) for i in (0, 2, 4))

    #         color_table.CreateColorRamp(start_color_level, start_rgb_color, end_color_level, end_rgb_color)
    #         print(f"cl_index: {cl_index}, color_level: {color_level}, c_index: {c_index}, hex_color: {hex_color}, start_color_level: {start_color_level}, start_rgb_color: {start_rgb_color}, end_color_level: {end_color_level}")
    # # # Set the color table for your band
    # # band.SetColorTable(color_table)
    # band.SetRasterColorTable(color_table)
    # band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    
    band.SetNoDataValue(-9999) #optional if no-data transparent
    band.WriteArray(rotated_array)
    band.FlushCache()
    band = None

    # 8. Update the spatial reference system of the dataset & close the dataset.
    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(4326) # WGS84 WGS（World Geodetic System）即世界大地测量系统，GPS 坐标系
    out_ds.SetProjection(out_srs.ExportToWkt())
    out_ds = None
    # remarks 坐标系:
    # 2000 坐标系（CGCS2000|EPSG：4490, 天地图坐标系
    # 百度坐标系（BD09）
    # WGS 坐标系：目前国际通用的坐标系，也是 GPS 设备获取出来的原始经纬度采用的坐标系；
    # 火星坐标系（GCJ-02|地形图非线性保密处理技术）,中国为了国家安全，在 WGS 坐标系之上进行偏移之后的坐标系，高德使用的就是这个坐标系。

    print("Rasterization complete! GeoTIFF saved at:", output_file)

    new_output_file = "./sample_cog_02.tif"
    convert_to_cog(input_file=output_file, output_file=new_output_file)
except RuntimeError as e:
    print(f"GDAL error: {e}")
