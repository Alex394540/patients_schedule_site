from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=150, unique=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
    	return self.name


class News(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created', 'title']
    
    @property
    def formatted_creation_time(self):
        return self.created.strftime("%Y-%m-%d %H:%M")

    def __str__(self):
    	return "{}    {}".format(self.formatted_creation_time, self.title)
