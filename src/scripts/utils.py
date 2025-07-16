import os

import pygame

BASE_PATH = '../assets/images/'

def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    if 'player' in path:
        img.set_colorkey((0, 0, 0))
    else:
        img.set_colorkey((110, 205, 30))
    return img

def load_images(path):
    images = []
    
    for img in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + '/' + img))
    
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.imageDuration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.imageDuration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.imageDuration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.imageDuration * len(self.images) - 1)
            if self.frame >= self.imageDuration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.imageDuration)]