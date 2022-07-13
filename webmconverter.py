import os
import subprocess
import sys

dropped_file = sys.argv[1]

def convert_to_webm(inputFile):
    file_size_input = ""
    file_name_input = ""
    file_duration_input = ""
    height = ""
    width = ""

    while(has_numbers(file_size_input) == False):
        file_size_input = input("Enter Output Video Size (In MB): ")

    while(has_numbers(file_duration_input) == False):
        file_duration_input = input("Enter Duration (In SECONDS): ")

    while((file_name_input) == ""):
        file_name_input = input("Enter Output Filename: ")

    while(has_numbers(width) == False):
        width = input("Enter Output Width (Default: 1280): ")
        if(width == ""):
            width = "1280"

    while(has_numbers(height) == False):
        height = input("Enter Output Height (Default: -1 To Maintain Aspect" 
                       " Ratio): ")
        if(height == ""):
            height = "-1"

    if ".webm" in file_name_input:
        pass
    else:
        file_name_input += ".webm"

    video_size = int(file_size_input)
    video_seconds = int(file_duration_input)
    bitrate = int(((video_size * 1024 * 8) / video_seconds))
    
    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print(file_name_input)

    start_button = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if(start_button.lower() == "q"):
        return 0

    subprocess.call(["ffmpeg.exe", '-i', f'{dropped_file}', '-c:v', 
                     'libvpx-vp9', '-pass', '1', '-b:v', f'{bitrate}K', 
                     '-threads', '16', '-speed', '0', '-vf', 
                     f'scale={width}:{height}', '-tile-columns', '0', 
                     '-frame-parallel', '0', '-auto-alt-ref', '1', 
                     '-lag-in-frames', '25', '-g', '600', '-aq-mode', '0', 
                     '-an', '-f', 'webm',f'{file_name_input}'])

    subprocess.call(["ffmpeg.exe", '-i', f'{dropped_file}', '-c:v', 
                     'libvpx-vp9', '-pass', '2', '-b:v', f'{bitrate}K', 
                     '-threads', '16', '-speed', '0', '-vf', 
                     f'scale={width}:{height}', '-tile-columns', '0', 
                     '-frame-parallel', '0', '-auto-alt-ref', '1', 
                     '-lag-in-frames', '25', '-g', '600', '-aq-mode', '0', 
                     '-an', '-f', 'webm',f'{file_name_input}'])
    pass

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

convert_to_webm(dropped_file)