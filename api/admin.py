from django.contrib import admin
from . import models

admin.site.register(models.Bid)
admin.site.register(models.BidRound)
admin.site.register(models.Unit)
admin.site.register(models.Tender)