from django.core.management.base import BaseCommand, CommandError
from app.pm_doc_manager.pm_doc_builder import delete_pm_doc_task

class Command(BaseCommand):
    help = 'Delete PM PDF Doc'
    def handle(self, *args, **options):
        try:
           result= delete_pm_doc_task()
        except Exception as ex:
            # util.add_error_to_file(str(ex))
            print(str(ex))

