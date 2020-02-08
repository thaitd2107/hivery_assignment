import json

from django.db import transaction

from paranuara.models import Company, People, Friend
from paranuara.serializers import CompanyListSerializer, PeopleImportSerializer


def import_company_data_from_file(file_path="./json/companies.json"):
    print("Importing companies from {}".format(file_path))
    with open(file_path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    if data:
        for item in data:
            serializer = CompanyListSerializer(data=item)
            # validate data
            serializer.is_valid()
            if serializer.errors:
                raise Exception(serializer.errors)
            Company.objects.get_or_create(**serializer.validated_data)
        # count company
        count = Company.objects.all().count()
        print("Number of company {}".format(count))


def import_people_data_from_file(file_path="./json/people.json"):
    print("Importing people from {}".format(file_path))
    with open(file_path, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    if data:
        # loading all people into database first
        for item in data:
            serializer = PeopleImportSerializer(data=item)
            # validate data
            serializer.is_valid()
            if serializer.errors:
                raise Exception(serializer.errors)
            # save object
            serializer.save()
        # count people
        count_people = People.objects.all().count()
        print("Number of people {}".format(count_people))
        # Then loading all friends
        chunk_size = 1000
        friend_queue = []
        for item in data:
            friend_queue.append(item)
            if chunk_size == len(friend_queue):
                save_friends(friend_queue)
                friend_queue = []
        # remain
        if len(friend_queue) > 0:
            save_friends(friend_queue)
        # count Friends
        count_friends = Friend.objects.count()
        print("Number of friends {}".format(count_friends))


@transaction.atomic
def save_friends(friends):
    # this one execute inside transaction
    for item in friends:
        people = People.objects.get(index=item['index'])
        people.add_friends(item['friends'])
