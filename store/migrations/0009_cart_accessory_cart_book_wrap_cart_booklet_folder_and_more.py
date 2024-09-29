# Generated by Django 5.1.1 on 2024-09-29 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_accessory_ebook_schooloffice_bookwrap_exlibris_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='accessory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.accessory'),
        ),
        migrations.AddField(
            model_name='cart',
            name='book_wrap',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.bookwrap'),
        ),
        migrations.AddField(
            model_name='cart',
            name='booklet_folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.bookletfolder'),
        ),
        migrations.AddField(
            model_name='cart',
            name='ebook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.ebook'),
        ),
        migrations.AddField(
            model_name='cart',
            name='exlibris',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.exlibris'),
        ),
        migrations.AddField(
            model_name='cart',
            name='other',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.other'),
        ),
        migrations.AddField(
            model_name='cart',
            name='pencil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.pencil'),
        ),
        migrations.AddField(
            model_name='cart',
            name='school_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.schooloffice'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.book'),
        ),
    ]
