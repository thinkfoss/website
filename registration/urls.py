from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from registration import views
from registration.views import *
from registration.models import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', UserRegistrationView.as_view(), name='register_user'),
    url(r'^user/$', UserRegistrationView.as_view(), name='register_user'),
    url(r'^user/success/', TemplateView.as_view(template_name='register/user/success.html'),
        name='user_registration_success'),
    url(r'^user/portal/$', ProfileHomeView.as_view(), name='portal'),
    url(r'^user/portal/mentoring/$', PortalMentoringView.as_view(), name='portal_mentoring'),
    url(r'^user/portal/mentor/view_enrolled/(?P<course_id>\d+)/$', MentorEnrolledListView.as_view(), name='mentor_view_enrolled_users'),
    url(r'^user/portal/mentor/course_progress/(?P<enrollment_id>\d+)/$', MentorProgressView.as_view(), name='course_progress'),
    url(r'^user/portal/mentor/course_progress/(?P<enrollment_id>\d+)/update/(?P<module_id>\d+)/$', MentorProgressUpdateView.as_view() , name='update_module_progress'),
    url(r'^user/portal/mentor/course_progress/update/success/$', login_required(TemplateView.as_view(template_name='portal/mentor/update_progress_success.html')),
            name='progress_update_success'),
    url(r'^user/portal/mentor/add_course$', CourseRegistrationView.as_view(), name='mentor_addcourse'),
    url(r'^user/portal/mentor/courseadd_success/$',login_required( TemplateView.as_view(template_name='portal/mentor/addcourse_success.html')), name='course_add_success'),
    url(r'^user/portal/course/edit/(?P<course_id>\d+)/$', MentorCourseUpdateView.as_view(), name='mentor_course_update'),
    url(r'^user/portal/course/edit/modules/view/(?P<course_id>\d+)/$', CourseModulesListView.as_view(), name='mentor_course_module'),
    url(r'^user/portal/course/delete/(?P<course_id>\d+)/$', CourseDeleteView.as_view(), name='mentor_course_delete'),
    url(r'^user/portal/course/edit/modules/add/(?P<course_id>\d+)/$', CourseModulesCreateView.as_view(), name='course_add_module'),
    url(r'^user/portal/course/edit/modules/edit/(?P<module_id>\d+)/$', CourseModulesEditView.as_view(), name='course_edit_module'),
    url(r'^user/portal/course/edit/modules/delete/(?P<module_id>\d+)/$', ModuleDeleteView.as_view(), name='mentor_module_delete'),
    url(r'^user/portal/mentor/module_add_success/$', login_required(TemplateView.as_view(template_name='portal/mentor/addmodule_success.html')),
            name='module_add_success'),
    url(r'^user/portal/mentor/module_edit_success/$', login_required(TemplateView.as_view(template_name='portal/mentor/editmodule_success.html')),
            name='module_edit_success'),
    url(r'^user/portal/course/edit/success/$', login_required(TemplateView.as_view(template_name='registration/course_update_success.html')),
        name='course_edit_success'),
    url(r'^user/portal/student/enrolled/$', StudentCourseEnrolledListView.as_view(), name='student_enrolled_view'),
    url(r'^user/portal/student/view_mentor/(?P<mentor_id>\d+)/$', StudentViewMentorProfile.as_view(), name='mentor_profile_view'),
    url(r'^user/portal/student/view_course/(?P<course_id>\d+)/(?P<course_name>.+)/$', StudentViewCourse.as_view(), name='student_course_view'),
    url(r'^user/portal/student/add_to_cart/(?P<course_id>\d+)/$', views.add_course_to_cart, name='add_to_cart'),
    url(r'^user/portal/student/view_cart/$', ViewCart.as_view(), name='cart_view'),
    url(r'^user/portal/student/remove_from_cart/(?P<checkout_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^user/portal/student/checkout_items/$', views.checkout_items, name='checkout_order'),
    url(r'^user/portal/student/instamojoresponse/$', views.instamojo_response, name='instamojo_response'),
    url(r'^user/profile/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^user/profile/view_public/(?P<user_id>\d+)/$', UserProfileCommonView.as_view(), name='user_profile_public'),
    url(r'^user/profile/edit/$', UserProfileUpdateView.as_view(), name='user_profile_update'),
    url(r'^user/profile/edit/success/$',
        TemplateView.as_view(template_name='registration/user_update_success.html'),
        name='user_profile_update_success'),
]
