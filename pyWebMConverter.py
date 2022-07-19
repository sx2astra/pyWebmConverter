import os
import subprocess
import sys
<<<<<<< HEAD
import unittest
=======
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5

inputVideo = sys.argv[1]

def convertToWebm(inputFile):
<<<<<<< HEAD
    bitrate = calculateBitrate()
    width, height = setResolution()
    #startTime, endTime = trimVideo()
    #cropW, cropH, cropX, cropY = cropVideo()

    outputFileName = ""
    while((outputFileName) == ""):
        outputFileName = input("Enter Output Filename: \n")
=======
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
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5

    if ".webm" in outputFileName:
        pass
    else:
        outputFileName += ".webm"
<<<<<<< HEAD
=======

    videoSize = int(outputFileSize)
    outputVideoDuration = int(inputVideoDuration)
    bitrate = int(((videoSize * 1024 * 8) / outputVideoDuration))
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
    
    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print((outputFileName), "\n\n")

    startButton = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if(startButton.lower() == "q"):
        return 0

<<<<<<< HEAD
    videoPass = 1
=======
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
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

<<<<<<< HEAD
def trimVideo():
    startTime = ""
    endTime = ""
    while(hasNumbers(startTime) == False):
        startTime = input("Enter Video Start Time (HH:MM:SS / Secs): ")

    while(hasNumbers(endTime) == False):
        endTime = input("Enter Video End Time (HH:MM:SS / Secs): ")

    return startTime, endTime

def cropVideo():
    cropW, cropH, cropX, cropY = "0"
    switcher = input("What type of crop?\n"
                     "0: None\n"
                     "1: To 4:3\n"
                     "2: To 16:9\n"
                     "3: From Top Right\n"
                     "4: From Center\n"
                     "5: Custom\n"
                    )

    switcher = {
        0: "pass",
        1: "crop=ih/3*4:ih",
        2: "crop=ih/16*9:ih",
        3: ""
        }
    return switcher.get(num, "Invalid Input")

def calculateBitrate():
    outputFileSize = ""
    inputVideoDuration = ""
    while(hasNumbers(outputFileSize) == False):
        outputFileSize = input("Enter Output Video Size (In MB): \n")
        print("\n")

    while(hasNumbers(inputVideoDuration) == False):
        inputVideoDuration = input("Enter Duration (In SECONDS): \n")
        print("\n")

    videoSize = int(outputFileSize)
    outputVideoDuration = int(inputVideoDuration)
    bitrate = int(((videoSize * 1024 * 8) / outputVideoDuration))
    return bitrate

def setResolution():
    width = ""
    height = ""
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

    return width, height

=======
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

convertToWebm(inputVideo)