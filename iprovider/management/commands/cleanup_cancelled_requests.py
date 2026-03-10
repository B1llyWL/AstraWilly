from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import  timedelta
from iprovider.models import ConnectionRequest

class Command(BaseCommand):
    help = 'Удаляет отмененные заявки старше указанного количества дней (по умолчанию 30)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Количество дней, после которого заявки удаляются'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff = timezone.now() - timedelta(days=days)
        deleted_count, _ = ConnectionRequest.objects.filter(
            status = 'cancelled',
            created_at__lt = cutoff
        ).delete()
        self.stdout.write(
            self.style.SUCCESS(f'Удалено {deleted_count} отмененных заявок, созданных до {cutoff.date()}')
        )