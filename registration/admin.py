from django.contrib import admin
from registration.models import User, Course, CourseEnrollment, CourseModules, Solution, CourseProgress, Order

class UserAdmin(admin.ModelAdmin):
    search_fields = ('user_first_name', 'user_last_name', 'email')
    list_display = ('user_first_name', 'user_last_name', 'email', 'date_joined')
admin.site.register(User, UserAdmin)


class CourseAdmin(admin.ModelAdmin):
    search_fields = ('course_name', 'course_user')
    list_display = ('course_name', 'course_created', 'course_user','approved' )
    list_filter = ('approved',)
admin.site.register(Course, CourseAdmin)



class CourseEnrollmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)


class CourseModulesAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'course', 'module_id' )
admin.site.register(CourseModules, CourseModulesAdmin)


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('solution_name', 'solution_contact_email','solution_contact_phone', 'solution_created' )
admin.site.register(Solution, SolutionAdmin)


class CourseProgressAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseProgress, CourseProgressAdmin)


class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)
