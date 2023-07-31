from django.core.management.base import BaseCommand, CommandError
from app.pm_doc_manager.pm_doc_builder import process_pm_doc_task
import app.utility as util

class Command(BaseCommand):
    help = 'Create PM PDF Doc as Zip file and Send mail to requestor'
    def handle(self, *args, **options):
        try:
           result= process_pm_doc_task()
        except Exception as ex:
            # util.add_error_to_file(str(ex))
            print(str(ex))

