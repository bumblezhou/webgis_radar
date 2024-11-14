# 引用库

## gma
https://pypi.org/project/gma/
https://gma.luosgeo.com/Introduce.html

## 查看geotiff文件信息:
gdalinfo -mdd COG C:/Users/hp/Desktop/雷达解析/sample_cog_01.tif
gdalinfo -mdd COG C:/Users/hp/Desktop/雷达解析/sample_cog_02.tif

## 使用COG格式封装tif文件
gdalwarp C:\Users\hp\Desktop\雷达解析\sample_cog_01.tif C:\Users\hp\Desktop\雷达解析\sample_cog_wrapped_01.tif -of COG

## 安装pyinstaller
```bash
pip install pyinstaller
```

## 生成pycwr_tool可执行文件
pyinstaller --onefile pycwr_tool.py --console --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/data/;pycwr/data" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/configure/;pycwr/configure" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/draw/;pycwr/draw"

pyinstaller --onefile pycwr_tool.py --console --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/data/;pycwr/data" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/configure/;pycwr/configure" --add-data "C:/Users/hp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/pycwr/draw/;pycwr/draw" --debug=all

## 如何在windows上安装GDAL
    1. 安装和设置vcpkg和gdal C++库.
        git clone https://github.com/microsoft/vcpkg.git
        cd vcpkg; .\bootstrap-vcpkg.bat
        vcpkg install gdal
    2. 安装./tools/VC_redist.x64.exe.
        https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-140
        https://aka.ms/vs/17/release/vc_redist.x64.exe
    3. 安装./tools/vs_BuildTools.exe.
        WorkLoad -> Desktop development with C++
    4. 安装gdal python库。
        pip install gdal=3.9.1

## 安装其他python依赖库
```bash
pip install -r requirements.txt
```

## 下载并配置编译好的gdal C++库
    1. 下载地址
        https://www.gisinternals.com/release.php
    2. 解压release-1928-x64-gdal-3-9-1-mapserver-8-2-0.zip到任意目录，比如d:/
    3. 设置环境变量 GDAL_DATA 为 d:/release-1928-x64-gdal-3-9-1-mapserver-8-2-0/bin/gdal-data。
        这样在gdal进行计算时，就可以找到它所需要的数据文件。
    4. 设置环境变量 PROJ_LIB 为 d:/release-1928-x64-gdal-3-9-1-mapserver-8-2-0/bin/proj9/share.
        这样在gdal进行计算时，就可以找到它所需要的数据文件。
    5. 把 d:/release-1928-x64-gdal-3-9-1-mapserver-8-2-0/bin/ 添加到环境变量 PATH 中去。
        这样java代码在调用gdal功能时，就可以找到它所需要的dll文件。
    6. 把 d:/release-1928-x64-gdal-3-9-1-mapserver-8-2-0/bin/gdal/apps/ 添加到环境变量 PATH 中去。
        这样java代码在调用gdal功能时，就可以找到java代码所需要执行的.exe文件。