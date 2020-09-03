from django.db import models


# Create your models here.
class ToDoList(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class Item(models.Model):
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	text 	 = models.CharField(max_length=300)
	complete = models.BooleanField()	

	def __str__(self):
		return self.text
 
 
class Feedback(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    text  = models.CharField(max_length=300, default='0000000')
    
 
    def __str__(self):
        return self.name

class Headline(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  
  def __str__(self):
    return self.title

