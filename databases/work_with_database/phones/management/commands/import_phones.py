from csv import DictReader
from datetime import datetime
from distutils.util import strtobool
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as csvfile:
            phone_reader = DictReader(csvfile, delimiter=';')
            for row in phone_reader:
                phone = Phone.objects.create(
                    name=row['name'],
                    price=int(row['price']),
                    image=row['image'],
                    release_date=datetime.strptime(
                        row['release_date'], '%Y-%m-%d'),
                    lte_exists=bool(strtobool(row['lte_exists']))
                    )
                phone.save()
