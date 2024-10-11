from django.db import models


class Employee(models.Model):
    image = models.ImageField(default="images/default-user.png", upload_to='employee-images')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return " ".join((self.first_name, self.last_name))


class Company(models.Model):
    name = models.CharField(max_length=255)
    stir = models.CharField(max_length=64)
    address = models.TextField()
    status = models.CharField(max_length=16)
    
    def __str__(self) -> str:
        return self.name
    
    
class Request(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    priority = models.IntegerField()
    description = models.TextField()
    long = models.CharField(max_length=256)
    lat = models.CharField(max_length=256)
    file = models.FileField(blank=True)
    
        
class RequestImage(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='request-images/')
    
    
    
    
    