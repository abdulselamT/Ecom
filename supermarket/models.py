from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	address=(('Franko','Franko'),('Mebrat','Mebrat'),('POSTA','POSTA'))
	BANKS=(('AWASH','AWASH'),('abysinea','abysinea'),('CBE','CBE'),('Zemzem','Zemzem'))
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	address=models.CharField(max_length=200,null=True,choices=address)
	phone = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	bank=models.CharField(max_length=35,choices=BANKS)
	account_number=models.IntegerField(null=True,blank=True)
	total_birr=models.FloatField(default=56789)
	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Phone', 'Phone'),
			('Watch', 'Watch'),

			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	pic=models.ImageField(null=True,blank=True)
	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer,on_delete= models.CASCADE)
	product = models.ForeignKey(Product,on_delete= models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	added = models.BooleanField(default=False)
	tot=models.IntegerField(default=1)
	def __str__(self):
		return str(self.product.name) + str(self.customer.name)
	def calc_total(self):
		return self.product.price * self.tot
class Cart(models.Model):
	customer=models.ForeignKey(Customer,on_delete= models.CASCADE)
	product=models.ManyToManyField(Product)
	total=models.FloatField(default=1)
	def __str__(self):
		self.customer
	
	def calc_total(self):
		self.total=sum([k.price for k  in self.product])
		return self.total
class Historypurchase(models.Model):
	customer=models.ForeignKey(Customer,models.CASCADE)
	items=models.ManyToManyField(Product)
	total_cost=models.CharField(max_length=200,null=True)
	def __str__(self):
		self.customer.name