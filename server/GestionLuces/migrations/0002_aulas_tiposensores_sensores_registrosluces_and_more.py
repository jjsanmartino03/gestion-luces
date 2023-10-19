# Generated by Django 4.2.6 on 2023-10-19 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionLuces', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aulas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoSensores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Sensores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_signal_late', models.IntegerField()),
                ('ip_aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionLuces.aulas')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionLuces.tiposensores')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrosLuces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.DateTimeField()),
                ('hasta', models.DateTimeField()),
                ('estado', models.BooleanField()),
                ('id_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionLuces.sensores')),
            ],
        ),
        migrations.CreateModel(
            name='Interacciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('encendido', 'encendido'), ('apagado', 'apagado')], max_length=10)),
                ('fecha', models.DateTimeField()),
                ('id_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionLuces.sensores')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionLuces.usuarios')),
            ],
        ),
    ]
