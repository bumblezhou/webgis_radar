import cinrad
# import salem
import geopandas as geo
from cinrad.io import CinradReader, StandardData
# import PIL
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import numpy as np
from matplotlib import font_manager
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import maskout
import matplotlib.pyplot as plt
matplotlib.rc("font", family='SimHei')
# import copy
# import shapefile
import pandas as pd
from ftplib import FTP
import datetime
import os
from pycwr.io import read_auto
from pycwr.draw.RadarPlot import plot_lonlat_map
from matplotlib.colors import Normalize,BoundaryNorm,ListedColormap
from matplotlib.cm import ScalarMappable
from pathlib import Path

def ftp_connect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def download_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    #fp.close()

def getLastRadarFile():
    #1.获取最新雷达基数据 172.19.38.5 radar/Radar*%8263#
    ftp = ftp_connect("172.19.38.5", "radar", "Radar*%8263#")
    ftp.cwd('/zls_archive')
    filenamelist = ftp.nlst()
    nowtime = datetime.datetime.now() + datetime.timedelta(hours=-8)
    nowtime_shijie_1 = datetime.datetime.now() + datetime.timedelta(hours=-8)
    nowtime_shijie_2 = datetime.datetime.now() + datetime.timedelta(hours=-9)
    nowtime_str = nowtime.strftime("%Y%m%d")
    partfilename = "Z9411."+nowtime_str+"."
    radarlist = []
    for x in filenamelist:
        if(x.startswith(partfilename) and x.endswith('.bz2')):
            radarlist.append(x)
        if(x.startswith(nowtime_str)):
            ftp.cwd("/zls_archive"+"/"+x)
            filelist = ftp.nlst()
            for radarname in filelist:
                partfilename_2 = "Z9411."+nowtime_shijie_1.strftime("%Y%m%d")+"."+nowtime_shijie_1.strftime("%H")
                partfilename_3 = "Z9411."+nowtime_shijie_2.strftime("%Y%m%d")+"."+nowtime_shijie_2.strftime("%H")
                if((radarname.startswith(partfilename_2) or radarname.startswith(partfilename_3)) and radarname.endswith('.bz2')):
                    radarlist.append("/zls_archive"+"/"+x+"/"+radarname)
    for name in radarlist:
        ftp = ftp_connect("172.19.38.5", "radar", "Radar*%8263#")
        if(name.startswith("Z9411")):
            ftp.cwd('/zls_archive')
            download_file(ftp,name,"temp"+"/"+name)
        if(name.startswith("/")):
            basename = os.path.basename(name)
            download_file(ftp,name,"temp"+"/"+basename)
    return None

def drawRadar(filename):
    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['axes.unicode_minus']=False   #解决负号“-”显示为方块的问题
    f = StandardData('./temp'+"/"+filename)
    rl = list(f.iter_tilt(230, 'REF'))
    #计算组合反射率
    cr = cinrad.calc.quick_cr(rl)
    arr = cr.CR.data

    lon1d = np.arange(121, 127, 0.01) ##lon方向0.01等间距，117-120范围
    lat1d = np.arange(38, 44, 0.01) ##lat方向0.01等间距， 31-34度范围
    PRD = read_auto('./temp'+"/"+filename)
    PRD.add_product_CR_lonlat(XLon=lon1d, YLat=lat1d)

    scantime_str = cr.attrs["scan_time"]
    scantime = datetime.datetime.strptime(scantime_str,"%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
    scantime_str = scantime.strftime("%Y-%m-%d %H:%M:00")
    titletime_str = scantime.strftime("%Y%m%d%H%M")
    dict_info = {
        # "大连全区":["DL_COU_CUSTOM.shp","sq.csv",[120, 123, 38.8, 40.2],[121.30, 39.11],[280, 690]],
        "大连市区":["ZCQ_TOW.shp","sq.csv",[121.15, 121.85, 38.75, 39.15],[121.60, 39.8],[300, 690],"dlsq"],
        "旅顺口区":["LS_TOW.shp","ls.csv",[120.95, 121.40, 38.70, 39.00],[120.93, 39.05],[350, 690],"ls"],
        "金普新区":["JP_TOW.shp","jp.csv",[121.40, 122.34, 38.90, 39.55],[121.45, 39.55],[375, 710],"jz"],
        "长兴岛经济区":["CXD_TOW.shp","cxd.csv",[121.15, 121.63, 39.32, 39.71],[121.05, 39.77],[295, 710],"cxd"],
        "普兰店区":["PLD_TOW.shp","pld.csv",[121.65, 122.75, 39.24, 40.12],[121.67, 40.15],[375, 710],"pld"],
        "瓦房店市":["WFD_TOW.shp","wfd.csv",[121.20, 122.50, 39.27, 40.15],[121.24, 40.18],[375, 710],"wfd"],
        "庄河市":["ZH_TOW.shp","zh.csv",[122.23, 123.83, 39.28, 40.33],[122.19, 40.25],[295, 710],"zh"],
        "长海县":["CH_TOW.shp","ch.csv",[121.81, 123.63, 38.68, 39.71],[121.96, 39.63],[215, 710],"ch"]
    }
    for sitename,value in dict_info.items():
        shppath = r"./DL_ALL/" + value[0]
        shp = geo.read_file(shppath)
        #1.筛选市区范围内组合反射率值
        # cr_data = cr.salem.roi(shape=shp)
        #掩膜
        #cr_data = PRD.product.salem.roi(shape=shppath)
        cr_data = PRD.product
        fig = plt.figure(figsize=(9,6),facecolor='#666666',edgecolor='Blue',frameon=False)
        ax1 = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
        clevs = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0] #色标柱
        cdict = ['#FFFFFF', '#01a0f6', '#00ecec', '#01ff00', '#00c800', '#019000', '#ffff00', '#e7c000', '#ff9000',
                  '#ff0000',
                  '#d60000', '#c00000', '#ff00f0', '#780084', '#ad90f0']#颜色对应色标值
        # lons = cr_data.longitude.data
        # lats = cr_data.latitude.data
        lons = cr_data.lon_cr.data
        lats = cr_data.lat_cr.data
        crdata = cr_data['CR_geo'].data
        
        grid_lon,grid_lat = np.meshgrid(lon1d,lat1d,indexing="ij")

        #crdata = cr_data.data
        cr_array = xr.DataArray(crdata,coords=[lats,lons],dims=['latitude', 'longitude'])
        my_cmap = colors.ListedColormap(cdict)  # 自定义颜色映射 color-map
        norm = mpl.colors.BoundaryNorm(clevs, my_cmap.N)
        #pm = ax1.contourf(grid_lon, grid_lat, crdata, transform=ccrs.PlateCarree(), cmap=my_cmap, norm=norm, zorder=4)
        #cf = cr_array.plot.contourf(transform=ccrs.PlateCarree(), cmap=my_cmap, norm=norm, add_colorbar =False,alpha=1,add_labels=False)
        cf = ax1.contourf(grid_lon,grid_lat,crdata,transform=ccrs.PlateCarree(), cmap=my_cmap, norm=norm, alpha=1)

        # stationdata = pd.read_csv(value[1],encoding='gbk')
        # for index,row in stationdata.iterrows():
        #     ax1.text(row['LON2'], row['LAT2'], '●', color='black', zorder=3,fontsize=4)
        #     ax1.text(row['LON2']+0.002, row['LAT2']+0.002, row['SNAME'], color='black', zorder=3,fontsize=9,fontweight='1000')
        # plt.gca().xaxis.set_major_locator(plt.NullLocator())
        # plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95)
        plt.tight_layout(h_pad=0)
        ax1.set_extent(value[2])
        title = sitename +scantime_str + "雷达组合反射率实况图"
        title1 = value[5] + "_"+titletime_str
        # ax1.text(value[3][0], value[3][1], title, color='black', zorder=3,fontsize=16,fontweight='1000')
        shape_featrue = cfeature.ShapelyFeature(Reader(shppath).geometries(), ccrs.PlateCarree(), edgecolor='k', facecolor='none', linewidth=0.5, alpha=0.5)
        #shape_featrue1 = cfeature.ShapelyFeature(Reader(shp1_path).geometries(), ccrs.PlateCarree(), edgecolor='blue', facecolor='none', linewidth=1, alpha=1)
        # shape_featrue = cfeature.ShapelyFeature((dalian_border).geometry(), ccrs.PlateCarree(), edgecolor='k', facecolor='none', linewidth=1, alpha=1)
        ax1.add_feature(shape_featrue, zorder=5)
        diycolors = ['#01a0f6', '#00ecec', '#01ff00', '#00c800', '#019000', '#ffff00', '#e7c000', '#ff9000',
                  '#ff0000',
                  '#d60000', '#c00000', '#ff00f0', '#780084', '#ad90f0']
        cmap1 = ListedColormap(diycolors)
        sm = ScalarMappable(cmap=cmap1,norm=norm)
        sm.set_array([])
        rect = plt.Rectangle((0,0),1,1,fill=False,edgecolor='none')
        ax1.add_patch(rect)
        cbar = fig.colorbar(sm,ax=ax1,orientation='horizontal',fraction=0.1,shrink=0.4,pad=0.04)
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label(sitename+'雷达实况 ['+scantime_str+']'                     '[组合反射率(dbZ)]')
        cbar.set_ticks([0,5, 10,15,20,25,30,35,40,45,50,55,60,65,70])
        cbar.set_ticklabels([5, 10,15,20,25,30,35,40,45,50,55,60,65,70,75])
        #ax1.add_feature(shape_featrue1, zorder=10)
        labels=['5-10', '10-15','15-20','20-25','25-30','30-35','35-40','40-45','45-50','50-55','55-60','60-65','65-70','70以上']#指定bar的颜色
        image1 = "logo.png"
        img1 = plt.imread(image1)
        # fig.figimage(img1, 280, 690, zorder=4, alpha=1)#logo
        fig.figimage(img1, value[4][0], value[4][1], zorder=4, alpha=1)#logo
        color=['#01a0f6', '#00ecec', '#01ff00', '#00c800', '#019000', '#ffff00', '#e7c000', '#ff9000',
                      '#ff0000',
                      '#d60000', '#c00000', '#ff00f0', '#780084', '#ad90f0']
        patches = [ mpatches.Patch(color=color[i], label="{:s}".format(labels[i]) ) for i in range(len(color))]
        # ax1.legend(handles=patches, bbox_to_anchor=(1.0,0.24), ncol=2,title="图例(dbz)",framealpha=1)
        clip = maskout.shp2clip(cf, ax1, shppath, None)
        # ax1.add_feature(cfeature.LAND)
        #fig.savefig('test.png',bbox_inches='tight',dpi=400)
        # fig.colorbar(cf)
        target_folder = "./product/"+value[5]
        Path(target_folder).mkdir(parents=True, exist_ok=True)
        target_file = target_folder+"/"+title1+'.png'
        fig.savefig(target_file)
        # fig.savefig("test"+"/"+'test'+'.png')
    return None

if __name__ == "__main__":
    # getLastRadarFile()
    # radarfilelist = os.listdir('temp')
    # radarfilelist.sort(reverse=True)
    # radarlist = radarfilelist[0:1]
    # for x in radarlist:
    #     drawRadar(x)
    drawRadar("Z9411.20240501.145843.AR2.bz2")