from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edx_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sqlusernotificationpreferences',
            unique_together={('user_id', 'preference')},
        ),
    ]
