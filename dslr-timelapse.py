from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

TIMELAPSE_INTERVAL = 30

#kill gphoto2 process that starts whenever we connect the camera
def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], [stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    #search for the line that has the process we want to kill
    for line in out.spitlines():
        if b'gvfsd-gphoto2' in line:
            #Kill the process!
            pid = int(line.split(None, 1) [0])
            os.kill(pid, signal.SIGKILL)
            
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "PiShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID 
save_location = "/home/pi/Desktop/gphoto2/images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory.")
        os.chdir(save_location)
        
def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)
    
# TODO add camera name to the name string
    def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) <13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Renamed the CR2")
                
killphoto2process()
gp(clearCommand)

while True:
    createSaveFolder()
    captureImages()
    renameFiles(picID)
    sleep(TIMELAPSE_INTERVAL)
    
    
# Check if there is enough space in sd, ssd, internal storage
# send picture every hour
# Control exposure
# Create logs
# Connect remotely through VNC 
# Scollect and end email with various pre-defined logs
# Check and send lan + external IP
