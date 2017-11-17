from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __unicode__(self):
        return self.name

