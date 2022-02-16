from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from base.models import Catalog, Film, Director, Producer, Cast


TESTDATA = [
    {
        'name': 'Action',
        'films': [
            {
                'title': 'Annabelle',
                'runtime': '1h30',
                'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                'poster': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg',
                'directors': [
                    {
                        'name': 'Dummy director1',
                    }
                ],
                'producers': [
                    {
                        'name': 'Dummy producer1',
                    }
                ],
                'cast': [
                    {
                        'name': 'Dummy cast1',
                    }
                ]
            },
            {
                'title': 'Ghost',
                'runtime': '1h30',
                'synopsis': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                'poster': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg',
                'directors': [
                    {
                        'name': 'Dummy director2',
                    }
                ],
                'producers': [
                    {
                        'name': 'Dummy producer2',
                    }
                ],
                'cast': [
                    {
                        'name': 'Dummy cast2',
                    }
                ]
            }
        ]
    }
]

class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cat_name = TESTDATA[0]['name']
        cls.catalog = Catalog.objects.create(name=cat_name)

        cls.film_1 = cls.catalog.films.create(
                title = cat_name[0]['title'],
                poster = cat_name[0]['poster'],
                runtime = cat_name[0]['runtime'],
                synopsis = cat_name[0]['synopsis']
            )
        cls.film_1.directors.create(name=cat_name[0]['directors']['name'])
        cls.film_1.producers.create(name=cat_name[0]['producers']['name'])
        cls.film_1.cast.create(name=cat_name[0]['cast']['name'])

        cls.film_2 = cls.catalog.films.create(
                title = cat_name[1]['title'],
                poster = cat_name[1]['poster'],
                runtime = cat_name[1]['runtime'],
                synopsis = cat_name[1]['synopsis']
            )
        cls.film_2.directors.create(name=cat_name[1]['directors'][0]['name'])
        cls.film_2.producers.create(name=cat_name[1]['producers'][0]['name'])
        cls.film_2.cast.create(name=cat_name[1]['cast'][0]['name'])


class TestFilm(BaseAPITestCase):
    
    url = reverse_lazy('films-list')

    def get_film_detail_data(self, films):
        results = []
        for film in films:
            data = {
                'id': film.pk,
                'category_id': film.category_id,
                'title': film.title,
                'poster': film.poster,
                'runtime': film.runtime,
                'synopsis' : film.synopsis,
                'directors' : [{'name': director.name} for director in film.directors],
                'producers' : [{'name': producer.name} for producer in film.producers],
                'cast' : [{'name': cast.name} for cast in film.cast]
            }
            results.append(data)
        return results
    
    def test_list(self):
        response : self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_film_detail_data([self.film_1, self.film2]), response.json)
    
    def test_list_filter(self):
        response = self.client.get(f"{self.url}?name={self.film_1}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_film_detail_data([self.film_1]), response.json())