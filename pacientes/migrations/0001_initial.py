# Generated by Django 3.1.3 on 2021-06-12 23:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hora',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('hora_cit', models.TextField(max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('motivo_consulta', models.CharField(max_length=100, verbose_name='Motivo')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Observación')),
            ],
            options={
                'verbose_name': 'Observación',
                'verbose_name_plural': 'Observaciones',
                'db_table': 'observacion',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=25, verbose_name='Apellido')),
                ('edad', models.PositiveIntegerField(verbose_name='Edad')),
                ('dni', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='Documento')),
                ('telefono', models.TextField(blank=True, null=True, verbose_name='Teléfono')),
                ('addres', models.CharField(max_length=66, verbose_name='Direcciòn')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='pacientes/img/', verbose_name='Imagen del paciente')),
                ('record', models.ImageField(blank=True, null=True, upload_to='record/img/', verbose_name='Documento')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'db_table': 'paciente',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('asistencia', models.CharField(blank=True, choices=[('P', 'Pendiente'), ('A', 'Asistió'), ('F', 'Faltó')], max_length=1, null=True, verbose_name='Asistencia')),
                ('fecha', models.DateField(verbose_name='Día')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turnos', to='pacientes.paciente', verbose_name='Paciente')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.hora', verbose_name='HORA DE LA CITA')),
            ],
            options={
                'verbose_name': 'Turno',
                'verbose_name_plural': 'Turnos',
                'db_table': 'turno',
            },
        ),
    ]
