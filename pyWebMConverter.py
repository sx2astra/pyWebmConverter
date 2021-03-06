import os
import subprocess
import sys

inputVideo = sys.argv[1]

def convertToWebm(inputFile):
    outputFileSize = ""
    outputFileName = ""
    inputVideoDuration = ""
    height = ""
    width = ""
    videoPass = 1

    while(hasNumbers(outputFileSize) == False):
        outputFileSize = input("Enter Output Video Size (In MB): \n")
        print("\n")

    while(hasNumbers(inputVideoDuration) == False):
        inputVideoDuration = input("Enter Duration (In SECONDS): \n")
        print("\n")

    while((outputFileName) == ""):
        outputFileName = input("Enter Output Filename: \n")
        print("\n")

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

    if ".webm" in outputFileName:
        pass
    else:
        outputFileName += ".webm"

    videoSize = int(outputFileSize)
    outputVideoDuration = int(inputVideoDuration)
    bitrate = int(((videoSize * 1024 * 8) / outputVideoDuration))
    
    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print((outputFileName), "\n\n")

    startButton = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if(startButton.lower() == "q"):
        return 0

    while(videoPass <= 2):
        subprocess.call(["ffmpeg.exe", '-i', f'{inputVideo}', '-c:v', 
                         'libvpx-vp9', '-pass', f'{videoPass}', '-b:v', 
                         f'{bitrate}K', '-threads', '16', '-speed', '0', 
                         '-crf', '12', '-vf', f'scale={width}:{height}', 
                         '-tile-columns', '0', '-frame-parallel', '0', 
                         '-auto-alt-ref', '1', '-lag-in-frames', '25', 
                         '-row-mt', '1', '-g', '600', '-aq-mode', '0', '-an', 
                         '-f', 'webm',f'.\Output\{outputFileName}']
                         )
        videoPass += 1

    print("Conversion Complete!\n")
    input(f"File Avaliable at .\Output\{outputFileName}")
    pass

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

convertToWebm(inputVideo)