from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,name, email,username, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")


        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            name=name,
            username = username
        )


        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,name, email,username, phone, password=None):
        user = self.create_user(
            name=name,
            email=email,
            password=password,
            phone=phone,
            username = username
        )
        user.is_admin = True
        user.role = "admin"
        user.is_superuser = True
        user.is_staff = True


        user.save(using=self._db)
        return user
