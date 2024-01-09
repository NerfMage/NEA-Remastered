import pygame


class Creature:
    def __init__(self, name, health, speed):
        """
        A superclass for all the enemies and the player
        :param name: the creature's name
        :param health: their hit points
        :param speed: their speed in pixels
        """
        self.name = name
        self.health = health
        self.speed = speed
