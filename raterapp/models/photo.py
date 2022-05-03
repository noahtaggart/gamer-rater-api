from distutils.command.upload import upload
from tkinter import PhotoImage
from unittest.util import _MAX_LENGTH
from django.db import models

class Photo(models.Model):
    photo = models.ImageField(upload_to='images/')
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)