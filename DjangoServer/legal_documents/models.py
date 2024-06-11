from django.db import models
from django.utils.translation import gettext_lazy as _

class Laws(models.Model):
    class Meta:
        verbose_name = _("Laws")
        verbose_name_plural = _("Luật")

    law_number = models.CharField(_("Số hiệu"), max_length=255)
    issued_date = models.DateField()
    law_name = models.TextField()
    law_link = models.CharField(max_length=255)

class Decrees(models.Model):
    class Meta:
        verbose_name = _("Decrees")
        verbose_name_plural = _("Nghị định")

    decree_number = models.CharField(_("Số hiệu"), max_length=255)
    issued_date = models.DateField(_("Ngày ban hành"))
    decree_name = models.TextField(_("Tên nghị định"))
    decree_link = models.CharField(_("Link"), max_length=255)

class Circulars(models.Model):

    class Meta:
        verbose_name = _("Circulars")
        verbose_name_plural = _("Thông tư")

    circular_number = models.CharField(max_length=255)
    issued_date = models.DateField()
    circular_name = models.TextField()
    circular_link = models.CharField(max_length=255)

class Decisions(models.Model):

    class Meta:
        verbose_name = _("Decisions")
        verbose_name_plural = _("Quyết định")

    decision_number = models.CharField(max_length=255)
    issued_date = models.DateField()
    decision_name = models.TextField()
    decision_link = models.CharField(max_length=255)
