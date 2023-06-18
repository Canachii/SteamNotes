from django.db import models


# Create your models here.
class App(models.Model):
    class Meta:
        db_table = "app"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
    capsule_image = models.TextField(default="{% static 'default_header.jpg' %}")
    header_image = models.TextField(default="{% static 'default_header.jpg' %}")
    is_free = models.BooleanField(null=True)
    initial_price = models.IntegerField(null=True)
    discount_percent = models.IntegerField(null=True)
    final_price = models.IntegerField(null=True)


class Rank(models.Model):
    class Meta:
        db_table = "rank"

    app = models.OneToOneField(App, on_delete=models.SET_NULL, null=True, related_name='rank')
    rank = models.IntegerField(primary_key=True)
    last_week_rank = models.IntegerField()
    peak_in_game = models.IntegerField()
