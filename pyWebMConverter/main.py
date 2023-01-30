from tkinter import filedialog
from converter import *

root = tk.Tk()
root.withdraw()

def main():
    the_converter = WebmConverter()
    file_size = ""
    video_duration = ""
    file_name = ""
    width = ""
    height = ""
    quality_setting = ""
    audio_setting = ""
    
    input_video = filedialog.askopenfilename()
    print(input_video)

    while has_numbers(file_size) == False:
        file_size = input("Enter Output Video Size (In MB) : \n")
        print("\n")

    while has_numbers(video_duration) == False:
        video_duration = input("Enter Duration (In SECONDS) : \n")
        print("\n")

    while file_name == "":
        file_name = input("Enter Output Filename : \n")
        print("\n")

    while has_numbers(width) == False:
        width = input("Enter Output Width (Default: 1280) : \n")
        print("\n")
        if width == "":
            width = "1280"

    while has_numbers(height) == False:
        height = input(
            "Enter Output Height (Default: -1 To Maintain Aspect" " Ratio) : \n"
        )
        print("\n")
        if height == "":
            height = "-1"

    while quality_setting not in ["high", "mid", "low"]:
        quality_setting = input("Select Quality High | Mid | Low : \n")
        print("\n")
        quality_setting = quality_setting.lower()

    while audio_setting not in ["on", "off"]:
        audio_setting = input("Enter Audio Enablement On | Off : \n")
        print("\n")
        audio_setting = audio_setting.lower()

    bitrate = the_converter.calculate_bitrate(file_size, video_duration)
    file_name = the_converter.set_file_name(file_name)
    #quality_setting, audio_setting = the_converter.parse_config(
    #    quality_setting, audio_setting
    #)

    print(f"{width} x {height} Video Resolution")
    print((bitrate), " KB/s")
    print("Audio: ", audio_setting.upper())
    print((quality_setting.upper()), " Settings")
    print((file_name), "\n\n")

    start_button = input("Enter To Start Conversion. Enter 'Q' to Quit. ")
    if start_button.lower() == "q":
        return 0

    video_pass = 1
    while video_pass <= 2:
        cmd = f"ffmpeg.exe -i {input_video} -c:v libvpx-vp9 -pass {video_pass} -b:v {bitrate}K -threads 16 -speed 0 -crf 12 -vf scale={width}:{height} -tile-columns 0 -tile-columns 0 -auto-alt-ref 1 -lag-in-frames 25 -row-mt 1 -g 600 -aq-mode 0 -an -f webm .\Output\{file_name}"
        
        subprocess.run(cmd, shell=True)
        video_pass += 1
    
    print("Conversion Complete!\n")
    input(f"File Avaliable at .\Output\{file_name}")
    return 0

if __name__ == "__main__":
    main()
