from apps.expenses.models import Expense, Membership, Group, Payment
from apps.expenses.forms import GroupForm, ExpenseForm, MembershipForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, RequestContext
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory

@login_required
def create_group(request, group_id=None, success_url=None,
                 template_name='expenses/create_group.html'):
    if group_id is None:
        g = Group()
    else:
        try:
            g = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise Http404

    if request.method == 'POST':
        if success_url is None:
            success_url = reverse('expenses-group-list')
        form = GroupForm(request.POST, instance=g)
        if form.is_valid():
            if group_id is None:
                g.creator   = request.user
            g.save()
            if group_id is None:
                membership      = Membership(user=request.user, group=g)
                membership.save()
            return HttpResponseRedirect(success_url)
    else:
        form = GroupForm(instance=g)

    return render_to_response(template_name,
        { 'form': form },
        context_instance=RequestContext(request))

@login_required
def create_expense(request, group_id, expense_id=None, success_url=None,
                   template_name='expenses/create_expense.html'):
    if expense_id is None:
        expense = Expense(group=Group.objects.get(pk=group_id),
            creator=request.user)
    else:
        try:
            expense = request.user.group_set.get(id=group_id).expense_set.get(id=expense_id)
        except ObjectDoesNotExist:
            raise Http404

    ExpenseFormSet = inlineformset_factory(Expense, Payment,
        can_delete=False,
        extra=2)

    if request.method == 'POST':
        if success_url is None:
            success_url = reverse('expenses-expense-list',
                kwargs={ 'group_id': group_id })
        form    = ExpenseForm(request.POST, instance=expense)
        formset = ExpenseFormSet(request.POST, instance=expense)
        if formset.is_valid() and form.is_valid():
            form.save()
            formset.save()
            return HttpResponseRedirect(success_url)
    else:
        form    = ExpenseForm(instance=expense)
        formset = ExpenseFormSet(instance=expense)

    return render_to_response(template_name,
        { 'form': form,
        'formset': formset },
        context_instance=RequestContext(request))

class group_list(ListView):
    def get_queryset(self):
         return self.request.user.group_set.all()

@login_required
def expense_list(request, group_id,
                 template_name='expenses/expense_list.html'):
    try:
        e = request.user.group_set.get(id__exact=group_id).expense_set.all()
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response(template_name,
        {'expenses': e},
        context_instance=RequestContext(request))

@login_required
def group_members_list(request, group_id,
                       template_name='expenses/membership_list.html'):
    try:
        m = request.user.group_set.get(id__exact=group_id).membership_set.all()
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response(template_name, { 'memberships': m},
        context_instance=RequestContext(request))

@login_required
def create_membership(request, group_id, success_url=None,
                      template_name='expenses/create_membership.html'):

    MembershipFormSet = modelformset_factory(Membership,
        form=MembershipForm,
        extra=1,
        can_delete=True)

    if request.method == 'POST':
        if success_url is None:
            success_url = reverse('expenses-membership-list',
                kwargs={ 'group_id': group_id })

        formset = MembershipFormSet(request.POST)

        if formset.is_valid():
            memberships = formset.save(commit=False)
            for membership in memberships:
                membership.group = Group.objects.get(id__exact=group_id)
                membership.save()

            return HttpResponseRedirect(success_url)
    else:
        try:
            g = Group.objects.get(id__exact=group_id)
            m = Membership.objects.filter(group=g)
        except ObjectDoesNotExist:
            raise Http404

        formset = MembershipFormSet(queryset=m)

    return render_to_response(template_name,
        { 'formset': formset },
        context_instance=RequestContext(request))
