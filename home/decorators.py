from django.contrib.auth.decorators import user_passes_test

def staff_pengaduan_required(view_func):
    def check_staff_pengaduan(user):
        return user.groups.filter(name='staff_pengaduan').exists() or user.is_superuser
    return user_passes_test(check_staff_pengaduan)(view_func)
