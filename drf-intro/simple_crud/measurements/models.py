from django.db import models


# Параметр abstract = True указывает, что этот класс не создаёт новую
# таблицу в БД, а добавляет указанные в нём поля в таблицы для классов,
# унаследованных от этого класса. Если не указать этот параметр, то
# поля по-прежнему будут добавляться в унаследованные классы, но
# при этом для самого класса будет создаваться новая таблица в БД.


class TimestampFields(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Project(TimestampFields):
    """Объект на котором проводят измерения."""

    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Measurement(TimestampFields):
    """Измерение температуры на объекте."""

    value = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
