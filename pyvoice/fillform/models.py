from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password, business_Email=None,
                    business_Name=None,
                    business_Address=None, business_Phone=None, business_Number=None):

        if not username:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        print('Details received by model')
        # print('email = ', email)
        # print('password = ', password)

        user = self.model(
            username=username,
            business_Email=self.normalize_email(business_Email),
            business_Name=business_Name,
            business_Address=business_Address,
            business_Phone=business_Phone,
            business_Number=business_Number

        )
        user.set_password(password)
        # print("user.password ", user.password)

        user.save(using=self._db)
        return user

        # user.set_password(password)
        # user.save(using=self._db)
        # return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        print('superuser')
        user.is_verified = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True

        user.save(using=self._db)
        return user


# Create your models here
class account(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=20, unique=True, default=None)
    business_Name = models.CharField(max_length=20, default=None, null=True)
    business_Email = models.EmailField(max_length=60, null=True)
    business_Address = models.CharField(max_length=256, default=None, null=True)
    business_Phone = models.CharField(max_length=15, default=None, null=True)
    business_Number = models.CharField(max_length=20, default=None, null=True)
    password = models.CharField(verbose_name="password", max_length=255)

    invoice_count = models.IntegerField(default="{0:0=5d}".format(1), null=True)

    # is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['password']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class invoice_detail(models.Model):
    invoice_Number = models.CharField(max_length=20, default=None, null=True)
    user = models.ForeignKey(account, on_delete=models.DO_NOTHING, default=None, null=True)
    logo = models.ImageField(upload_to='', default=None, null=True)

    client_Name = models.CharField(max_length=20, default=None, null=True)
    client_Email = models.EmailField(max_length=20, default=None, null=True)
    client_Address = models.CharField(max_length=20, default=None, null=True)
    client_Phone = models.CharField(max_length=20, default=None, null=True)

    date = models.DateField(default=None, null=True)
    table_Items = models.CharField(max_length=256, default=None, null=True)
    terms = models.CharField(max_length=256, default=None, null=True)

    amounts = models.CharField(max_length=256,default=None, null=True)


# class User_info(models.Model):
#     first_name = models.CharField(max_length=20)
#     last = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.first_name
