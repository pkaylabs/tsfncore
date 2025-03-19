from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''Manages User account creation'''

    def create_user(self, email, password=None, name=None, phone=None, address=None, region=None, district=None, **kwargs):
        '''Create a regular user'''
        if not email:
            raise ValueError('The Email field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            address=address,
            region=region,
            district=district,
            **kwargs
        )
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None, phone=None, address=None, region=None, district=None, **kwargs):
        '''Create a superuser'''
        if not email:
            raise ValueError('The Email field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        user = self.create_user(
            phone=phone,
            name=name,
            email=email,
            password=password,
            address=address,
            region=region,
            district=district,
            **kwargs
        )
        user.is_staff = True
        # TODO: Think through the implications again.
        user.is_superuser = True
        user.save(using=self._db)
        return user
