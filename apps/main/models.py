from django.db import models


# Create your models here.


class District(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class LocalBody(models.Model):
    name = models.CharField(max_length=60)
    district = models.ForeignKey(to=District, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Local bodies'

    def __str__(self):
        return f'{self.district.name} ==> {self.name}'


class Ward(models.Model):
    local_body = models.ForeignKey(to=LocalBody, on_delete=models.DO_NOTHING)
    number = models.IntegerField()

    def __str__(self):
        return f'{self.local_body.district.name} ==> {self.local_body.name} ==> {self.number}'


class Animal(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class AnimalType(models.Model):
    name = models.CharField(max_length=100)
    animal = models.ForeignKey(to=Animal, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.animal} - {self.name}'


class Status(models.TextChoices):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class Producer(models.Model):
    name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=10)
    ward = models.ForeignKey(to=Ward, on_delete=models.DO_NOTHING)
    house_photo = models.ImageField(upload_to='uploads/', null=True, blank=True)
    milk_source = models.ForeignKey(to=AnimalType, on_delete=models.DO_NOTHING)
    litre_to_sell = models.IntegerField()
    rate_per_litre = models.IntegerField(help_text='In rupees')
    status = models.CharField(max_length=60, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.name
