from django.db import models

# Create your models here.
class Categories (models.Model):
	name = models.Charfield(max_length=128, unique=True)

	def __unicode__(self):
		return self.name


class Pages(models.Model):
	category = models.ForeignKey(Category)
	title = models.Charfield(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	def __unicode__(self):
		return self.title