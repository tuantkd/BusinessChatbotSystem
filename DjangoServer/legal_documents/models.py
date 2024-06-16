from django.db import models
from django.utils.translation import gettext_lazy as _

class Laws(models.Model):
    class Meta:
        verbose_name = _("Law")
        verbose_name_plural = _("Laws")

    law_number = models.CharField(_("Law Number"), max_length=255)
    issued_date = models.DateField(_("Issued Date"))
    law_name = models.TextField(_("Law Name"))
    law_link = models.CharField(_("Law Link"), max_length=255)

    def __str__(self):
        return f"{self.law_name} ({self.law_number})"

class Decrees(models.Model):
    class Meta:
        verbose_name = _("Decree")
        verbose_name_plural = _("Decrees")

    decree_number = models.CharField(_("Decree Number"), max_length=255)
    issued_date = models.DateField(_("Issued Date"))
    decree_name = models.TextField(_("Decree Name"))
    decree_link = models.CharField(_("Decree Link"), max_length=255)

    def __str__(self):
        return f"{self.decree_name} ({self.decree_number})"

class Circulars(models.Model):
    class Meta:
        verbose_name = _("Circular")
        verbose_name_plural = _("Circulars")

    circular_number = models.CharField(_("Circular Number"), max_length=255)
    issued_date = models.DateField(_("Issued Date"))
    circular_name = models.TextField(_("Circular Name"))
    circular_link = models.CharField(_("Circular Link"), max_length=255)

    def __str__(self):
        return f"{self.circular_name} ({self.circular_number})"

class Decisions(models.Model):
    class Meta:
        verbose_name = _("Decision")
        verbose_name_plural = _("Decisions")

    decision_number = models.CharField(_("Decision Number"), max_length=255)
    issued_date = models.DateField(_("Issued Date"))
    decision_name = models.TextField(_("Decision Name"))
    decision_link = models.CharField(_("Decision Link"), max_length=255)

    def __str__(self):
        return f"{self.decision_name} ({self.decision_number})"
