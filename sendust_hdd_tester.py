
#  HDD, SSD Write speed test python code by sendust  2022/7/28
#  
#  usage :
#     python sendust_hdd_tester.py "d:/temp"
#     python sendust_hdd_tester.py "//jungbi2/media"
#  Press Control-c to stop test
#
#  Improve instant speed display
#
#  2022 7/28 improve logging (write dirname)
#            Support UNC path
#  2022/7/29 Report free space every loop
#
#



import time, os, sys, datetime, ctypes, platform

filesize = 1024          # write file size, unit in MB
blocksize = 1024 * 1024      # Create 1MB. unit in bytes  (do not change this value !!)

buffer = bytes(b'a') * blocksize     # Create 1MB buffer for block write
speed_block_prev = 0


def updatelog(*args, end="\n"):  
    log_prefix = "HDD_speed_tester_"
    if not os.path.exists(os.getcwd() + "\\log"):
        print("path not exist.. make one")
        os.mkdir(os.getcwd() + "\\log")
    filename_log = os.getcwd() + "\\log\\" + log_prefix + datetime.datetime.now().strftime("%Y-%m-%d_[") + str(os.getpid()) + "].log"
    #print("log file name is " + filename_log)
    result = ""
    # date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S ")
    for value in args:
        result += str(value)
    
    #print(result, end=end)
    with open(filename_log, "a") as the_file:
        the_file.write(str(datetime.datetime.now()) + "  "  + result + end)   
        
        
def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024
        

if len(sys.argv) >= 2:
    dirname = sys.argv[1]
    # dirname = dirname.replace("\\", '/')
    #if not os.path.isdir(dirname): 
    #    print("Specified argument is not a directory. Bailing out")
    #    sys.exit(1)
else:
    # no argument, so use current working directory
    dirname = os.getcwd()
    print("Using current working directory")

str_report = "\nStart New Test........\nTarget folder is " + dirname + "\n" \
    "Free size is " + str(get_free_space_mb(dirname)) + " Mbytes \n"

print(str_report)
updatelog(str_report)

try:
    with open(os.path.join(dirname, "writetest.txt"), "a") as the_file:
        the_file.write("\nFile writing test.........\n")
except:
    print("Error writing file... check path exist or access control")
    updatelog("Error writing file... check path exist or access control")
    sys.exit(1)


try:

    while True:
        filename = os.path.join(dirname,"WriteTestFile_" + "{:.2f}".format(time.time()) + ".bin")

        hfile = open(filename, "wb")


        start = time.time()
        count = 0
        for i in range(0, filesize):
            start_block = time.time()
            hfile.write(buffer)
            diff_block = time.time() - start_block
            if diff_block:
                speed_block = blocksize / diff_block
            else:
                speed_block = speed_block_prev
            speed_block_prev = speed_block
            print('[' , i , '] ' , "Instant writing speed: %.2f MB/s     " % (speed_block / 1024 / 1024), end="\r")
            count += 1
        diff = time.time() - start
        writesize = blocksize * count
        if diff:
            speed = writesize / diff
        else:
            speed = 0
        str_report = "Disk writing speed: {0:.2f} MB/s  free space is {1:.2f} MB".format( speed / 1024 / 1024, get_free_space_mb(dirname))
        print(str_report)
        updatelog(str_report)
        hfile.close()

except KeyboardInterrupt:
    print("Keyboard interrupted")
    sys.exit(0)
    
