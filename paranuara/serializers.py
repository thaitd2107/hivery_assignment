from rest_framework import serializers
from paranuara.models import Company, People
from decimal import Decimal
from django.utils.dateparse import parse_datetime


def get_fruit_list():
    return ['apple', 'apricot', 'banana', 'bilberry', 'blackberry', 'blackcurrant',
            'blueberry', 'coconut', 'currant', 'cherry', 'cherimoya', 'clementine',
            'cloudberry', 'date', 'damson', 'durian', 'elderberry', 'fig', 'feijoa',
            'gooseberry', 'grape', 'grapefruit', 'huckleberry', 'jackfruit', 'jambul',
            'jujube', 'kiwifruit', 'kumquat', 'lemon', 'lime', 'loquat', 'lychee', 'mango',
            'melon', 'cantaloupe', 'honeydew', 'watermelon', 'rock', 'melon', 'nectarine',
            'orange', 'passionfruit', 'peach', 'pear', 'plum', 'plumcot', 'prune',
            'pineapple', 'pomegranate', 'pomelo', 'purple', 'mangosteen', 'raisin',
            'raspberry', 'rambutan', 'redcurrant', 'satsuma', 'strawberry', 'tangerine',
            'tomato', 'ugli', 'fruit']


def get_vegetable_list():
    return ['artichoke', 'asparagus', 'aubergine', 'beet', 'beetroot', 'bell pepper',
            'broccoli', 'brussels sprout', 'cabbage', 'carrot', 'cauliflower', 'celery',
            'corn', 'courgette', 'cucumber', 'eggplant', 'green bean', 'green onion',
            'leek', 'lettuce', 'mushroom', 'onion', 'pea', 'pepper', 'potato', 'pumpkin',
            'radish', 'spring onion', 'squash', 'sweet potato', 'tomato', 'zucchini']


def parse_register_date(register_str):
    return parse_datetime(register_str.replace(" ", ""))


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ["_id", "index", "guid", "has_died", "balance", "picture", "age", "eye_color", "name", "gender",
                  "company_id", "email", "phone", "address", "about", "registered", ]


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["index", "company"]


class CompanyDetailSerializer(serializers.ModelSerializer):
    employees = PeopleSerializer(many=True)

    class Meta:
        model = Company
        fields = ["index", "company", "employees"]


class PeopleSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ["index", "name", "age", "address", "phone"]


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ["index", "name", "eye_color", "has_died"]


class PeopleSerializerDetail(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    fruits = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()

    def get_username(self, people):
        return people.name

    def get_fruits(self, people):
        return people.get_fruits()

    def get_vegetables(self, people):
        return people.get_vegetables()

    class Meta:
        model = People
        fields = ["username", "age", "fruits", "vegetables"]


class PeopleImportSerializer(serializers.Serializer):
    _id = serializers.CharField()
    index = serializers.IntegerField()
    guid = serializers.CharField()
    has_died = serializers.BooleanField()
    balance = serializers.CharField()
    picture = serializers.CharField()
    age = serializers.IntegerField()
    eyeColor = serializers.CharField()
    name = serializers.CharField()
    gender = serializers.CharField()
    company_id = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    about = serializers.CharField()
    registered = serializers.CharField()
    tags = serializers.ListSerializer(child=serializers.CharField())
    greeting = serializers.CharField()
    favouriteFood = serializers.ListSerializer(child=serializers.CharField())

    def create_or_update(self, people, validated_data):
        people._id = validated_data['_id']
        people.guid = validated_data['guid']
        people.index = validated_data['index']
        people.name = validated_data['name']
        people.age = validated_data['age']
        people.has_died = False if validated_data['has_died'] == "false" or not validated_data['has_died'] else True
        people.balance = Decimal(validated_data['balance'].strip('$').replace(',', ''))
        people.picture = validated_data['picture']
        people.eye_color = validated_data['eyeColor']
        people.gender = validated_data['gender']
        people.company = Company.objects.filter(index=validated_data['company_id']).first()
        people.email = validated_data['email']
        people.phone = validated_data['phone']
        people.address = validated_data['address']
        people.about = validated_data['about']
        people.greeting = validated_data['greeting']
        try:
            people.registered = parse_register_date(validated_data['registered'])
        except Exception as e:
            pass
        people.add_tags(validated_data['tags'])
        people.add_favourite_food(validated_data['favouriteFood'])

        fruit_list = get_fruit_list()
        vegetable_list = get_vegetable_list()

        for food in validated_data['favouriteFood']:
            if food in fruit_list:
                if people.fruits:
                    people.fruits = "{},{}".format(people.fruits, food)
                else:
                    people.fruits = food

            if food in vegetable_list:
                if people.vegetables:
                    people.vegetables = "{},{}".format(people.vegetables, food)
                else:
                    people.vegetables = food
        return people

    def create(self, validated_data):
        people = People()
        people = self.create_or_update(people, validated_data)
        people.save()
        return people

    def update(self, instance, validated_data):
        people = self.create_or_update(instance, validated_data)
        people.save()
