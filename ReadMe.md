# 引用库

## gma
https://pypi.org/project/gma/
https://gma.luosgeo.com/Introduce.html

## 查看geotiff文件信息:
gdalinfo -mdd COG C:/Users/hp/Desktop/雷达解析/sample_cog_01.tif
gdalinfo -mdd COG C:/Users/hp/Desktop/雷达解析/sample_cog_02.tif

## 使用COG格式封装tif文件
gdalwarp C:\Users\hp\Desktop\雷达解析\sample_cog_01.tif C:\Users\hp\Desktop\雷达解析\sample_cog_wrapped_01.tif -of COG

## 生成pycwr_tool可执行文件
pyinstaller --onefile pycwr_tool.py --console --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/data/;pycwr/data" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/configure/;pycwr/configure" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/draw/;pycwr/draw"

pyinstaller --onefile pycwr_tool.py --console --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/data/;pycwr/data" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/configure/;pycwr/configure" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/draw/;pycwr/draw" --debug=all
