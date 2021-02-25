from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

MARKET_CHOICES = [
    ('aFRR', 'aFRR'),
    ('mFRR', 'mFRR')
]
DIRECTION_CHOICES = [
    ('U', 'up'),
    ('D', 'down')
]

class Tender(models.Model):
    date = models.DateField()
    market = models.CharField(max_length=4, choices=MARKET_CHOICES, default='aFRR')
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default='D')
    tender_round = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])

    def __str__(self):
        return 'Tender %s %s-%s-%d' % (str(self.date), self.market, self.direction, self.tender_round, )

    class Meta:
        ordering = ['-date']

class Unit(models.Model):
    fromdate = models.DateField()
    todate = models.DateField()
    tender = models.ForeignKey(Tender, models.CASCADE, 'units')

    def __str__(self):
        return "Unit-%d %s-%s" % (self.tender.id, str(self.fromdate), str(self.todate))

class Bid(models.Model):
    bid_round = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    price = models.IntegerField()
    amount = models.IntegerField()
    ours = models.BooleanField(default=False)
    unit = models.ForeignKey(Unit, models.CASCADE, 'bids')

    def __str__(self):
        return "Bid-%d %d %d" % (self.bid_round, self.price, self.amount)