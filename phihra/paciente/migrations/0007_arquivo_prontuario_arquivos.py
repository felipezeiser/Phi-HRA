# Generated by Django 5.0.2 on 2024-02-21 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0006_solicitacaoexame'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='prontuarios/')),
            ],
        ),
        migrations.AddField(
            model_name='prontuario',
            name='arquivos',
            field=models.ManyToManyField(to='paciente.arquivo'),
        ),
    ]
