from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import secrets 

class UserManager(BaseUserManager):
    def generate_patient_code(self):
        for _ in range(10):
            code = secrets.token_hex(4)[:8]
            if not User.objects.filter(patient_code=code).exists():
                return code
        raise ValueError('Unable to generate patient code')

    def create_user(self, email, name, password=None, role='patient', **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)

        if role == 'patient':
            extra_fields['patient_code'] = self.generate_patient_code()

        user = self.model(email=email, name=name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, name='Admin', password=password, role='admin', **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser , PermissionsMixin):
    ROLE_CHOICES =[
        ('patient','Patient'),
        ('doctor','Doctor'),
        ('nurse','Nurse'),
        ('admin','admin'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  
    patient_code = models.CharField(max_length=8, unique=True, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return f"{self.email}({self.role})"

