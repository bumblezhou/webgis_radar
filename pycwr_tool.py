import os
from pycwr.io import read_auto
import numpy as np
import argparse
import pandas as pd
import json


def process_composite_reflectivity_radar_file(src_file_path, output_file_path, lon1d = np.arange(119.20, 124.20, 0.01), lat1d = np.arange(36.80, 41.80, 0.01)):
    """
    生成组合反射率要素的雷达图像
    :param src_file_path:str, 源雷达文件路径
    :param output_file_path:str, 生成雷达文件COG(*.tif)路径
    :param lon1d:np.array, 1d, units:degree, 默认为大连地区经度119.2-124.2度范围, 0.01度等间距，
    :param lat1d:np.array, 1d, units:degree, 默认为大连地区纬度 36.8- 41.8度范围, 0.01度等间距，
    :return:
    """
    if(not os.path.exists(src_file_path)):
        print(f"文件({src_file_path})不存在!")
        return
    
    # Step 1: 读取雷达数据
    PRD = read_auto(src_file_path)

    # lon1d = np.arange(119.20, 124.20, 0.01) ##lon方向0.01等间距，经度119.2-124.2范围
    # lat1d = np.arange(36.80, 41.80, 0.01) ##lat方向0.01等间距， 纬度36.8-41.8度范围
    PRD.add_product_CR_lonlat(XLon=lon1d, YLat=lat1d)
    cr_data = PRD.product
    # lons = cr_data.lon_cr.data #经度
    # lats = cr_data.lat_cr.data #纬度

    data_arr = cr_data.CR_geo.data
    height = data_arr.shape[0]
    width = data_arr.shape[1]
    #sample geoextent & resolution - Update it according to your requirement
    origin_x = lon1d[0]    # Longitude of top-left corner
    origin_y = lat1d[-1]    # Latitude of top-left corner
    pixel_width = (lon1d.max()-lon1d.min())/len(lon1d)  # Approx. 1 km in degrees
    pixel_height = (lat1d.min()-lat1d.max())/len(lat1d)  # Negative to indicate top-down
    print(f"origin:({origin_x}, {origin_y}), width: {width}, height: {height}, pixel_width: {pixel_width}, pixel_height: {pixel_height}")

    # Replace NaN values with 0.0
    # data_arr[np.isnan(data_arr)] = 0.0

    rotated_array = np.rot90(data_arr, k=1)  # k=-1 for clockwise, k=1 for counterclockwise
    rotated_array = np.nan_to_num(rotated_array, nan=-9999)  # Replace NaNs with 0 or any preferred value

    data = {
        "name": "给定经纬度范围内的雷达组合反射率数据",
        "width": width,
        "height": height,
        "origin_x": origin_x,
        "origin_y": origin_y,
        "pixel_width": pixel_width,
        "pixel_height": pixel_height,
        "lon1d": lon1d.tolist(),
        "lat1d": lat1d.tolist(),
        "data": rotated_array.tolist(),
    }

    if(os.path.exists(output_file_path)):
        os.remove(output_file_path)
    # Exporting the object to a JSON file
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="A tool that analyse and generate all kinds of radar images.")
    
    # Adding arguments
    parser.add_argument("type", type=int, help="雷达文件类型: 1: 组合反射率(*.AR2.bz2), 2: FY4可见光,  3: FY4中层水汽,  4: FY4红外")
    parser.add_argument("radar_file_path", type=str, help="雷达AR2.bz2文件路径")
    parser.add_argument("output_json_path", type=str, help="输出JSON文件路径")
    parser.add_argument("--width", type=str, default="500", help="Width of the target image(*.tif)")
    parser.add_argument("--height", type=str, default="500", help="Height of the target image(*.tif)")
    
    # Parsing arguments
    args = parser.parse_args()

    if(args.type == 1):
        process_composite_reflectivity_radar_file(args.radar_file_path, args.output_json_path)
    

if __name__ == "__main__":
    main()