from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    reg_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name    


class book_category(models.Model):
    category= models.ForeignKey(Category, null=True,
                                 on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=50, unique=True)
    reg_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class book(models.Model):  # blog_article

    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.CASCADE, related_name="category")
    Bookcategory = models.ForeignKey(book_category, null=True,
                                         on_delete=models.CASCADE, related_name="books")
    title = models.CharField(verbose_name="Kitob nomi", max_length=50)
    text = models.TextField(help_text="Kitob matnini yozing")
    image = models.ImageField(upload_to="")
    file=models.FileField(upload_to="")
    price = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0, editable=False)
    sold = models.PositiveIntegerField(default=0)
    reg_date = models.DateField(auto_now_add=True)


    color = "red"

    class Meta:
        ordering = ["-reg_date"]
        verbose_name = "Book"
        verbose_name_plural = "Books"



class audio(models.Model):  # blog_article

    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.CASCADE, related_name="audios")
    Bookcategory = models.ForeignKey(book_category, null=True,
                                         on_delete=models.CASCADE, related_name="audios")
    title = models.CharField(verbose_name="Audio Kitob nomi", max_length=50)
    text = models.TextField(help_text="Audio Kitob matnini yozing")
    image = models.ImageField(upload_to="")
    file=models.FileField(upload_to="")
    price = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0, editable=False)
    sold = models.PositiveIntegerField(default=0)
    reg_date = models.DateField(auto_now_add=True)


    color = "red"

    class Meta:
        ordering = ["-reg_date"]
        verbose_name = "audio"
        verbose_name_plural = "audios"



class Comment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)  # EmailField ishlatilmoqda
    text = models.TextField(max_length=3000)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.book.price

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(book, on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")])

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
