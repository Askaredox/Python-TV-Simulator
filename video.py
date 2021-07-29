import cv2
import numpy as np 
import os
from time import sleep
from ffpyplayer.player import MediaPlayer
import pygame


class Time:
    def __init__(self, hour=0, minute=0, second=0, millisecond=0):
        self.hour, self.minute, self.second, self.millisecond = hour, minute, second, millisecond

    def __repr__(self):
        return self.format("<pygamevideo.Time(%h:%m:%s:%f)>")

    def __add__(self, other):
        return Time.from_millisecond(self.to_millisecond() + other.to_millisecond())

    def __sub__(self, other):
        return Time.from_millisecond(self.to_millisecond() - other.to_millisecond())

    def format(self, format_string):
        if "%H" in format_string: format_string = format_string.replace("%H", str(self.hour).zfill(2))
        if "%M" in format_string: format_string = format_string.replace("%M", str(self.minute).zfill(2))
        if "%S" in format_string: format_string = format_string.replace("%S", str(self.second).zfill(2))
        if "%F" in format_string: format_string = format_string.replace("%F", str(self.millisecond).zfill(2))
        if "%h" in format_string: format_string = format_string.replace("%h", str(int(self.hour)).zfill(2))
        if "%m" in format_string: format_string = format_string.replace("%m", str(int(self.minute)).zfill(2))
        if "%s" in format_string: format_string = format_string.replace("%s", str(int(self.second)).zfill(2))
        if "%f" in format_string: format_string = format_string.replace("%f", str(int(self.millisecond)).zfill(2))

        return format_string

    def to_hour(self):
        return self.hour + self.minute/60 + self.second/3600 + self.millisecond/3600000

    def to_minute(self):
        return self.hour*60 + self.minute + self.second/60 + self.millisecond/60000

    def to_second(self):
        return self.hour*3600 + self.minute*60 + self.second + self.millisecond/1000

    def to_millisecond(self):
        return self.hour*3600000 + self.minute*60000 + self.second*1000 + self.millisecond

    @classmethod
    def from_millisecond(cls, ms):
        h = ms//3600000
        hr = ms%3600000

        m = hr//60000
        mr = hr%60000

        s = mr//1000
        sr = mr%1000

        return cls(hour=h, minute=m, second=s, millisecond=sr)


class Video:
    def __init__(self, filepath) -> None:
        self.is_ready = False
        self.load(filepath)

    def __repr__(self):
        return f"<Video(time#{self.current_time}, source#{self.video_path})>"

    def load(self, filepath):
        filepath = str(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file or directory: '{filepath}'")

        self.filepath = filepath

        self.is_playing = False
        self.is_paused  = False
        self.is_looped  = False

        self.volume   = 1
        self.is_muted = False

        self.video = cv2.VideoCapture(filepath)
        self.player = MediaPlayer(filepath)

        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.sleep_ms = int(np.round((1/self.fps)))

        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        self.frame_width  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_surf   = pygame.Surface((self.frame_width, self.frame_height))
        self._aspect_surf = pygame.Surface((self.frame_width, self.frame_height))

        self.is_ready = True

    def release(self):
        self.video.release()
        self.player.close_player()
        self.is_ready = False

    def play(self, loop=False):
        if(not self.is_playing):
            if(not self.is_ready): self.load(self.filepath)
            self.is_playing = True
            self.is_looped = loop
            return self.fps

    def restart(self):
        if(self.is_playing):
            self.release()
            sleep(0.1)
            self.video = cv2.VideoCapture(self.filepath)
            self.player = MediaPlayer(self.filepath)
            self.is_ready = True
            self.is_playing = True
            

    def stop(self):
        if(self.is_playing):
            self.is_playing = False
            self.is_looped = False
            self.release()

    def pause(self):
        self.is_playing = False
        self.player.set_pause(True)

    def resume(self):
        self.is_playing = True
        self.player.set_pause(False)

    def mute(self):
        self.is_muted = True
        self.player.set_mute(True)

    def unmute(self):
        self.is_muted = False
        self.player.set_mute(False)

    def set_volume(self, volume):
        self.volume = volume
        self.player.set_volume(volume)

    @property
    def duration(self):
        return Time.from_millisecond((self.total_frames/self.fps)*1000)

    @property
    def current_time(self):
        return Time.from_millisecond(self.video.get(cv2.CAP_PROP_POS_MSEC))

    @property
    def remaining_time(self):
        return self.duration - self.current_time

    def seek_time(self, t):
        if isinstance(t, Time):
            _t = t.to_millisecond()
            self.seek_time(_t)

        elif isinstance(t, str):
            h = float(t[:2])
            m = float(t[3:5])
            s = float(t[6:8])
            f = float(t[9:])

            _t = Time(hour=h, minute=m, second=s, millisecond=f)
            self.seek_time(_t.to_millisecond())

        elif isinstance(t, (int, float)):
            self.video.set(cv2.CAP_PROP_POS_MSEC, t)
            self.player.seek(t/1000, relative=False)

        else:
            raise ValueError("Time can only be represented in Time, str, int or float")

    def get_size(self):
        return (self.frame_width, self.frame_height)

    def get_width(self):
        return self.frame_width

    def get_height(self):
        return self.frame_height

    def set_size(self, size):
        if not (self.frame_width > 0 and self.frame_height > 0):
            raise ValueError(f"Size must be positive")

        self.frame_width, self.frame_height, = size
        self._aspect_surf = pygame.transform.scale(self._aspect_surf, (self.frame_width, self.frame_height))

    def set_width(self, width):
        if self.frame_width <= 0:
            raise ValueError(f"Width must be positive")

        self.frame_width = width
        self._aspect_surf = pygame.transform.scale(self._aspect_surf, (self.frame_width, self.frame_height))

    def set_height(self, height):
        if self.frame_height <= 0:
            raise ValueError(f"Height must be positive")

        self.frame_height = height
        self._aspect_surf = pygame.transform.scale(self._aspect_surf, (self.frame_width, self.frame_height))

    def _scaled_frame(self):
        return pygame.transform.scale(self.frame_surf, (self.frame_width, self.frame_height))

    def get_frame(self, surface, show=True):
        if not self.is_playing:
            return self._scaled_frame()
            
        if(self.is_playing):
            success, frame=self.video.read()
            audio_frame, val = self.player.get_frame()
            sleep(self.sleep_ms)
            if(not success):
                if self.is_looped:
                    self.restart()
                    return
                else:
                    self.stop()
                    return
            else:
                if(show):
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = frame.swapaxes(0, 1)
                    size = self.get_size()
                    frame = cv2.resize(frame, size[::-1], interpolation=cv2.INTER_AREA)
                    pygame.surfarray.blit_array(surface, frame)
                    pygame.display.update()
