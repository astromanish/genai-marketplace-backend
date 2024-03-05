# Generated by Django 3.2.12 on 2024-03-05 17:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gpts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitysummary',
            name='generatedDate',
        ),
        migrations.RemoveField(
            model_name='activitysummary',
            name='modelStats',
        ),
        migrations.RemoveField(
            model_name='activitysummary',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='activitysummary',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='gpt',
            name='activitySummary',
        ),
        migrations.RemoveField(
            model_name='gpt',
            name='categories',
        ),
        migrations.AddField(
            model_name='gpt',
            name='generatedDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gpt',
            name='tags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gpts.tags'),
        ),
        migrations.AlterField(
            model_name='activitysummary',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='gpt',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='owner',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tags',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
