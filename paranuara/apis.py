from rest_framework.decorators import api_view
from paranuara.models import Company, People, Friend
from paranuara import serializers
from rest_framework.response import Response
from rest_framework import status


def success_response(data):
    return {"status": "Success", "data": data}


def fail_response(error):
    return {"status": "Fail", "error": error}


@api_view(['GET'])
def company_list(request):
    """
    List all companies, or create a new company.
    """
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = serializers.CompanyListSerializer(companies, many=True)
        return Response(success_response(serializer.data))


@api_view(['GET'])
def company_detail(request, pk):
    """
    Return Company detail with all their employees
    :param request:
    :return:
    """
    try:
        company = Company.objects.get(pk=pk)

    except Company.DoesNotExist:
        content = fail_response("Company does not exist!")
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = serializers.CompanyDetailSerializer(company)
        return Response(success_response(serializer.data), status=status.HTTP_200_OK)


def get_friends_in_common(ids, eye_color, has_died):
    list_ids = ids.split(",")
    # For this requirement only accept 2 people
    if len(list_ids) < 2:
        content = fail_response("Only accept 2 people!")
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    friend_list_people_1 = Friend.objects.filter(people_index__index=list_ids[0]).values_list("friend_index__index",
                                                                                              flat=True)
    friend_list_people_2 = Friend.objects.filter(people_index__index=list_ids[1]).values_list("friend_index__index",
                                                                                              flat=True)

    common_friend_ids = set(friend_list_people_1).intersection(set(friend_list_people_2))
    friends = People.objects.filter(index__in=common_friend_ids, eye_color=eye_color, has_died=has_died)
    response_common_friends = serializers.FriendSerializer(data=friends, many=True)
    response_common_friends.is_valid()

    peoples = People.objects.filter(index__in=list_ids[0:2]).all()
    response_peoples = serializers.PeopleSerializerSimple(data=peoples, many=True)
    response_peoples.is_valid()

    content = success_response({"peoples": response_peoples.data,
                                "common_friends": response_common_friends.data})
    return content


@api_view(['GET'])
def people_friends_in_common(request):
    """

    :param request:
    :return:
    """
    ids = request.query_params.get('ids', "")
    eye_color = request.query_params.get('eye_color', "brown")
    has_died = request.query_params.get('has_died', False)
    if request.method == 'GET':
        try:
            content = get_friends_in_common(ids, eye_color, has_died)
        except Exception:
            content = fail_response("Bad request!")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
def people_detail(request, pk):
    """
    Return People detail and provide a list of fruits and vegetables they like
    :param request:
    :return:
    """
    try:
        people = People.objects.get(pk=pk)
    except People.DoesNotExist:
        content = fail_response("People not found!")
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = serializers.PeopleSerializerDetail(people)
        return Response(success_response(serializer.data), status=status.HTTP_200_OK)
