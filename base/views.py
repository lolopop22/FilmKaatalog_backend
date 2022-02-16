from django.shortcuts import render
import imdb
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CatalogSerializer, FilmSerializer
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from base.models import Catalog, Film
from imdb import Cinemagoer, IMDbError


class FilmAPIView(APIView, PageNumberPagination):  # LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        
        title = self.request.GET.get('title')

        print("---------------------")
        print(f"Searching for the film with title: {title}")

        if title:
            # Fetch the movie(s) with the given name from IMDb
            films = []
            try:
                movie_db = imdb.Cinemagoer()
                movies = movie_db.search_movie(title)
                movie_ids = [movie.movieID for movie in movies if title.lower() in movie['title'].lower()]

                for movie_id in movie_ids:
                    movie = movie_db.get_movie(movie_id)
                    title = movie.get('title')
                    poster = movie.get('full-size cover url')
                    synopsis = movie.get('plot outline')
                    
                    if isinstance(movie.get('runtimes'), list):
                        runtime = "{:02d}h{:02d}min".format(*divmod(int(movie.get('runtimes')[0]), 60)) # conversion des minutes en heure
                    else:
                        runtime = "Pas de durée renseignée"
                    
                    if isinstance(movie.get('director'), list):
                        directors = [director.get('name') for director in movie.get('director')]
                    else:
                        directors = []

                    if isinstance(movie.get('producer'), list):
                        producers = [producer.get('name') for producer in movie.get('producer')][:5]
                    else:
                        producers = []

                    if isinstance(movie.get('cast'), list):
                        cast = [actor.get('name') for actor in movie.get('cast')][:5]
                    else:
                        cast = []
                    
                    movie_info = {
                        'title': title,
                        'poster': poster,
                        'runtime': runtime,
                        'directors': directors,
                        'producers': producers,
                        'cast': cast,
                        'synopsis': synopsis,
                    }
                    
                    films.append(movie_info)
            except IMDbError as e:
                print(e)

            results = {
                "response": {
                    "count": len(films), 
                    "results": films
                }
            }

            return Response(results, status=status.HTTP_200_OK)
        else:
            films = Film.objects.all()
            query_set = self.paginate_queryset(films, request, view=self)
            serializer = FilmSerializer(query_set, many=True)
            return self.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        serializer = FilmSerializer(data = request.data)
        print("--------------------------------------------")
        print(f"request data: {request.data}")
        print(f"serializer: {serializer}")
        print("--------------------------------------------")
        if serializer.is_valid():
            print("serializer is valid!")
            serializer.save()
            print(f"serializer data: {serializer.data}")
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        print('serializer is not valid.')
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
