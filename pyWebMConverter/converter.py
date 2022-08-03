class webMConverter:
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

    def calculateBitrate(outputFileSize, inputVideoDuration):
        videoSize = int(outputFileSize)
        outputVideoDuration = int(inputVideoDuration)
        bitrate = int(((videoSize * 1024 * 8) / outputVideoDuration))
        return bitrate

    def setFileName(outputFileName):
        if ".webm" in outputFileName:
            return outputFileName
        else:
            outputFileName += ".webm"
            return outputFileName

def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)