from django.forms import ModelForm, TextInput
from apps.expenses.models import Group, Expense, Membership

class GroupForm(ModelForm):
    class Meta:
        model   = Group
        fields  = ('name',)
        widgets = {
            'name': TextInput(attrs={'placeholder': '38th Ave.'}),
        }

class ExpenseForm(ModelForm):
    class Meta:
        model   = Expense
        exclude = ('creator', 'group', 'payments',)

class MembershipForm(ModelForm):
    class Meta:
        model   = Membership
        exclude = ('group')
        # widgets = {
        #     'user': TextInput(attrs={'maxlength': 75}),
        # }
