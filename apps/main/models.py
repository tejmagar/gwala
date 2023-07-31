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


class Status(models.TextChoices):
    NONE = 'none'  # User filled half form but not completed yet
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class TradeType(models.TextChoices):
    BUY = 'buy'
    SELL = 'sell'


class MilkTrade(models.Model):
    # Primary fields
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    contact_number = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    local_body = models.CharField(max_length=100)
    ward = models.IntegerField()
    google_map_location = models.URLField(null=True, blank=True)
    house_photo = models.ImageField(upload_to='uploads/')

    # Additional fields
    milk_source = models.ForeignKey(to=Animal, on_delete=models.DO_NOTHING, null=True, blank=True)
    litre_to_sell = models.IntegerField(null=True, blank=True)
    rate_per_litre = models.IntegerField(help_text='In rupees', null=True, blank=True)

    # Status
    trade_type = models.CharField(max_length=20, choices=TradeType.choices)
    status = models.CharField(max_length=60, choices=Status.choices, default=Status.NONE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
