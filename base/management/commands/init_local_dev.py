from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from base.models import Catalog, Director, Producer, Cast

UserModel = get_user_model()

CATALOGS = [
    {
        'name': 'Catalog 1',
        'films': [
            {
                'title': 'Film 1',
                'runtime': '1h30',
                'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                'poster': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg',
                'directors': [
                    {
                        'name': 'director1',
                    },
                    {
                        'name': 'director2'
                    }
                ],
                'producers': [
                    {
                        'name': 'producer1',
                    },
                    {
                        'name': 'producer2'
                    }
                ],
                'cast': [
                    {
                        'name': 'cast1',
                    },
                    {
                        'name': 'cast2'
                    }
                ]
            },
            {
                'title': 'Film 2',
                'runtime': '1h30',
                'synopsis': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                'poster': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg',
                'directors': [
                    {
                        'name': 'director3',
                    },
                    {
                        'name': 'director2'
                    }
                ],
                'producers': [
                    {
                        'name': 'producer1',
                    },
                    {
                        'name': 'producer4'
                    }
                ],
                'cast': [
                    {
                        'name': 'cast3',
                    },
                    {
                        'name': 'cast4'
                    },
                ]
            },
            {
                'title': 'Terminator',
                'runtime': '1h30',
                'synopsis': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                'poster': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX101_CR0,0,101,150_.jpg',
                'directors': [
                    {
                        'name': 'director3',
                    },
                    {
                        'name': 'director2'
                    }
                ],
                'producers': [
                    {
                        'name': 'producer5',
                    },
                    {
                        'name': 'producer3'
                    }
                ],
                'cast': [
                    {
                        'name': 'cast5',
                    },
                    {
                        'name': 'cast6'
                    }
                ]
            }
        ]
    }
]

ADMIN_ID = 'admin-oc'
ADMIN_PASSWORD = 'password-oc'


class Command(BaseCommand):

    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        Catalog.objects.all().delete()

        for data_catalog in CATALOGS:
            catalog = Catalog.objects.create(name=data_catalog['name'])
            for data_film in data_catalog['films']:
                film = catalog.films.create(
                    title = data_film['title'],
                    poster = data_film['poster'],
                    runtime = data_film['runtime'],
                    synopsis = data_film['synopsis']
                )
                for data_director in data_film['directors']:
                    director, created = Director.objects.get_or_create(name=data_director['name'])
                    film.directors.add(director)
                    print(f"name={data_director['name']} - created={created}")
                for data_producer in data_film['producers']:
                    producer, created = Producer.objects.get_or_create(name=data_producer['name'])
                    film.producers.add(producer)
                    print(f"name={data_producer['name']} - created={created}")
                for data_cast in data_film['cast']:
                    cast, created = Cast.objects.get_or_create(name=data_cast['name'])
                    film.cast.add(cast)
                    print(f"name={data_cast['name']} - created={created}")

        UserModel.objects.create_superuser(ADMIN_ID, 'admin@oc.drf', ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS("All Done !"))