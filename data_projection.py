import math as m
import json
import datetime
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt

# setting constants
datetimeFormat = '%Y-%m-%d %H:%M:%S'
p = {}


def plot_map():
    # Downloaded from http://biogeo.ucdavis.edu/data/gadm2/shp/DEU_adm.zip
    fname = 'map/gadm36_CHN_0.shp'

    adm1_shapes = list(shpreader.Reader(fname).geometries())

    ax = plt.axes(projection=ccrs.PlateCarree())

    plt.title('Deutschland')
    ax.coastlines(resolution='10m')

    ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                      edgecolor='black', facecolor='gray', alpha=0.5)

    ax.set_extent([4, 16, 47, 56], ccrs.PlateCarree())

    plt.show()


def map_function(d_s, d_t):
    d = {}
    # fragment_dict = DictList()
    relative_null_point = {'latitude': 39.75872, 'longitude': 116.04142}
    for i in range(182):  # change to accomodate number of users
        user_str = '%03d' % i
        with open('processing/parsed_data/output_' + user_str + '.txt') as f:
            print(user_str)
            for line in f:
               print(line)
    print("Tiles generated")
    print("No of tiles are: " + str(len(d.keys())) + str(d_s) + str(d_t))
    with open("processing/structure/json_structure_" + str(d_s) + "_" + str(d_t) + ".csv", 'w') as f:
        json.dump(d, f)
    # with open("structure/json_structure_"+str(ds)+"_"+str(dt)+".txt") as f:
    #     load_dict = json.load(f)


ds = 200  # 100 500 1000
dt = 500  # 300 600 1200
# map_function(ds, dt)  # call based on ds and dt
plot_map()