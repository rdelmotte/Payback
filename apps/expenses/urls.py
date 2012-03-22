from django.conf.urls.defaults import patterns, url
from apps.expenses.views import group_list, create_group, expense_list, create_expense, group_members_list, create_membership
from django.views.generic import DetailView
from apps.expenses.models import Group, Expense

urlpatterns = patterns('views',
    url(r'^groups/$',
        group_list.as_view(
            context_object_name = 'groups',
            template_name       = 'expenses/group_list.html'),
        name = 'expenses-group-list'),
    url(r'^groups/add/$',
        create_group,
        name = 'expenses-create-group'),
    url(r'^group/(?P<group_id>\d+)/edit/$',
        create_group,
        name = 'expenses-edit-group'),
    url(r'^group/(?P<pk>\d+)/$',
        DetailView.as_view(
            model               = Group,
            context_object_name = 'group',
            template_name       = 'expenses/group_detail.html'),
        name = 'expenses-group-detail'),
    url(r'^group/(?P<group_id>\d+)/expenses/$',
        expense_list,
        name = 'expenses-expense-list'),
    url(r'^group/(?P<group_id>\d+)/expenses/add/$',
        create_expense,
        name = 'expenses-create-expense'),
    url(r'^group/(?P<group_id>\d+)/expense/(?P<expense_id>\d+)/edit/$',
        create_expense,
        name = 'expenses-create-expense'),
    url(r'^group/(?P<group_id>\d+)/expense/(?P<pk>\d+)/$',
        DetailView.as_view(
            model               = Expense,
            context_object_name = 'expense',
            template_name       = 'expenses/expense_detail.html'),
        name = 'expenses-expense-detail'),
    url(r'^group/(?P<group_id>\d+)/memberships/$',
        group_members_list,
        name = 'expenses-membership-list'),
    url(r'^group/(?P<group_id>\d+)/memberships/add/$',
        create_membership,
        name = 'expenses-create-membership'),
)
