import csv

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import User
from core.utils.decorators import StaffLoginRequired


class UsersView(View):
    '''To get all users'''
    template = 'dashboard/pages/users.html'
    permission_required = ['accounts.view_user']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        if query:
            users = User.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query) | 
                Q(phone__icontains=query)).order_by('-created_at') # noqa
        else:
            users = User.objects.all().order_by('-created_at')
        context ={
            'users': users
        }
        return render(request, self.template, context)
    

class CreateUpdateUser(View):
    '''Create or update user'''
    template = 'dashboard/pages/create-update-user.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        context = {
            'user': user
        }
        return render(request, self.template, context)

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        status = request.POST.get('status')
        try:
            user_id = int(user_id)
        except:
            user_id = None

        user = User.objects.filter(id=user_id).first()
        if user:
            # only update if user exists and attributes are not empty
            user.name = name if name else user.name
            user.email = email if email else user.email
            user.phone = phone if phone else user.phone
            user.role = role if role else user.role
            user.status = status if status else user.status
            user.save()
            messages.success(request, 'User Profile Updated Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                user = User.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    is_staff=role.upper() == 'STAFF',
                    is_superuser=role.upper() == 'SUPERUSER',
                    is_active=status.upper() == 'ACTIVE'
                )
            except Exception as e:
                user = None
                messages.error(request, f'Error: {e}')
                return redirect('dashboard:create_update_user')
            messages.success(request, 'User Created Successfully')
        redirect_url = reverse('dashboard:create_update_user') + '?user_id=' + str(user.id)
        return redirect(redirect_url)


class UserDetailsView(View):
    '''CBV for user details'''
    template = 'dashboard/pages/user_details.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        context = {
            'user': user,
        }
        return render(request, self.template, context)



class UpdateUserProfilePicView(PermissionRequiredMixin, View):
    '''Update user profile picture'''
    permission_required = ['accounts.change_user']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        return redirect('dashboard:users')
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        user_id = request.POST.get('user_id')
        profile_pic = request.FILES.get('avatar')
        user = User.objects.filter(id=user_id).first()
        if user:
            user.avatar = profile_pic
            user.save()
            messages.success(request, 'Profile Picture Updated Successfully')
            return redirect('dashboard:users')
        else:
            messages.error(request, 'User Not Found')
            return redirect('dashboard:users')



class AddUserToGroupsView(PermissionRequiredMixin, View):
    '''CBV for adding user to groups'''
    template = 'dashboard/pages/user_details.html'
    permission_required = ['accounts.change_user']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        user_id = request.GET.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        groups = Group.objects.all().order_by('name')
        if user:
            permissions = Permission.objects.all().order_by('name')
            saved_permissions = user.user_permissions.all()
            saved_groups = user.groups.all()
            context = {
                'user': user,
                'permissions': permissions,
                'saved_groups': saved_groups,
                'groups': groups,
                'saved_permissions': saved_permissions,
            }
            return render(request, self.template, context)  # noqa
        messages.info(request, 'User Does Not Exist')
        return redirect('dashboard:users')

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        user_id = request.POST.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        user_groups = request.POST.getlist('groups')
        if user:
            user.groups.clear()
            for group in user_groups:
                item = Group.objects.filter(id=group).first()
                user.groups.add(item)
            user.save()
            messages.success(request, 'User Groups Updated Successfully')  # noqa
        else:
            messages.info(request, 'User Does Not Exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddPermsToUserView(PermissionRequiredMixin, View):
    '''CBV for assigning permissions to user'''
    template = 'dashboard/pages/user_details.html'
    permission_required = ['accounts.change_user']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        user_id = request.GET.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        groups = Group.objects.all().order_by('name')
        if user:
            permissions = Permission.objects.all().order_by('name')
            saved_permissions = user.user_permissions.all()
            saved_groups = user.groups.all()
            context = {
                'user': user,
                'permissions': permissions,
                'saved_groups': saved_groups,
                'groups': groups,
                'saved_permissions': saved_permissions,
            }
            return render(request, self.template, context)  # noqa
        messages.info(request, 'User Does Not Exist')
        return redirect('dashboard:users')

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        user_id = request.POST.get('user_id') or None
        user = User.objects.filter(id=user_id).first()
        user_permissions = request.POST.getlist('permissions')
        if user:
            user.user_permissions.clear()
            for permission in user_permissions:
                item = Permission.objects.filter(id=permission).first()
                user.user_permissions.add(item)
            user.save()
            messages.success(request, 'User Permissions Updated Successfully')  # noqa
        else:
            messages.info(request, 'User Does Not Exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DownloadUsersView(View):
    '''Download users as csv'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        users = User.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(['primary_key', 'name', 'email', 'phone', 'is_staff', 'is_superuser', 'is_active', 'created_at', 'avatar']) # noqa
        for user in users:
            base = "127.0.0.1:8000/assets/avatars/"
            avatar = f"{base}{user.avatar.url}" if user.avatar else "No Avatar"
            writer.writerow([user.id, user.name, user.email, user.phone, user.is_staff, user.is_superuser, user.is_active, user.created_at, avatar])
        return response