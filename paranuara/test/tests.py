from django.test import TestCase
from paranuara import util
from paranuara.models import Company, People
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.


class TestImportData(TestCase):
    def test_import_six_companies(self):
        # Calling import data
        util.import_company_data_from_file(file_path="./paranuara/test/resources/companies.json")
        # filter companies
        company_count = Company.objects.filter(index__in=('0', '1', '2', '3', '4', '5')).count()
        self.assertEqual(company_count, 6)

    def test_import_people(self):
        # Calling import company
        util.import_company_data_from_file(file_path="./paranuara/test/resources/companies.json")
        util.import_people_data_from_file(file_path="./paranuara/test/resources/people.json")
        people_count = People.objects.filter(index__in=('0', '1', '2')).count()
        self.assertEqual(people_count, 3)
        people = People.objects.get(index=0)
        # evaluate people detail
        self.assertEqual(people.name, "Carmella Lambert")


class APITestCase(TestCase):
    def setUp(self):
        # Calling import data
        util.import_company_data_from_file(file_path="./paranuara/test/resources/companies.json")
        util.import_people_data_from_file(file_path="./paranuara/test/resources/people.json")
        self.client = APIClient()

    def test_api_two_people(self):
        response = self.client.get('/peoples/friends_in_common/', {'ids': '1,2'}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Carmella Lambert")

    def test_api_company_get_list_employees(self):
        response = self.client.get('/companies/0', format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Carmella Lambert")

    def test_api_can_get_fruits_and_vegetables(self):
        response = self.client.get('/peoples/0', format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Carmella Lambert")
