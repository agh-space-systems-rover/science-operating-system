#!/usr/bin/env python3

# SCIENCE OPERATING SYSTEM
import subprocess
from typing import List
from dataclasses import dataclass
from pathlib import Path
import re
import sys

BOLD = '\033[1m'
END = '\033[0m'
GREEN = '\033[92m'
BLUE = '\033[94m'

@dataclass
class Video():
    start: int
    path: Path

class ScienceOperatingSystem:
    def __init__(self, files: List[str]):
        self.start = 0
        self.videos = []
        accumulated_time = 0
        for file in files:
            video_len = self._get_video_length(file)
            self.videos.append(Video(accumulated_time, file))
            accumulated_time += video_len

        accumulated_time /= 1000
        minutes = int(accumulated_time//60)
        seconds = int(accumulated_time)%60

        print(f"GOT {len(self.videos)} VIDEOS, TOTAL TIME: {minutes}:{seconds}")

    # REAL TIME = self.start + timestamp

    def _get_video_length(self, filepath: str):
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(filepath)
        minutes = int(clip.duration//60)
        seconds = int(clip.duration)%60

        print(f"VIDEO {filepath}: {minutes}:{seconds}")
        return (minutes*60 + seconds)*1000

    def _get_video_from_time(self, timestamp: int):
        for i in range(1, len(self.videos)):
            if self.videos[i].start > self.start+timestamp:
                return self.videos[i-1]
        return self.videos[-1]

    def _start(self, timestamp: int):
        self.start = timestamp

    def _go(self, timestamp: int):
        video = self._get_video_from_time(timestamp)
        time = timestamp + self.start - video.start
        p = subprocess.Popen(f"vlc --start-time={time//1000}.{(time%1000)//10} {video.path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

    def _convert_to_miliseconds(self, input_time: str):
        # input_time "XXXX:YY"
        
        minutes, seconds = map(int, input_time.strip().split(":"))
        return (minutes*60 + seconds)*1000

    def run(self):
        print(BOLD + GREEN + "SCIENCE OPERATING SYSTEM OPERATIONAL" + END)
        try:
            while (cmd := input(BOLD + BLUE + "SOS SHELL >> " + END).strip()) != "exit":
                if cmd.isspace() or len(cmd) == 0:
                    pass
                elif re.match(r"go [0-9]+:[0-9][0-9]", cmd):
                    input_time = cmd[len("go")+1:]
                    timestamp = self._convert_to_miliseconds(input_time)

                    try:
                        self._go(timestamp)
                    except KeyboardInterrupt:
                        print()
                elif re.match(r"start [0-9]+:[0-9][0-9]", cmd):
                    input_time = cmd[len("start")+1:]
                    timestamp = self._convert_to_miliseconds(input_time)
                    self._start(timestamp)
                    print(BOLD + "START TIME SET" + END)
                else:
                    print(BOLD + "USAGE:" + END)
                    print("start MM:SS  -> Setup rover start time")
                    print("go MM:SS     -> Jump to timestamp")
                    print("exit         -> Exit")
        except KeyboardInterrupt:
            print()
        print(BOLD + GREEN + "KAMULEC REPORTED" + END)
                

if __name__ == "__main__":
    files = sys.argv[1:]
    sos = ScienceOperatingSystem(files)
    sos.run()