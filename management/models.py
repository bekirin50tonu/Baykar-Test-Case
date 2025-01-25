from django.db import models

from authentication.models import Team, CustomUser


class PlaneType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name



class ItemType(models.Model):
    name = models.CharField(max_length=100)
    plane_type = models.ForeignKey(PlaneType,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PlaneRecipe(models.Model):
    plane_type = models.ForeignKey(PlaneType,on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType,on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item_type.name}-{self.count}"




class ProducedItem(models.Model):
    item = models.ForeignKey(ItemType,on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name


class ProducedPlane(models.Model):
    plane_type = models.ForeignKey(PlaneType,on_delete=models.CASCADE,default=1)
    member = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.plane_type.name

class PlaneParticipant(models.Model):
    plane = models.ForeignKey(ProducedPlane,on_delete=models.CASCADE)
    part = models.ForeignKey(ProducedItem,on_delete=models.CASCADE)

    def __str__(self):
        return self.part.item.name
