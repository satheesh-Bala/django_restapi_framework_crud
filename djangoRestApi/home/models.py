from django.db import models

# person table model
class Colors(models.Model):
    color_name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name    

class Person(models.Model):
    color_id=models.ForeignKey(Colors,on_delete=models.SET_NULL,blank=True,null=True)
    name=models.CharField(max_length=100)
    age=models.IntegerField()