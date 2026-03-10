from django.db import migrations, models
import django.utils.timezone


def set_default_dates(apps, _):
    tariff_price_model = apps.get_model('iprovider', 'TariffPrice')
    for price in tariff_price_model.objects.all():
        if not price.created_at:
            price.created_at = django.utils.timezone.now()
        if not price.updated_at:
            price.updated_at = django.utils.timezone.now()
        price.save()


class Migration(migrations.Migration):

    dependencies = [
        ('iprovider', '0011_alter_tariff_price_alter_vacancy_price_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariffprice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='tariffprice',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
        migrations.RunPython(set_default_dates, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='tariffprice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='tariffprice',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]