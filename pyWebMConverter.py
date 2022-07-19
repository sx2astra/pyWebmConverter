import os
import subprocess
import sys
<<<<<<< HEAD
<<<<<<< HEAD
import unittest
=======
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
=======
import unittest
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc

inputVideo = sys.argv[1]

def convertToWebm(inputFile):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc
    bitrate = calculateBitrate()
    width, height = setResolution()
    #startTime, endTime = trimVideo()
    #cropW, cropH, cropX, cropY = cropVideo()

<<<<<<< HEAD
    outputFileName = ""
    while((outputFileName) == ""):
        outputFileName = input("Enter Output Filename: \n")
=======
    outputFileSize = ""
=======
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc
    outputFileName = ""
    while((outputFileName) == ""):
        outputFileName = input("Enter Output Filename: \n")
<<<<<<< HEAD
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
=======
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc

    if ".webm" in outputFileName:
        pass
    else:
        outputFileName += ".webm"
<<<<<<< HEAD
<<<<<<< HEAD
=======

    videoSize = int(outputFileSize)
    outputVideoDuration = int(inputVideoDuration)
    bitrate = int(((videoSize * 1024 * 8) / outputVideoDuration))
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
=======
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc
    
    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print((outputFileName), "\n\n")

    startButton = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if(startButton.lower() == "q"):
        return 0

<<<<<<< HEAD
<<<<<<< HEAD
    videoPass = 1
=======
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
=======
    videoPass = 1
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc
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
<<<<<<< HEAD
=======
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc
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

<<<<<<< HEAD
=======
>>>>>>> acee6f656749e8adcd37a0f64475a2b98bb7ceb5
=======
>>>>>>> b2f45ca8860d7e83b1de09c18d56d7fac7b8d3fc
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

convertToWebm(inputVideo)