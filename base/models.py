from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name 


class Director(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name 


class Producer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Cast(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=255)
    runtime = models.CharField(max_length=10)
    synopsis = models.TextField(blank=True)
    poster = models.TextField(blank=True)

    catalog = models.ForeignKey('base.Catalog', on_delete=models.CASCADE, related_name='films')
    
    directors = models.ManyToManyField('base.Director', blank=True, related_name='directors')
    producers = models.ManyToManyField('base.Producer', blank=True, related_name='producers')
    cast = models.ManyToManyField('base.Cast', blank=True, related_name='cast')

    def __str__(self) -> str:
        return self.title    
