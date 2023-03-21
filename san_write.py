
#  HDD, SSD Write speed test python code by sendust  2022/7/28
#  
#  usage :
#     python san_write.py --dest c:\temp --size 100
#   
#     Press Control-c to stop test
#
#  Improve instant speed display
#
#  2022 7/28 improve logging (write dirname)
#            Support UNC path
#  2022/7/29 Report free space every loop
#  2023/2/2  add argparser, size limit
#  2023/2/3  time estimation includes file handle open and close



import time, os, sys, datetime, ctypes, platform, argparse

filesize = 1024          # write file size, unit in MB
blocksize = 1024 * 1024      # Create 1MB. unit in bytes  (do not change this value !!)

buffer = bytes(b'a') * blocksize     # Create 1MB buffer for block write
speed_block_prev = 0
parser = argparse.ArgumentParser(description = 'Write block data and estimate speed',
    epilog='Code managed by sendust (sendust@sbs.co.kr)')

parser.add_argument('--dest', help='destination path, ex: c:\\temp', default='.')
parser.add_argument('--size', help='Total write file size in GB, ex: 100', type=int, default=10)

args=parser.parse_args()
if (len(sys.argv) <= 1):
    print(parser.print_help())
    sys.exit(1)


def updatelog(*args, end="\n"):  
    log_prefix = "HDD_speed_write_tester_"
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
        

dirname = args.dest
size_limit = args.size * 1000 * 1000 * 1000 # change GB to bytes
if (dirname == '.'):
    dirname = os.getcwd()

print("test destination folder is " + dirname)
print("size limit is " + f'{size_limit:,}' + " Bytes")


if not os.path.exists(dirname):
    print("destination folder is not exist.. exit program..")
    sys.exit(1)

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

size_total = 0

try:

    while True:
        filename = os.path.join(dirname,"WriteTestFile_" + "{:.2f}".format(time.time()) + ".bin")
        start = time.time()
        hfile = open(filename, "wb")

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
        hfile.close()
        diff = time.time() - start
        writesize = blocksize * count
        if diff:
            speed = writesize / diff
        else:
            speed = 0
        str_report = "Disk writing speed: {0:.2f} MB/s  free space is {1:.2f} MB".format( speed / 1024 / 1024, get_free_space_mb(dirname))
        size_total += writesize
        print(str_report + "  [" + f'{size_total:,}'   + "]")
        updatelog(str_report)

        if (size_total > size_limit):
            print("Reaches size limit..")
            break

except KeyboardInterrupt:
    print("Keyboard interrupted")
    sys.exit(0)

sys.exit(1)