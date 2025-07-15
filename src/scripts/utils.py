import os

import pygame

BASE_PATH = '../assets/images/'

def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((110, 205, 30))
    return img

def load_images(path):
    images = []
    
    for img in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + '/' + img))
    
    return images