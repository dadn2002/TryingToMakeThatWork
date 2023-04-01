import math

import pygame


def PathingDirection(x1, y1, x2, y2):
    # print(x1, y1, x2, y2)
    return [x2 - x1, y2 - y1]


def collided(sprite, other):
    """Check if the hitboxes of the two sprites collide."""
    return sprite.hitbox.colliderect(other.hitbox)



