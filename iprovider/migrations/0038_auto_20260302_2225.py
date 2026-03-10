from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('iprovider', '0037_alter_connectionrequest_contact_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrequest',
            name='contact_method',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]