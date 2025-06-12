from django.db import models

# Create your models here.

class employee(models.Model):
    desg = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="emp_photo/")

    def __str__(self):
        return self.name

class service(models.Model):
    image = models.ImageField(upload_to='ser_photo/')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name   


class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    categeory = models.CharField(max_length=60)
    decribe = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

class contactForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name
