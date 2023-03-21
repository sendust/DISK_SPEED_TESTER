
#  HDD, SSD read speed test python code by sendust  2022/7/28
#  
#  usage :
#     python san_read.py --dest c:\temp
#   
#     Press Control-c to stop test
#
#  Improve instant speed display
#
#  2022 7/28 improve logging (write dirname)
#            Support UNC path
#  2022/7/29 Report free space every loop
#  2023/2/2  Modify code from write test
#



import time, os, sys, datetime, ctypes, platform, argparse, glob

filesize = 1024          # write file size, unit in MB

speed_block_prev = 0
parser = argparse.ArgumentParser(description = 'Read block data and estimate speed',
    epilog='Code managed by sendust (sendust@sbs.co.kr)')

parser.add_argument('--dest', help='destination path, ex: c:\\temp', default='.')

args=parser.parse_args()
if (len(sys.argv) <= 1):
    print(parser.print_help())
    sys.exit(1)


def updatelog(*args, end="\n"):  
    log_prefix = "HDD_speed_read_tester_"
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

if (dirname == '.'):
    dirname = os.getcwd()

print("test destination folder is " + dirname)


if not os.path.exists(dirname):
    print("destination folder is not exist.. exit program..")
    sys.exit(1)

str_report = "\nStart New Test........\nTarget folder is " + dirname + "\n" \
    "Free size is " + str(get_free_space_mb(dirname)) + " Mbytes \n"

print(str_report)
updatelog(str_report)

try:
    list_file = glob.glob(os.path.join(dirname, "*.bin"))
except:
    print("Error reading file list... check path exist or access control")
    updatelog("Error writing file... check path exist or access control")
    sys.exit(1)

print("Number of bin files = " + str(len(list_file)))


speed_prev = 0
count_read = 20000
try:

    while count_read:
        for i, filename in enumerate(list_file):
            if not os.path.exists(filename):
                print("test file is removed form folder.. skip file..  " + filename)
                continue
            start = time.time()
            hfile = open(filename, "rb")
            print("open and read file to buffer // " + filename)

            contents = hfile.read()         #
            hfile.close()
            diff_time = time.time() - start
            blocksize = len(contents)
            if diff_time:
                speed = blocksize / diff_time
            else:
                speed = speedprev
            speed_prev = speed
            print("ETA ... " + str(count_read))
            print('[' , i , '/', str(len(list_file)) , '] ' , "Instant read speed: %.2f MB/s     " % (speed / 1024 / 1024))

            str_report = "Disk read speed: {0:.2f} MB/s  free space is {1:.2f} MB".format( speed / 1024 / 1024, get_free_space_mb(dirname))
            print(str_report)
            updatelog(str_report)
            count_read -= 1



except KeyboardInterrupt:
    print("Keyboard interrupted")
    sys.exit(1)
