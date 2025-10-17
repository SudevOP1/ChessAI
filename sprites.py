from settings import *
import pygame as py


class ChessPiece(py.sprite.Sprite):
    def __init__(
        self,
        surf: py.Surface,
        col_ind: int,
        row_ind: int,
        *groups,
        **pos,
    ):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(**pos)
        self.col_ind = col_ind
        self.row_ind = row_ind
