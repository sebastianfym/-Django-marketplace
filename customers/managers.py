from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
    def create_user(self, email, phone, avatar=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_("User must have an email"))
        if not password:
            raise ValueError(_("User must have a password"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.phone = phone
        user.avatar = avatar
        user.email_ver = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, avatar=None, password=None,  phone=None,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if not email:
            raise ValueError(_("User must have an email"))
        if not password:
            raise ValueError(_("User must have a password"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.phone = phone
        user.avatar = avatar
        user.email_ver = True
        user.save(using=self._db)
        return user
