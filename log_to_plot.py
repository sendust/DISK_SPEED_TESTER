#  log to plot by sendust
#
#  Last edit : 2022/8/9
#
#
#
#
#

import matplotlib.pyplot as plt
import sys, os

    
if len(sys.argv) >= 2:
    file_log = sys.argv[1]
    pre, ext = os.path.splitext(file_log)
    file_png = pre + ".png"
    print(file_png)
else:
    print("Usage....\r\nplot.py test.csv")
    sys.exit(1)

plt.rcParams["figure.figsize"] = [10, 6]

df = {}
df['freespace'] = []
df['speed'] = []

hlogfile = open(file_log, "r")
lines = hlogfile.readlines()
for eachline in lines:
    if "speed:" in eachline:
        parser = eachline.split(" ")
        #print(parser[6], parser[12])
        df['speed'].append(float(parser[6]))
        df['freespace'].append(parser[12])
    elif "Target folder is" in  eachline:
        targetfolder = eachline
    
hlogfile.close()

print("Target folder is " + targetfolder)
print("Get speed data ... " + str(len(df['speed'])))
print("Get freespace data ... " + str(len(df['freespace'])))
print("Show first 10 data")
try:
    for idx in range(10):
        print(df['speed'][idx], end="    ")
        print(df['freespace'][idx])
except:
    print("No more data .... ")



#plt.plot(df['freespace'], df['speed'])
plt.plot(df['freespace'], df['speed'], '.g', markersize=2)
plt.xlabel("freespace(MB)")
plt.ylabel("speed(MB/s)")

#print(df["freespace"])
#print(len(df["freespace"]))
xindex_max = len(df["freespace"])-1
xindex_mid = int(xindex_max / 2)
plt.grid()
plt.ylim([0, 2000])
plt.xticks([df["freespace"][0], df["freespace"][xindex_mid], df["freespace"][xindex_max]])
plt.title(targetfolder)
plt.savefig(file_png)
plt.show()

