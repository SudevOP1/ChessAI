from settings import *
import pygame as py


class ChessPiece(py.sprite.Sprite):
    def __init__(self, surf: py.Surface, *groups, **pos):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(**pos)
