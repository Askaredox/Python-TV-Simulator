import pyglet

class Video:
    def __init__(self, path) -> None:
        self.path = path
        self.player = pyglet.media.Player()
        # source = pyglet.media.StreamingSource()
        MediaLoad = pyglet.media.load(path)
        self.player.queue(MediaLoad)
        self.player.play()
        self.player.loop = True

    def mute(self):
        self.player.volume = 0

    def unmute(self):
        self.player.volume = 1