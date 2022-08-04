from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib import admin
from django.core.validators import MinLengthValidator



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)  # ?*
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    App base user class.
    Email and password are required. Other fields are optional.
    """

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % self.first_name
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=50)
    responsavel = models.CharField('Responsável', max_length=50)
    email = models.CharField('E-mail', max_length=50)
    telefone1 = models.CharField('Telefone 1', max_length=14)
    telefone2 = models.CharField('Telefone 2 (opcional)', max_length=14, blank=True, null=True)
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = self.pk

    def get_absolute_url(self):
        return reverse('detalhe_cliente', kwargs={'slug': self.slug})


class Certificado(models.Model):
    ticket_validator = MinLengthValidator(11, 'Confira o número do ticket')

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    ticket = models.CharField('Ticket', max_length=11, validators=[ticket_validator])
    produto = models.CharField('Produto', max_length=50)
    emissao = models.DateField('Emissão')
    validade = models.DateField('Validade')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    observacao = models.CharField('Observação', max_length=100, blank=True, null=True)
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = self.pk

    def get_absolute_url(self):
        return reverse('detalhe_certificado', kwargs={'slug': self.slug})

