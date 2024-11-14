# PPI（Plan Position Indicator）用于展示雷达在水平扫描平面上探测到的回波强度分布。
# PPI绘图不叠加地图：
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import Graph
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# fig, ax = plt.subplots()
# graph = Graph(PRD)
# graph.plot_ppi(ax, 0, "dBZ", cmap="CN_ref") ## 0代表第一层, dBZ代表反射率产品
# graph.add_rings(ax, [0, 50, 100, 150, 200, 250, 300])
# ax.set_title("PPI Plot", fontsize=16)
# ax.set_xlabel("Distance From Radar In East (km)", fontsize=14)
# ax.set_ylabel("Distance From Radar In North (km)", fontsize=14)
# plt.show()

# PPI绘图叠加地图：
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import GraphMap
# import cartopy.crs as ccrs
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# ax = plt.axes(projection=ccrs.PlateCarree())
# graph = GraphMap(PRD, ccrs.PlateCarree())
# graph.plot_ppi_map(ax, 0, "dBZ", cmap="CN_ref") ## 0代表第一层, dBZ代表反射率产品，cmap
# ax.set_title("PPI Plot with Map", fontsize=16)
# plt.tight_layout()
# plt.show()

# RHI图是垂直平面的扫描结果，通常用于研究风暴的垂直结构。
# 雷达RHI绘图:
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import Graph
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# fig, ax = plt.subplots()
# graph = Graph(PRD)
# graph.plot_rhi(ax, 0, field_name="dBZ", cmap="CN_ref", clabel="Radar Reflectivity")
# ax.set_ylim([0, 10]) #设置rhi的高度范围 （units：km）
# ax.set_xlabel("distance from radar (km)", fontsize=14)
# ax.set_ylabel("Height (km)", fontsize=14)
# plt.tight_layout()
# plt.show()

# 天气雷达剖面图：
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import Graph
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# fig, ax = plt.subplots()
# graph = Graph(PRD)
# graph.plot_vcs(ax, (0,0), (150, 0), "dBZ", cmap="copy_pyart_NWSRef") #起点，终点 （units: km）
# ax.set_ylim([0, 15])
# ax.set_xlim([0, 80])
# ax.set_ylabel("Height (km)", fontsize=14)
# ax.set_xlabel("Distance From Section Start (Uints:km)", fontsize=14)
# ax.set_title("VCS Plot", fontsize=16)
# plt.tight_layout()
# plt.show()

# 水凝物分类
# # -*- coding: utf-8 -*-
# from pycwr.io import read_auto
# from pycwr.retrieve.HID import fhc_HCL
# import matplotlib.pyplot as plt
# import numpy as np
# from pycwr.draw.RadarPlot import plot_xy, add_rings
# import pandas as pd
# file = r"./data/NUIST.20150627.002438.AR2.bz2"
# file_t = r"./data/20150627.csv"
# temp = pd.read_csv(file_t, index_col=0, header=None, names=['temp'])
# NRadar = read_auto(file)
# num = 3
# dBZ = np.where(NRadar.fields[num].CC>0.9, NRadar.fields[num].dBZ, np.nan)
# KDP = np.where(NRadar.fields[num].CC>0.9, NRadar.fields[num].KDP, np.nan)
# ZDR = np.where(NRadar.fields[num].CC>0.9, NRadar.fields[num].ZDR, np.nan)
# CC = np.where(NRadar.fields[num].CC>0.9, NRadar.fields[num].CC, np.nan)
# temp_2d = np.interp(NRadar.fields[num].z.values/1000., temp.index, temp['temp'])
# dBZ[:,0] = np.nan
# ticks = np.arange(1, 11, 1)
# ticklabels = ['Drizzle', 'Rain', 'Ice Crystals', 'Aggregates', 'Wet Snow', 'Vertical Ice', 'LD Graupel', 'HD Graupel', 'Hail', 'Big Drops']
# hcl = fhc_HCL(dBZ=dBZ, KDP=KDP, ZDR=ZDR, CC = CC, T=temp_2d)
# fig, ax = plt.subplots()
# plot_xy(ax, NRadar.fields[num].x, NRadar.fields[num].y, hcl,
#         cmap="CN_hcl", bounds=np.arange(0.5,10.6,1),
#         cbar_ticks=ticks, cbar_ticklabels=ticklabels)
# add_rings(ax=ax, rings=[0, 50, 100, 150])
# ax.set_xlim([-150, 150])
# ax.set_ylim([-150, 150])
# ax.set_xlabel("Distance From Radar In East (km)", fontsize=12)
# ax.set_ylabel("Distance From Radar In North (km)", fontsize=12)
# ax.set_title("Hydrometeor classification, El : 3.4", fontsize=14)
# # plt.savefig(r"./201506270024_HC.png", dpi=600)
# plt.show()

# 以雷达为中心，生成笛卡尔坐标的组合反射率网格产品
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import plot_xy
# import numpy as np
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# x1d = np.arange(-210000, 210001, 1000) ##x方向1km等间距， -210km～210km范围
# y1d = np.arange(-210000, 210001, 1000) ##y方向1km等间距， -210km～210km范围
# PRD.add_product_CR_xy(XRange=x1d, YRange=y1d)
# print(PRD.product)
# grid_x, grid_y = np.meshgrid(x1d, y1d, indexing="ij")
# fig, ax = plt.subplots()
# plot_xy(ax, grid_x, grid_y, PRD.product.CR) ##画图显示
# ax.set_xlabel("Distance From Radar In East (km)", fontsize=14)
# ax.set_ylabel("Distance From Radar In North (km)", fontsize=14)
# plt.tight_layout()
# plt.show()

# # 利用经纬度坐标信息生成组合反射率网格产品(辽宁地区，使用在线地图)
from pycwr.io import read_auto
import matplotlib.pyplot as plt
from pycwr.draw.RadarPlot import plot_lonlat_map
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import numpy as np
filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
PRD = read_auto(filename)
lon1d = np.arange(119.2, 124.2, 0.01) ##lon方向0.01等间距，117-120范围
lat1d = np.arange(36.8, 41.8, 0.01) ##lat方向0.01等间距， 31-34度范围
PRD.add_product_CR_lonlat(XLon=lon1d, YLat=lat1d)
grid_lon, grid_lat = np.meshgrid(lon1d, lat1d, indexing="ij")
ax = plt.axes(projection=ccrs.PlateCarree())
plot_lonlat_map(ax, grid_lon, grid_lat, PRD.product.CR_geo, transform=ccrs.PlateCarree())
ax.set_extent([119.2, 124.2, 36.8, 41.8], crs = ccrs.PlateCarree()) #设置显示范围
plt.tight_layout()
plt.show()

# CAPPI（Constant Altitude Plan Position Indicator）图展示的是某一固定高度上的回波分布。
# 以雷达为中心，生成笛卡尔坐标的CAPPI网格产品
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import plot_xy
# import numpy as np
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# x1d = np.arange(-210000, 210000, 1000) ##x方向1km等间距， -210km～210km范围
# y1d = np.arange(-210000, 210000, 1000) ##y方向1km等间距， -210km～210km范围
# PRD.add_product_CAPPI_xy(XRange=x1d, YRange=y1d, level_height=3000) ##level height units:meters
# print(PRD.product)
# grid_x, grid_y = np.meshgrid(x1d, y1d, indexing="ij")
# fig, ax = plt.subplots()
# plot_xy(ax, grid_x, grid_y, PRD.product.CAPPI_3000) ##画图显示
# ax.set_xlabel("Distance From Radar In East (km)", fontsize=14)
# ax.set_ylabel("Distance From Radar In North (km)", fontsize=14)
# plt.tight_layout()
# plt.show()

# 利用经纬度坐标信息生成CAPPI网格产品
# from pycwr.io import read_auto
# import matplotlib.pyplot as plt
# from pycwr.draw.RadarPlot import plot_lonlat_map
# import cartopy.crs as ccrs
# import numpy as np
# filename = r"./temp/Z9411.20240501.145843.AR2.bz2"
# PRD = read_auto(filename)
# lon1d = np.arange(119.2, 124.2, 0.01) ##lon方向0.01等间距，117-120范围
# lat1d = np.arange(37.2, 42.2, 0.01) ##lat方向0.01等间距， 31-34度范围
# PRD.add_product_CAPPI_lonlat(XLon=lon1d, YLat=lat1d, level_height=3000) ##插值1500m高度的
# # XLon:np.ndarray, 1d, units:degrees
# # YLat:np.ndarray, 1d, units:degrees
# # level_height:常量，要计算的高度 units:meters
# grid_lon, grid_lat = np.meshgrid(lon1d, lat1d, indexing="ij")
# ax = plt.axes(projection=ccrs.PlateCarree())
# plot_lonlat_map(ax, grid_lon, grid_lat, PRD.product.CAPPI_geo_3000, transform=ccrs.PlateCarree())
# ax.set_extent([119.2, 124.2, 37.2, 42.2], crs = ccrs.PlateCarree()) #设置范围
# plt.tight_layout()
# plt.show()

# import warnings
# warnings.filterwarnings('ignore')
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from pycwr.GraphicalInterface.RadarInterface import MainWindow
# from PyQt5 import QtWidgets
# app = QtWidgets.QApplication(sys.argv)
# ui = MainWindow()
# ui.show()
# sys.exit(app.exec_())