import os
from django.core.management.base import BaseCommand
from paranuara.util import import_company_data_from_file, import_people_data_from_file


class Command(BaseCommand):
    help = 'Import company/people data from resources file'

    def add_arguments(self, parser):
        parser.add_argument('--path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options.get('path', None)
        if path:
            companies_path = os.path.join(path[0], 'companies.json')
            people_path = os.path.join(path[0], 'people.json')
            import_company_data_from_file(companies_path)
            import_people_data_from_file(people_path)
        else:
            import_company_data_from_file()
            import_people_data_from_file()
        self.stdout.write(self.style.SUCCESS('Successfully import data'))
