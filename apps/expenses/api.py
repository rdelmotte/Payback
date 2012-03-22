from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.constants import ALL_WITH_RELATIONS
from apps.expenses.models import Group, Expense, Payment

class UserResource(ModelResource):
    class Meta:
        queryset        = User.objects.all()
        fields          = [None]
        resource_name   = 'user'
        allowed_methods = ['get']
        authorization   = Authorization()
        authentication  = BasicAuthentication()

class GroupResource(ModelResource):
    #user        = fields.ToOneField(UserResource, 'user')
    members     = fields.ToManyField(UserResource,
            'members',
            full = True,
        )
    expenses    = fields.ToManyField('apps.expenses.api.ExpenseResource',
            'expense_set',
            related_name    = 'group',
            readonly        = True,
        )

    class Meta:
        queryset        = Group.objects.all()
        resource_name   = 'group'
        excludes        = ['creator', 'pubdate', 'id']
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization   = Authorization()
        authentication  = BasicAuthentication()
        filtering = {
                "name": ALL_WITH_RELATIONS,
            }

    def obj_create(self, bundle, request=None, **kwargs):
        return super(GroupResource, self).obj_create(bundle, request, creator=request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(creator=request.user)

class PaymentResource(ModelResource):
    user    = fields.ToOneField(UserResource, 'user', full=True)
    expense = fields.ToOneField(UserResource, 'expense')

    class Meta:
        queryset        = Payment.objects.all()
        resource_name   = 'payment'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization   = Authorization()
        authentication  = BasicAuthentication()

class ExpenseResource(ModelResource):
    creator     = fields.ToOneField(UserResource, 'creator', full=True)
    group       = fields.ToOneField(GroupResource, 'group', full=True)
    payments    = fields.ToManyField(PaymentResource, 'payments')

    class Meta:
        queryset        = Expense.objects.all()
        resource_name   = 'expense'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization   = Authorization()
        authentication  = BasicAuthentication()