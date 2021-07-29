import pygame
from os import listdir
from os.path import isfile, join
from video import Video
from screeninfo import get_monitors

m = get_monitors()
m = m[0]
monitor_width = int(m.width)
monitor_height = int(m.height)
pygame.init()
window = pygame.display.set_mode([monitor_width, monitor_height])

clock = pygame.time.Clock()
# start video

player = []

def get_videos(path):
    onlyfiles = [path+'/'+f for f in listdir(path) if isfile(join(path, f))]
    global player
    active = True
    for f in onlyfiles:
        video = Video(f)
        video.set_size((monitor_width, monitor_height))
        if(not active): video.mute()
        vid = {'active': active, 'video': video, 'fps': video.play(loop=True)}
        active = False
        player.append(vid)

def activate_vid(i):
    for index, item in enumerate(player):
        if index == i:
            item['active'] = True
            item['video'].unmute()
        else:
            item['active'] = False
            item['video'].mute()
    
def main():

    print(monitor_height)
    print(monitor_width)

    get_videos('videos')
    # main loop
    try:
        while True:
            video = None
            for v in player:
                show=False
                v['video'].mute()
                if(v['active']):
                    show = True
                    v['video'].unmute()
                    video = v
                v['video'].get_frame(window, False)

            # set window title to current duration of video as hour:minute:second
            t = video['video'].current_time.format("%h:%m:%s")
            pygame.display.set_caption(t)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        print('0 pressed')
                    if event.key == pygame.K_1:
                        activate_vid(0)
                    if event.key == pygame.K_2:
                        activate_vid(1)
                    if event.key == pygame.K_3:
                        activate_vid(2)
                    if event.key == pygame.K_4:
                        activate_vid(3)
                    if event.key == pygame.K_5:
                        activate_vid(4)
                    if event.key == pygame.K_6:
                        activate_vid(5)
                    if event.key == pygame.K_7:
                        activate_vid(6)
                    if event.key == pygame.K_8:
                        activate_vid(7)
                    if event.key == pygame.K_9:
                        activate_vid(8)

            pygame.display.update()
            clock.tick(video['fps'])

    except (KeyboardInterrupt, SystemExit):
        pygame.quit()
        quit()


if __name__ == '__main__':
    main()