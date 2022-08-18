from configparser import ConfigParser, NoSectionError
import os
import sys
import subprocess

class WebmConverter():

    def __init__(self) -> None:
        pass

    # def trim_video(self, start_time, end_time):
    #     while has_numbers(start_time) is False:
    #         start_time = input("Enter Video Start Time (HH:MM:SS / Secs): ")

    #     while has_numbers(end_time) is False:
    #         end_time = input("Enter Video End Time (HH:MM:SS / Secs): ")

    #     return start_time, end_time

    # def crop_video(self, crop_w, crop_h, crop_x, crop_y):
    #     crop_w, crop_h, crop_x, crop_y = "0"
    #     num = ""
    #     switcher = input("What type of crop?\n"
    #                      "0: None\n"
    #                      "1: To 4:3\n"
    #                      "2: To 16:9\n"
    #                      "3: From Top Right\n"
    #                      "4: From Center\n"
    #                      "5: Custom\n"
    #                     )

    #     switcher = {
    #         0: "pass",
    #         1: "crop=ih/3*4:ih",
    #         2: "crop=ih/16*9:ih",
    #         3: ""
    #         }
    #     return switcher.get(num, "Invalid Input")

    def calculate_bitrate(self, file_size, video_duration):
        video_size = int(file_size)
        video_length = int(video_duration)
        bitrate = int(((video_size * 1024 * 8) / video_length))
        return bitrate

    def set_file_name(self, file_name):
        if ".webm" in file_name:
            pass
        else:
            file_name += ".webm"
        return file_name

    def parse_config(self, quality, audio):
        configur = ConfigParser()
        path = os.getcwd()

        try:
            # On GitHub Instance
            sys.path.insert(0, "/home/runner/work/pyWebmConverter/pyWebmConverter/pyWebMConverter")            
            subprocess.run("ls")
            print ("Current directory:" +  (path))
            configur.read('conf.ini')
        except NoSectionError:
            # For local machine pytest
            print ("Current directory:" +  (path))
            subprocess.run("ls")
            configur.read('pyWebmConverter/conf.ini')
            print("Sections : ", configur.sections())
        finally:
            print("Sections : ", configur.sections())
            print(configur)
            pass


        print("Sections : ", configur.sections())
        print("Quality : ", configur.get('quality',f'{quality}'))
        print("Audio Enabled : ", configur.get('audio',f'{audio}'))

        audio_setting = configur.get('audio',f'{audio}')
        quality_setting = configur.get('quality',f'{quality}')

        return quality_setting, audio_setting

    def build_arg(self, input_video, quality, audio, bitrate, width, height,
                video_pass, file_name, file_size):
                args_list = []
                return args_list

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)
