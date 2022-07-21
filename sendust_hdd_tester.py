
#  HDD, SSD Write speed test python code by sendust  2022/7/21
#  
#  usage :
#     python sendust_hdd_tester.py d:\temp
#  Press Control-c to stop test
#
#  Improve instant speed display
#
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
    filename_log = os.getcwd() + "\\log\\" + log_prefix + datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
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
    if not os.path.isdir(dirname): 
        print("Specified argument is not a directory. Bailing out")
        sys.exit(1)
else:
    # no argument, so use current working directory
    dirname = os.getcwd()
    print("Using current working directory")

status_dir = "\nStart New Test........\nTarget folder is " + dirname + "\n" \
    "Free size is " + str(get_free_space_mb(dirname)) + " Mbytes \n"
    
print(status_dir)
updatelog(status_dir)

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
            print('[' , i , '] ' , "Instant writing speed: %.2f MB/s           " % (speed_block / 1024 / 1024), end="\r")
            count += 1
        diff = time.time() - start
        writesize = blocksize * count
        if diff:
            speed = writesize / diff
        else:
            speed = 0
        print("Disk writing speed: %.2f Mbytes per second          " % (speed / 1024 / 1024))
        updatelog("Disk writing speed: %.2f Mbytes per second          " % (speed / 1024 / 1024))
        hfile.close()

except KeyboardInterrupt:
    print("Keyboard interrupted")
    sys.exit(0)
    