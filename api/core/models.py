from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

MARKET_CHOICES = [
    ('aFRR', 'aFRR'),
    ('mFRR', 'mFRR')
]
DIRECTION_CHOICES = [
    ('U', 'up'),
    ('D', 'down')
]

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'bids_{0}_{1}_{2}_{3}.xlsx'.format(instance.datestr, instance.market, instance.direction, instance.tender_round)

class Tender(models.Model):
    datestr = models.CharField(max_length=7)
    market = models.CharField(max_length=4, choices=MARKET_CHOICES, default='aFRR')
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, default='D')
    tender_round = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])
    current_bid_round = models.IntegerField(default=0)
    bid_file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return 'Tender %s %s-%s-%d' % (self.datestr, self.market, self.direction, self.tender_round)

    class Meta:
        ordering = ['-datestr']

class Unit(models.Model):
    fromdate = models.DateField()
    todate = models.DateField()
    tender = models.ForeignKey(Tender, models.CASCADE, 'units')

    def __str__(self):
        return "Unit-%d %s-%s" % (self.tender.id, str(self.fromdate), str(self.todate))

class BidRound(models.Model):
    number = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    max_price_wkdy = models.IntegerField()
    max_price_wknd = models.IntegerField()
    min_drop_wkdy = models.IntegerField()
    min_drop_wknd = models.IntegerField()
    tender = models.ForeignKey(Tender, models.CASCADE, 'bid_rounds')

    def __str__(self):
        return "Round %d of Tender %s %s-%s-%d" % (
            self.number, self.tender.datestr, self.tender.market, self.tender.direction, self.tender.tender_round
        )

class Bid(models.Model):
    price = models.IntegerField()
    amount = models.IntegerField()
    ours = models.BooleanField(default=False)
    bid_round = models.ForeignKey(BidRound, models.CASCADE, 'bids')
    unit = models.ForeignKey(Unit, models.CASCADE, 'bids')

    def __str__(self):
        return "Bid-%d %d" % (self.price, self.amount)


class OurBid(models.Model):
    o_price = models.IntegerField()
    o_amount = models.IntegerField()
    o_bid_round = models.ForeignKey(BidRound, models.CASCADE, 'our_bids')
    o_unit = models.ForeignKey(Unit, models.CASCADE, 'our_bids')

    def __str__(self):
        return "OurBid %d %d" % (self.o_price, self.o_amount)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)