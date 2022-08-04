import subprocess
import sys

from converter import *

def main():
    file_size = ""
    video_duration = ""
    file_name = ""
    width = ""
    height = ""
    input_video = sys.argv[1]


    while has_numbers(file_size) == False:
        file_size = input("Enter Output Video Size (In MB): \n")
        print("\n")

    while has_numbers(video_duration) == False:
        video_duration = input("Enter Duration (In SECONDS): \n")
        print("\n")

    bitrate = WebmConverter.calculate_birate(file_size, video_duration)

    while((file_name) == ""):
        file_name = input("Enter Output file_name: \n")
        print("\n")

    file_name = WebmConverter.set_file_name(file_name)

    while(has_numbers(width) == False):
        width = input("Enter Output Width (Default: 1280): \n")
        print("\n") 
        if(width == ""):
            width = "1280"

    while(has_numbers(height) == False):
        height = input("Enter Output Height (Default: -1 To Maintain Aspect" 
                       " Ratio): \n")
        print("\n")
        if(height == ""):
            height = "-1"

    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print((file_name), "\n\n")

    start_button = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if(start_button.lower() == "q"):
            return 0
    
    video_pass  = 1
    while(video_pass <= 2):
        subprocess.call(["ffmpeg.exe", '-i', f'{input_video}', '-c:v', 
                         'libvpx-vp9', '-pass', f'{video_pass}', '-b:v', 
                         f'{bitrate}K', '-threads', '16', '-speed', '0', 
                         '-crf', '12', '-vf', f'scale={width}:{height}', 
                         '-tile-columns', '0', '-frame-parallel', '0', 
                         '-auto-alt-ref', '1', '-lag-in-frames', '25', 
                         '-row-mt', '1', '-g', '600', '-aq-mode', '0', '-an', 
                         '-f', 'webm',f'.\Output\{file_name}']
                         )
        video_pass += 1

    print("Conversion Complete!\n")
    input(f"File Avaliable at .\Output\{file_name}")
    return 0

if __name__=="__main__":
    main()