import pygame as py

from settings import *


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
        self.image = surf
        self.rect = self.image.get_rect(**pos)
        self.col_i = col_i
        self.row_i = row_i
        self.name = name
