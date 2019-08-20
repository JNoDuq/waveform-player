from sys import argv
import sys
import argparse
import subprocess
import time
import os
import json



ffprobe_path = "ffprobe"
local_path = os.path.dirname(os.path.abspath(__file__))
ffplay_path = local_path + "/ffplay"



class videoFile(object):
    def __init__(self, input_file = None, style = None, components = None):
        super(videoFile, self).__init__()

        self.ffprobe_path = ffprobe_path
        self.ffplay_path = ffplay_path
        self.input_file = input_file
        self.style = style 
        self.components = components

        self.get_video_info()
        self.play_video_with_waveform()

    def get_video_info(self):

        ffprobe_cmd = "{0} -loglevel quiet -print_format json -show_streams -select_streams v -i {1}".format(self.ffprobe_path, self.input_file)

        result = subprocess.check_output(ffprobe_cmd, shell=True)
        self.ffprobe_results =  json.loads(result)
        self.input_file_width = self.ffprobe_results['streams'][0]['width']
        self.input_file_height = self.ffprobe_results['streams'][0]['height']

        try :
            sar = self.ffprobe_results['streams'][0]['sample_aspect_ratio']
            sar = sar.split(":")
            s = '/'
            self.sar = s.join(sar)

        except:
            self.sar = "1/1"

        #print (self.sar)


    def play_video_with_waveform(self):


        if self.style == "full" : 


            ffplay_cmd = '''{} -i {} -vf "waveform=display=parade:components={}:mirror=1:graticule=green:flags=numbers+dots,scale={}x{},setsar={}"'''.format(self.ffplay_path, self.input_file, self.components, self.input_file_width, self.input_file_height, self.sar)
 

        if self.style == "bar" : 
            self.ffplay_height = int(round(int(self.input_file_height)*1))
            self.ffplay_width = round(int(self.input_file_width)*0.70)

            self.video_height = round(int(self.input_file_height)*0.70)
            self.video_width = round(int(self.input_file_width)*0.70)

            self.waveform_height = round(int(self.input_file_height)*0.30)
            self.wavefom_width = round(int(self.input_file_width)*0.70)

            ffplay_cmd = '''{} -i {} -vf "split=3[a][b][c],[a]scale={}x{}[aa],[c]scale={}x{}[cc],[b]waveform=display=parade:components={}:mirror=1:graticule=green:flags=numbers+dots,scale={}x{}[bb],[cc][bb]overlay=0:main_h-{}[cb],[cb][aa]overlay=0:0,setsar={}"'''.format(self.ffplay_path, self.input_file, self.video_width, self.video_height,  self.ffplay_width, self.ffplay_height, self.components, self.wavefom_width, self.waveform_height, self.waveform_height, self.sar)
 

        if self.style == "split" : 
            self.ffplay_height = int(round(int(self.input_file_height)*1))
            self.ffplay_width = round(int(self.input_file_width)*0.50)

            self.video_height = round(int(self.input_file_height)*0.50)
            self.video_width = round(int(self.input_file_width)*0.50)

            self.waveform_height = round(int(self.input_file_height)*0.50)
            self.wavefom_width = round(int(self.input_file_width)*0.50)

            ffplay_cmd = '''{} -i {} -vf "split=3[a][b][c],[a]scale={}x{}[aa],[c]scale={}x{}[cc],[b]waveform=display=parade:components={}:mirror=1:graticule=green:flags=numbers+dots,scale={}x{}[bb],[cc][bb]overlay=0:main_h-{}[cb],[cb][aa]overlay=0:0,setsar={}"'''.format(self.ffplay_path, self.input_file, self.video_width, self.video_height,  self.ffplay_width, self.ffplay_height, self.components,self.wavefom_width, self.waveform_height, self.waveform_height, self.sar)
            #ffplay_cmd = '''{} -i {} -vf "split=3[a][b][c],[a]scale={}x{}[aa],[c]scale={}x{}[cc],[b]scale={}x{},format=yuv420p10,waveform=display=parade:components=1:mirror=1:graticule=green:flags=numbers+dots[bb],[cc][bb]overlay=0:main_h-{}[cb],[cb][aa]overlay=0:0,setsar=1/1"'''.format(self.ffplay_path, self.input_file, self.video_width, self.video_height,  self.ffplay_width, self.ffplay_height, self.wavefom_width, self.waveform_height, self.waveform_height)


        if self.style == "blend":
            self.ffplay_height = int(round(int(self.input_file_height)*1))
            self.ffplay_width = round(int(self.input_file_width)*0.70)

            self.video_height = round(int(self.input_file_height)*0.70)
            self.video_width = round(int(self.input_file_width)*0.70)

            self.waveform_height = round(int(self.input_file_height)*0.30)
            self.wavefom_width = round(int(self.input_file_width)*0.70)

            ffplay_cmd = '''{} -i {} -vf "split=2[a][b],[b]waveform=display=parade:components={}:mirror=1:graticule=green:flags=numbers+dots:display=parade,scale={}x{},setsar={}[bb],[a][bb]blend=all_mode='overlay':c0_opacity=7/10"'''.format(self.ffplay_path, self.input_file, self.components, self.input_file_width, self.input_file_height,  self.ffplay_width, self.ffplay_height, self.wavefom_width, self.waveform_height, self.waveform_height, self.sar)
 

        print(ffplay_cmd)
        ffplay = subprocess.check_output(ffplay_cmd, shell=True)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input', help="INPUT FILE")
    parser.add_argument('-style', dest='style', help="Style : bar, split, blend, full", default = "bar")
    parser.add_argument('-color', dest='color', action='store_true', help="Show color")

    args = parser.parse_args()
    input_file = args.input
    style = args.style
    color = args.color


    local_path = os.path.dirname(os.path.abspath(__file__))


    if color:
        components = 7
    else:
        components = 1


    foo = videoFile(input_file = input_file, style = style , components = components)



