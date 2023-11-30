from django.core.management.base import BaseCommand, CommandError
import app.pm_doc_manager.notify_monthly_pm as task
import app.utility as util

class Command(BaseCommand):
    help = 'Run Incomplete PM'
    def handle(self, *args, **options):
        try:
           result= task.notify_imcomplete_pm_to_team()
           print(result)
        except Exception as ex:
            # util.add_error_to_file(str(ex))
            print(str(ex))

