import pygame as py

from code.simul.settings import *


class ChessPiece(py.sprite.Sprite):
    def __init__(
        self,
        surf: py.Surface,
        col_i: int,
        row_i: int,
        name: str,
        *groups,
        **pos,
    ):
        super().__init__(*groups)
        self.surf = surf
        self.rect = self.surf.get_rect(**pos)
        self.col_i = col_i
        self.row_i = row_i
        self.name = name

    def draw(self, window: py.Surface):
        window.blit(self.surf, self.rect)
