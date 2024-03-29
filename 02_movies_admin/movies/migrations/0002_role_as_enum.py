# Generated by Django 3.2.14 on 2022-07-30 12:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                    CREATE TYPE "content"."role_type" AS ENUM ('actor', 'producer', 'director');
                    ALTER TABLE "content"."person_film_work"
                        ALTER COLUMN "role" TYPE "content"."role_type" using "role"::"role_type";
                """,
            reverse_sql="""
                    ALTER TABLE "content"."person_film_work"
                        ALTER COLUMN "role" TYPE TEXT;
                    DROP TYPE "content"."role_type";
                """,
        )

    ]
