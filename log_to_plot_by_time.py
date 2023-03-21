#  log to plot by sendust
#
#  Last edit : 2022/8/9
# 
#  2023/2/2   set yscale from df[speed] max
#             modified from log_to_plot (Freespace -> timestamp)
#  2023/2/8   support hangul font
#             Show minimun value, time stamp
#
#


import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
import sys, os

    
if len(sys.argv) >= 2:
    file_log = sys.argv[1]
    pre, ext = os.path.splitext(file_log)
    file_png = pre + ".png"
    print(file_png)
else:
    print("\r\nUsage....\r\npython log_to_plot_by_time.py test.log")
    print("code managed by sendust")
    sys.exit(1)

fontpath = os.path.realpath(os.path.dirname(__file__)) + "\\font\\naverdic.ttf"
fontprop = fm.FontProperties(fname=fontpath)
plt.rcParams["figure.figsize"] = [10, 6]


df = {}
df['freespace'] = []
df['speed'] = []
df['timestamp'] = []

hlogfile = open(file_log, "r")
lines = hlogfile.readlines()
for eachline in lines:
    if "speed:" in eachline:
        parser = eachline.split(" ")
        #print(parser[6], parser[12])
        df['speed'].append(float(parser[6]))
        df['freespace'].append(parser[12])
        df['timestamp'].append(parser[0] + " " + parser[1])
    elif "Target folder is" in  eachline:
        targetfolder = eachline
    
hlogfile.close()

print(targetfolder)
print("Get speed data ... " + str(len(df['speed'])))
print("Get freespace data ... " + str(len(df['freespace'])))
print("Show first 10 data")
try:
    for idx in range(10):
        print(df['speed'][idx], end="    ")
        print(df['freespace'][idx])
except:
    print("No more data .... ")

min_value = min(df['speed'])
min_index = df['speed'].index(min(df['speed']))
str_min = "Minimum speed is " + str(min(df['speed'])) + " MB/s  " + df['timestamp'][min_index]
print(str_min)

#plt.plot(df['freespace'], df['speed'])
plt.plot(df['timestamp'], df['speed'], '.g', markersize=2)
plt.xlabel("time")
plt.ylabel("speed[MB/s]")

#print(df["freespace"])
#print(len(df["freespace"]))
xindex_max = len(df["timestamp"])-1
xindex_mid = int(xindex_max / 2)
plt.grid()
plt.ylim([0, max(df['speed'])])
plt.xticks([df["timestamp"][0], df["timestamp"][xindex_mid], df["timestamp"][xindex_max]])
plt.title(targetfolder, fontproperties=fontprop)
plt.text(0, 0, str_min, fontsize=10)
plt.savefig(file_png)
plt.show()

