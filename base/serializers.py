from rest_framework.serializers import ModelSerializer, RelatedField
from base.models import Catalog, Film, Director, Producer, Cast


class DirectorSerializer(ModelSerializer):

    class Meta:
        model = Director
        fields = ['name']
    

    def to_representation(self, value):
         return value.name


class ProducerSerializer(ModelSerializer):

    class Meta:
        model = Producer
        fields = ['name']


    def to_representation(self, value):
         return value.name


class CastSerializer(ModelSerializer):

    class Meta:
        model = Cast
        fields = ['name']
    

    def to_representation(self, value):
         return value.name


class FilmSerializer(ModelSerializer):
    directors =  DirectorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    cast = CastSerializer(many=True)

    class Meta:
        model = Film
        fields = ['id', 'catalog_id', 'title', 'runtime', 'synopsis', 'poster', 'directors', 'producers', 'cast', 'catalog']
        # fields = "__all__"
    
    def create(self, validated_data):
        print(f"validated data before pop: {validated_data}")
        directors = validated_data.pop('directors', [])
        producers = validated_data.pop('producers', [])
        cast = validated_data.pop('cast', [])
        catalog_id = validated_data.pop('catalog').pk
        validated_data['catalog_id'] = catalog_id
        film, created = Film.objects.get_or_create(**validated_data)

        if not created:
            for data_director in directors:
                director, created = Director.objects.get_or_create(name=data_director['name'])
                print("hello director")
                film.directors.add(director)
                print(f"name={data_director['name']} - created={created}")
            for data_producer in producers:
                producer, created = Producer.objects.get_or_create(name=data_producer['name'])
                print("hello producer 1")
                film.producers.add(producer)
                print("hello producer 2")
                print(f"name={data_producer['name']} - created={created}")
            for data_cast in cast:
                cast, created = Cast.objects.get_or_create(name=data_cast['name'])
                film.cast.add(cast)
                print(f"name={data_cast['name']} - created={created}")

        return film



class CatalogSerializer(ModelSerializer):

    films = FilmSerializer(many=True)

    class Meta:
        model = Catalog
        fields = ['name', 'films']
