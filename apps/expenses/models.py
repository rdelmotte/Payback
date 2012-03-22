from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Group(models.Model):
    creator     = models.ForeignKey(User,
        related_name    = 'group_creator')
    pubdate     = models.DateTimeField(auto_now_add=True)
    update      = models.DateTimeField(auto_now=True)
    name        = models.CharField(_('name'),
        max_length  = 100,
        validators  = [MinLengthValidator(3)])
    members     = models.ManyToManyField(User,
        through = 'Membership')

    def __unicode__(self):
        return self.name

    def members_count(self):
        return self.members.count()

    def members_names(self):
        m = self.members.all()
        if len(m) > 3:
            return "%s,..." % (", ".join([u.username for u in m[:3]]))
        return ", ".join([u.username for u in m])

    class Meta:
        verbose_name        = _('group')
        verbose_name_plural = _('groups')
        ordering            = ['name']

class Membership(models.Model):
    user            = models.ForeignKey(User)
    group           = models.ForeignKey(Group)
    date_joined     = models.DateField(auto_now_add=True)
    can_see_group   = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.group.name)

    class Meta:
        verbose_name        = _('membership')
        verbose_name_plural = _('memberships')
        unique_together     = ('user', 'group')

class Expense(models.Model):
    creator     = models.ForeignKey(User,
        related_name    ='expense_creator')
    pubdate     = models.DateTimeField(auto_now_add=True)
    update      = models.DateTimeField(auto_now=True)
    group       = models.ForeignKey(Group)
    date        = models.DateTimeField(_('date'))
    name        = models.CharField(_('name'),
        max_length  = 100,
        validators  = [MinLengthValidator(3)])
    payments    = models.ManyToManyField(User,
        through         = 'Payment',
        related_name    = 'user_payments')

    def __unicode__(self):
        return self.name

    def _get_amount(self):
        return self.payment_set.aggregate((Sum('paid')))['paid__sum']
    amount = property(_get_amount)

    def _get_num_loaners(self):
        return self.payment_set.filter(paid__isnull=False).count()
    num_loaners = property(_get_num_loaners)

    def clean(self):
        if self.creator not in self.group.members.all():
            raise ValidationError(_('Creator is not part of this group.'))

    class Meta:
        verbose_name        = _('expense')
        verbose_name_plural = _('expenses')
        ordering            = ['-date', 'name']

class Payment(models.Model):
    user        = models.ForeignKey(User)
    expense     = models.ForeignKey(Expense)
    paid        = models.DecimalField(_('paid'),
        max_digits      = 10,
        decimal_places  = 2,
        blank           = True,
        null            = True,
        validators      = [MinValueValidator(0.009)])
    is_sharing  = models.BooleanField()

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.expense)

    class Meta:
        verbose_name        = _('payment')
        verbose_name_plural = _('payments')
        unique_together     = ('user', 'expense')
