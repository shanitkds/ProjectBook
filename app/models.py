from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    name=models.CharField(max_length=50)
    auther=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    description=models.TextField()
    cover=models.ImageField(upload_to='cover/',null=True,blank=True)
    
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.user