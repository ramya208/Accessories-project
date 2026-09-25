# # from django.db import models


# # class Category(models.Model):
# #     name = models.CharField(max_length=100)

# #     def __str__(self):
# #         return self.name


# # class Product(models.Model):
# #     name = models.CharField(max_length=100)
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
# #     quantity = models.IntegerField()
# #     category = models.ForeignKey(Category, on_delete=models.CASCADE)
# #     image = models.ImageField(upload_to='products/', null=True, blank=True)



# #     def __str__(self):
# #         return self.name
# from django.db import models


# class Product(models.Model):

#     name = models.CharField(
#         max_length=100
#     )

#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     image = models.ImageField(
#         upload_to='products/',
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return self.name
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    name = models.CharField(
        max_length=100
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name