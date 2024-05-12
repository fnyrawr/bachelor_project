from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import (
    login as auth_login,
)
from django.core.paginator import Paginator
from django.db.models import CharField, Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_api_key.permissions import HasAPIKey

from Departments.models import Department
from Qualifications.models import Qualification
from .models import User, EmployeesQualifications, UserSerializer
from .forms import CustomUserForm, SetPasswordFormImpl, SearchForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    # Login does not work if user not exists, user not set active or password does not match. Same error message for all
    # of those cases for security reasons
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        messages.success(self.request, "You are now logged in.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for error in list(form.errors.values()):
            messages.add_message(self.request, messages.ERROR, error)
        return redirect('base')


class UserCreationView(CreateView):
    model = User
    form_class = CustomUserForm
    template_name = 'users/create_user.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User successfully created.")
            return redirect('useraccounts')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template_name, {
            'form': form
        })


def edit_basedata(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        data = form.data
        User.objects.filter(id=user_id).update(
            email=data['email'],
            telephone_home=data['telephone_home'],
            telephone_mobile=data['telephone_mobile'],
            address=data['address'],
            zip_city=data['zip_city'],
        )
        messages.success(request, "Your base data has been updated.")
        return redirect('base')

    # GET request
    else:
        associated_qualifications = EmployeesQualifications.objects.filter(employee=user)
        form = CustomUserForm()
        context = {
            'form': form,
            'user': user,
            'associated_qualifications': associated_qualifications
        }
        return render(request, 'users/edit_basedata.html', context)


def edit_user(request, **kwargs):
    user_id = kwargs['pk']
    selected_user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = CustomUserForm(request.POST)
        data = form.data
        if 'is_external' in data:
            is_external = True
        else:
            is_external = False
        if 'is_active' in data:
            is_active = True
        else:
            is_active = False
        if 'is_verified' in data:
            is_verified = True
        else:
            is_verified = False
        if data['end_contract'] != '':
            end_contract = data['end_contract']
        else:
            end_contract = None
        if data['department'] != '':
            department = data['department']
        else:
            department = None
        if data['work_hours'] != '':
            work_hours = data['work_hours']
        else:
            work_hours = None
        if data['holiday_count'] != '':
            holiday_count = data['holiday_count']
        else:
            holiday_count = None
        User.objects.filter(id=user_id).update(
            username=data['username'],
            staff_id=data['staff_id'],
            is_external=is_external,
            start_contract=data['start_contract'],
            end_contract=end_contract,
            last_name=data['last_name'],
            first_name=data['first_name'],
            email=data['email'],
            telephone_home=data['telephone_home'],
            telephone_mobile=data['telephone_mobile'],
            address=data['address'],
            zip_city=data['zip_city'],
            role=data['role'],
            department=department,
            work_hours=work_hours,
            holiday_count=holiday_count,
            is_active=is_active,
            is_verified=is_verified
        )
        messages.success(request, "User has been successfully updated.")
        return redirect('useraccounts')
    # GET request
    else:
        departments = Department.objects.all()
        associated_qualifications = EmployeesQualifications.objects.filter(employee=selected_user)
        non_associated_qualifications = Qualification.objects.all().exclude(id__in=associated_qualifications.values('qualification'))
        form = CustomUserForm()
        context = {
            'form': form,
            'selected_user': selected_user,
            'departments': departments,
            'non_associated_qualifications': non_associated_qualifications,
            'associated_qualifications': associated_qualifications
        }
        return render(request, 'users/edit_user.html', context)


def add_qualification(request, **kwargs):
    user_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    selected_user = User.objects.get(id=user_id)
    selected_qualification = Qualification.objects.get(id=qualification_id)
    if not EmployeesQualifications.objects.filter(employee=selected_user, qualification=selected_qualification).exists():
        EmployeesQualifications.objects.create(employee=selected_user, qualification=selected_qualification)

    return redirect('edit_user', pk=user_id)


def remove_qualification(request, **kwargs):
    user_id = kwargs['pk1']
    qualification_id = kwargs['pk2']

    selected_user = User.objects.get(id=user_id)
    selected_qualification = Qualification.objects.get(id=qualification_id)
    entry = EmployeesQualifications.objects.filter(employee=selected_user, qualification=selected_qualification)
    if entry is not None:
        entry.delete()

    return redirect('edit_user', pk=user_id)


def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = SetPasswordFormImpl(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed.")
            return redirect('logout')
        else:
            for error in list(form.errors.values()):
                messages.add_message(request, messages.ERROR, error)
    # GET request
    form = SetPasswordFormImpl(user)
    return render(request, 'users/change_password.html', {'form': form})


def delete_user(request, **kwargs):
    user_id = kwargs['pk']
    selected_user = User.objects.get(id=user_id)
    user = request.user
    if user.role == 'A':
        selected_user.delete()
        messages.success(request, "User successfully deleted.")
    return redirect('useraccounts')


def user_list(request):
    data = None
    search = False

    if request.method == "POST":
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        keyword = data['keyword']
        # perform search over all CharFields
        fields = [f for f in User._meta.fields if isinstance(f, CharField)]
        queries = [Q(**{f.name + "__icontains": keyword}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        entries = User.objects.filter(qs) | User.objects.filter(department__name__icontains=keyword)
    else:
        entries = User.objects.order_by('first_name').order_by('last_name')

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data
    }
    return render(request, 'users/user_list.html', context)


def employee_list(request):
    data = None
    search = False

    if request.method == 'POST':
        search = True
        searchForm = SearchForm(request.POST)
        data = searchForm.data
        keyword = data['keyword']
        # perform search over all CharFields
        fields = [f for f in User._meta.fields if isinstance(f, CharField)]
        queries = [Q(**{f.name + "__icontains": keyword}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        entries = User.objects.filter(qs) | User.objects.filter(department__name__icontains=keyword)
    else:
        entries = User.objects.all()
    entries.order_by('first_name').order_by('last_name')
    # add qualifications as list to each entry
    for entry in entries:
        qualifications = EmployeesQualifications.objects.filter(employee_id=entry.id).order_by('qualification__name')
        entry.qualifications = qualifications

    paginator = Paginator(entries, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'entries': entries.count(),
        'search': search,
        'form': SearchForm,
        'data': data
    }
    return render(request, 'users/employee_list.html', context)


# HTMX
def check_username(request):
    username = request.POST.get('username')
    if len(username) == 0:
        return HttpResponse('<span class="supporting-text" id="username-error"></span>')
    if 0 < len(username) < 2:
        return HttpResponse('<span class="supporting-text amber darken-1 white-text" id="username-error">Username has to be at least 2 characters</span>')
    if User.objects.filter(username=username).exists():
        return HttpResponse('<span class="supporting-text red darken-1 white-text" id="username-error">Username already exists</span>')
    else:
        return HttpResponse('<span class="supporting-text light-green darken-1 white-text" id="username-error">Username is free</span>')


# ENDPOINT VIEWS
@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAdminUser | HasAPIKey,))
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            for attr, err in serializer.errors.items():
                if 'exists' in err[0]:
                    return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAdminUser | HasAPIKey,))
def get_user_by_username(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'user successfully deleted'}, status=status.HTTP_200_OK)
