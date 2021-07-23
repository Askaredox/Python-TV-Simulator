import pyglet
from video import Video
from screeninfo import get_monitors

monitor_width = 640
monitor_height = 480

m = get_monitors()
m = m[0]
monitor_width = int(m.width)
monitor_height = int(m.height)

print(monitor_height)
print(monitor_width)

title = "TV Simulator"
win = pyglet.window
window = win.Window(width=monitor_width, height=monitor_height)

player = [
    {'active':True,'video':Video('videos/Channel5.mp4')},
    {'active':False,'video':Video('videos/video.mp4')}
]


@window.event
def on_activate():
    print("hello form activate")
    for vid in player:
        if(not vid['active']):
            vid['video'].mute()


@window.event
def on_draw():
    window.clear()
    p = [x for x in player if x['active']][0]['video'].player
    p.volume = 1
    if p.source and p.source.video_format:
        p.texture.blit(0,0, width=monitor_width, height=monitor_height)


# key press event    
@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.P:
        print("Key : P is pressed")
        player.pause()
        print("Video is paused")

    if symbol == pyglet.window.key.R:
        print("Key : R is pressed")
        player.play()
        print("Video is resumed")

    if symbol == pyglet.window.key.Q:
        print("Key : Q is pressed")
        p = [x for x in player if x['active']][0]
        i = player.index(p) - 1 
        video = i % len(player)
        activate_vid(video)
        print("Video is paused")

    if symbol == pyglet.window.key.W:
        print("Key : W is pressed")
        p = [x for x in player if x['active']][0]
        i = player.index(p) + 1 
        video = i % len(player)
        print(video)
        activate_vid(video)
        print("Video is paused")

def activate_vid(i):
    for index, item in enumerate(player):
        if index == i:
            item['active']=True
            item['video'].unmute()
        else:
            item['active']=False
            item['video'].mute()

pyglet.app.run()

