import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from iprovider.models import CurrencyRate

class Command(BaseCommand):
    help = 'Обновление курсов валют из внешнего API (Frankfurter.app)'

    def handle(self, *args, **options):
        # Используем Frankfurter.app (бесплатно, без ключа)
        url = 'https://api.frankfurter.app/latest?from=USD'

        self.stdout.write("Запрашиваю курсы валют...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Frankfurter возвращает курсы относительно базовой валюты
            rates = data.get('rates', {})
            # Добавляем USD как базовую валюту с курсом 1.0
            rates['USD'] = 1.0

            updated_count = 0
            created_count = 0
            for currency_code, rate in rates.items():
                # Используем update_or_create для обновления или создания записи
                obj, created = CurrencyRate.objects.update_or_create(
                    currency=currency_code,
                    defaults={'rate_to_usd': Decimal(str(rate))}
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно: создано {created_count}, обновлено {updated_count} курсов валют.'
                )
            )

        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка сети при запросе к API: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Неожиданная ошибка: {e}')
            )