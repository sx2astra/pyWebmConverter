import subprocess
import sys

from pyWebMConverter import *

def main():
    fileSize = ""
    videoDuration = ""
    fileName = ""
    width = ""
    height = ""
    inputVideo = sys.argv[1]


    while(hasNumbers(fileSize) == False):
        fileSize = input("Enter Output Video Size (In MB): \n")
        print("\n")

    while(hasNumbers(videoDuration) == False):
        videoDuration = input("Enter Duration (In SECONDS): \n")
        print("\n")

    bitrate = webMConverter.calculateBitrate(fileSize, videoDuration)

    while((fileName) == ""):
        fileName = input("Enter Output Filename: \n")
        print("\n")

    fileName = webMConverter.setFileName(fileName)

    while(hasNumbers(width) == False):
        width = input("Enter Output Width (Default: 1280): \n")
        print("\n") 
        if(width == ""):
            width = "1280"

    while(hasNumbers(height) == False):
        height = input("Enter Output Height (Default: -1 To Maintain Aspect" 
                       " Ratio): \n")
        print("\n")
        if(height == ""):
            height = "-1"

    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print((fileName), "\n\n")

    startButton = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if(startButton.lower() == "q"):
            return 0
    
    videoPass = 1
    while(videoPass <= 2):
        subprocess.call(["ffmpeg.exe", '-i', f'{inputVideo}', '-c:v', 
                         'libvpx-vp9', '-pass', f'{videoPass}', '-b:v', 
                         f'{bitrate}K', '-threads', '16', '-speed', '0', 
                         '-crf', '12', '-vf', f'scale={width}:{height}', 
                         '-tile-columns', '0', '-frame-parallel', '0', 
                         '-auto-alt-ref', '1', '-lag-in-frames', '25', 
                         '-row-mt', '1', '-g', '600', '-aq-mode', '0', '-an', 
                         '-f', 'webm',f'.\Output\{fileName}']
                         )
        videoPass += 1

    print("Conversion Complete!\n")
    input(f"File Avaliable at .\Output\{fileName}")
    return 0

if __name__=="__main__":
    main()