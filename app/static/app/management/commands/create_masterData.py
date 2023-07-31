
from . import data_import1
from . import data_import2
# import app.management.commands.data_import as dx
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The excel file that contains the any master data.')

    def handle(self, *args, **kwargs):
        filename = kwargs['file_name']

        #data_import1.importCompanyMaster(filename)
        data_import2.importInventoryMaster(filename)

        #self.stdout.write(self.style.SUCCESS('Data imported successfully'))






