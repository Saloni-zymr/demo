from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, birthday=None, zipcode=None, password=None
                    ):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=self.normalize_email(email),
            Date_of_Birth=birthday,
            zipcode=zipcode,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    Gender = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    address = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    contact = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=Gender)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    Date_of_Birth = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True,  null=True)
    zipcode = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_super_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser


class Flight(models.Model):
    Ticket = (
        ('B', 'Business Class'),
        ('E', 'Economic Class'),
    )
    airlines = models.CharField(max_length=30)
    dep_time = models.TimeField(max_length=30)
    dep_date = models.DateField()
    duration = models.TimeField()
    ticket_type = models.CharField(max_length=30, choices=Ticket)
    price = models.IntegerField()
    dep_city = models.CharField(max_length=30)
    des_city = models.CharField(max_length=30)
    runway_no = models.IntegerField()
    total_seats = models.IntegerField()
    avail_seats = models.IntegerField()


class Passenger(models.Model):
    Gender = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    contact = models.IntegerField()
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender)


class BookingDetails(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    f_id = models.ForeignKey(Flight, on_delete=models.CASCADE)
    trip_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    des_city = models.CharField(max_length=30)
    passenger = models.ManyToManyField(Passenger)
    no_of_passengers = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=19, decimal_places=10)
