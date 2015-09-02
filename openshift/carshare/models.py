from django.db import models
from django.contrib import admin
import datetime
# Create your models here.


# Create your models here.
class user_info(models.Model):
	user_id=models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=64, default='')
	last_name = models.CharField(max_length=64, default='')
	nick_name = models.CharField(max_length=64, default='')
	phone=models.CharField(max_length=64, default='')
	email = models.EmailField()
	password=models.CharField(max_length=128)
	city = models.CharField(max_length=64)
	created = models.DateTimeField(default=datetime.datetime.now)
	

	
	
class travel_record(models.Model):
	rec_id=models.IntegerField(primary_key=True)
	from_name = models.CharField(max_length=64)
	to_name = models.CharField(max_length=64)
	from_position_lat=models.DecimalField( max_digits=19, decimal_places=10) #lat/long
	from_position_long=models.DecimalField( max_digits=19, decimal_places=10) #lat/long
	to_position_lat=models.DecimalField( max_digits=19, decimal_places=10) #lat/long
	to_position_long=models.DecimalField( max_digits=19, decimal_places=10) #lat/long
	travel_time = models.DateTimeField(default=datetime.datetime.now) #planned travel time
	isdriver=models.BooleanField(default=True)
	num_seat=models.IntegerField(default=1) #num of seats or number of people to travel
	general_info = models.CharField(max_length=512,default='')
	user_id = models.ForeignKey(user_info)
	created = models.DateTimeField(default=datetime.datetime.now)
	expired = models.DateTimeField(default=datetime.datetime.now)
	
	
class user_message(models.Model):
	msg_id=models.IntegerField(primary_key=True)
	msg_cont = models.CharField(max_length=256)
	msg_email = models.EmailField()
	msg_phone = models.CharField(max_length=64)
	user_id = models.ForeignKey(user_info)
	rec_id=models.ForeignKey(travel_record)
	created = models.DateTimeField(default=datetime.datetime.now)
	
class au_suburb(models.Model):
	rec_id=models.IntegerField(primary_key=True)
	postcode=models.IntegerField()
	suburb=models.CharField(max_length=128)
	state=models.CharField(max_length=64)
	dc=models.CharField(max_length=64)
	type=models.CharField(max_length=64)
	lat=models.DecimalField( max_digits=19, decimal_places=10) #lat/long
	lon=models.DecimalField( max_digits=19, decimal_places=10) #lat/long
	comment=models.CharField(max_length=128, default='')
	
	
admin.site.register(user_info)
admin.site.register(travel_record)
admin.site.register(user_message)
admin.site.register(au_suburb)

