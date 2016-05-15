from django.shortcuts import redirect
from thinkfoss import settings
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from registration.models import *
from registration.forms import *
from django.views.generic import ListView
from django.http import Http404
from django.http import HttpResponse
import simplejson as json
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage
from mail_templated import send_mail
import uuid
from string import Template
from django.views.decorators.csrf import csrf_exempt
from instamojo import Instamojo

class CurrentUserMixin(object):
    model = User

    def get_object(self, *args, **kwargs):
        try: obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError: obj = self.request.user
        return obj


# Create your views here
def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view


class HomePageView(ListView):
    template_name="index.html"

    def get_queryset(self):
        courses = Course.objects.filter(approved=True)[:8]
        return courses


class SolutionCreateView(FormView):
    template_name = "solutions/create_solution.html"
    form_class = SolutionCreateForm
    success_url = '/solution/create/success/'

    def form_valid(self, form):
        form.save()
        send_mail('emails/solution_created.html', {
            'solution_name': form.instance.solution_name,
            'solution_platform': form.instance.solution_platform,
            'solution_contact': form.instance.solution_contact_phone,
            'solution_deadline': form.instance.solution_deadline,
            'solution_budget': form.instance.solution_budget ,
            'solution_description': form.instance.solution_description
        }, 'admin@thinkfoss.com', [form.instance.solution_contact_email, 'admin@thinkfoss.com'])
        return FormView.form_valid(self, form)


class UserProfileView(LoginRequiredMixin, CurrentUserMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context


class UserRegistrationView(AnonymousRequiredMixin, FormView):
    template_name = "register/user/register_user.html"
    authenticated_redirect_url = reverse_lazy(u"home")
    form_class = UserRegistrationForm
    success_url = '/register/user/success/'

    def form_valid(self, form):
        form.save()
        return FormView.form_valid(self, form)


class ProfileHomeView(LoginRequiredMixin, ListView):
    template_name = 'portal/portal_learn.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        context['total_courses'] = Course.objects.filter(approved=True).count()
        if self.request.user.is_authenticated():
            context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
            context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def get_queryset(self):
        return Course.objects.filter(approved=True)


class PortalMentoringView(LoginRequiredMixin,ListView):
    template_name = 'portal/portal_mentor.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(PortalMentoringView, self).get_context_data(**kwargs)
        context['mentored_courses'] = Course.objects.filter(course_user=user).count()
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def get_queryset(self):
        self.user = self.request.user
        return Course.objects.filter(course_user=self.user).order_by('-approved')


class CourseRegistrationView( LoginRequiredMixin, FormView):
    template_name = "portal/mentor/addcourse.html"
    form_class = CourseRegistrationForm
    success_url = '/register/user/portal/mentor/courseadd_success/'

    def get_context_data(self, **kwargs):
        context = super(CourseRegistrationView, self).get_context_data(**kwargs)
        user = self.request.user
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def form_valid(self, form):
        form.instance.course_user = self.request.user
        form.save(commit=True)
        send_mail('emails/course_created.html', {'user': self.request.user, 'course': form.instance.course_name },
                  'admin@thinkfoss.com', [self.request.user.email,'admin@thinkfoss.com'])
        return FormView.form_valid(self, form)




class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('mentor_view')

    def get_object(self, queryset=None):
        self.user = self.request.user
        obj = Course.objects.get(course_id=self.kwargs['course_id'])
        if obj.course_user == self.user:
            return obj
        else:
            raise Http404("You are not allowed to edit that one.")


class MentorEnrolledListView(LoginRequiredMixin,ListView):
    template_name = 'portal/mentor/mentor_enrolled_students.html'

    def get_queryset(self):
        user = self.request.user
        course = Course.objects.get(course_id=self.kwargs['course_id'])
        items = CourseEnrollment.objects.filter(course=course,course_enrolled=True)
        return items


class MentorCourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = course_fields
    template_name_suffix = '_update_form'
    success_url = '/register/user/portal/course/edit/success/'

    def get_object(self, queryset=None):
        user = self.request.user
        obj = Course.objects.get(course_id=self.kwargs['course_id'])
        if obj.course_user == user:
            return obj
        else:
            raise Http404("You are not allowed to edit that one.")


class StudentCourseEnrolledListView(LoginRequiredMixin,ListView):
    template_name = 'portal/student/student_enrolled_view.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(StudentCourseEnrolledListView, self).get_context_data(**kwargs)
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def get_queryset(self):
        course_enrolled = []
        user = self.request.user
        items = CourseEnrollment.objects.filter(user=user,course_enrolled=True)
        for item in items:
            course_enrolled.append(item.course)

        return course_enrolled


class StudentViewMentorProfile(LoginRequiredMixin, DetailView ):
    template_name = 'portal/student/mentor_profile_view.html'

    def get_context_data(self, **kwargs):
        mentor_id = self.kwargs['mentor_id']
        mentor = User.objects.get(pk=mentor_id)
        user = self.request.user
        context = super(StudentViewMentorProfile, self).get_context_data(**kwargs)
        courses_offered_bymentor = Course.objects.filter(course_user=mentor).order_by('-approved')
        context['courses_offered_bymentor'] = courses_offered_bymentor
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        return context

    def get_object(self, queryset=None):
            mentor_id = self.kwargs['mentor_id']
            obj = User.objects.get(user_id=self.kwargs['mentor_id'])
            if obj:
                return obj
            else:
                raise Http404("No details Found.")


class UserProfileCommonView(DetailView):
    template_name = 'registration/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileCommonView, self).get_context_data(**kwargs)
        user = self.request.user
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        return context

    def get_object(self, queryset=None):
            user_id = self.kwargs['user_id']
            obj = User.objects.get(user_id=self.kwargs['user_id'])
            if obj:
                return obj
            else:
                raise Http404("No details Found.")


class StudentViewCourse(DetailView):
    template_name = 'portal/student/student_view_course.html'

    def get_context_data(self, **kwargs):
        course_id = self.kwargs['course_id']
        user = self.request.user
        course = Course.objects.get(pk=course_id)
        mentor_id = course.get_mentor().get_user_id()
        context = super(StudentViewCourse, self).get_context_data(**kwargs)
        mentor_details = User.objects.get(pk=mentor_id)
        context['mentor'] = mentor_details
        modules = CourseModules.objects.filter(course=course).order_by('module_id')
        context['modules'] = modules
        if not user.is_anonymous():
            obj = CourseEnrollment.objects.filter(course=course,user=user)
            for enrollment in obj:
                if enrollment:
                    if enrollment.has_checked_out():
                        context['enrolled'] = 'True'
                    else:
                        context['in_cart'] = 'True'
        context['total_courses'] = Course.objects.filter(approved=True).count()
        if self.request.user.is_authenticated():
            context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
            context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()

        return context

    def get_object(self, queryset=None):
            mentor_id = self.kwargs['course_id']
            obj = Course.objects.get(course_id=self.kwargs['course_id'])
            if obj:
                return obj
            else:
                raise Http404("No details Found.")


def add_course_to_cart(request,course_id ):
    course = Course.objects.get(pk=course_id)
    user = request.user
    CourseEnrollment.objects.add_to_cart(course,user)
    return redirect(request.META['HTTP_REFERER'])


def remove_from_cart(request,checkout_id ):
    item = CourseEnrollment.objects.get(pk=checkout_id)
    user = request.user
    if item.owner_of_item() == user:
        CourseEnrollment.objects.get(pk=checkout_id).delete()
    return redirect(request.META['HTTP_REFERER'])


def checkout_items(request):
    user = request.user
    total_cost = 0

    for item_order in request.POST.getlist('order'):
        item = CourseEnrollment.objects.get(pk=item_order)
        total_cost = total_cost + item.course.course_fees

    if total_cost > 0:
        api_key = settings.API_KEY
        auth_token = settings.AUTH_TOKEN

        api = Instamojo(api_key=api_key,auth_token=auth_token)
        api_request = api.payment_request_create(
            purpose="ThinkFOSS transaction",
            send_email=True,
            email=user.email,
            amount=total_cost,
            redirect_url="http://www.thinkfoss.com/register/user/portal/student/instamojoresponse/"
        )

        order_id = api_request['payment_request']['id']
        current_order = Order.objects.start_checkout(order_id, total_cost, user)
        for item_order in request.POST.getlist('order'):
            item = CourseEnrollment.objects.get(pk=item_order)
            item.order = current_order
            item.save()

        return redirect(api_request['payment_request']['longurl'])
    else:
        # Free course
        for item_order in request.POST.getlist('order'):
            item = CourseEnrollment.objects.get(pk=item_order)
            setattr(item,'course_enrolled',True)
            item.save()
            send_mail('emails/checkout_success.html', {'user': request.user, 'item': item.course.course_name },
                      'admin@thinkfoss.com', [user.email])
            send_mail('emails/notify_mentor.html',
                      {'user': request.user, 'mentor':item.course.course_user.user_first_name , 'item': item.course.course_name },
                      'admin@thinkfoss.com', [item.course.course_user.email, 'admin@thinkfoss.com'])

            return render_to_response('portal/cart/checkout_result.html', {'success': 'success'})


@csrf_exempt
def instamojo_response(request):
    user = request.user
    payment_id = request.GET.get('payment_id')
    payment_request_id = request.GET.get('payment_request_id')

    api_key = settings.API_KEY
    auth_token = settings.AUTH_TOKEN

    api = Instamojo(api_key=api_key,auth_token=auth_token)
    response = api.payment_request_payment_status(payment_request_id,payment_id)
    if response['payment_request']['status'] == "Completed":
        paid_amount = response['payment_request']['payment']['amount']
        order = Order.objects.get(pk=payment_request_id)
        if order.amount == float(paid_amount) and order.order_id == payment_request_id:
            order.tracking_id = response['payment_request']['payment']['payment_id']
            order.save()
            cart_itmes = CourseEnrollment.objects.filter(order=order)
            for item in cart_itmes:
                setattr(item,'course_enrolled',True)
                item.save()
                send_mail('emails/checkout_success.html', {'user': item.owner_of_item(), 'item': item.course.course_name },
                          'admin@thinkfoss.com', [item.owner_of_item().email])
                send_mail('emails/notify_mentor.html',
                          {'user': item.owner_of_item(), 'mentor':item.course.course_user.user_first_name, 'item': item.course.course_name },
                          'admin@thinkfoss.com', [item.course.course_user.email, 'admin@thinkfoss.com'])

            return render_to_response('portal/cart/checkout_result.html', {'success': 'success'})
        else:
            return render_to_response('portal/cart/checkout_result.html', {'failure': 'failure'})
    else:
        return render_to_response('portal/cart/checkout_result.html', {'failure': 'fail'})


class ViewCart(LoginRequiredMixin, ListView):
    template_name = 'portal/cart/view_cart.html'

    def get_context_data(self, **kwargs):
        context = super(ViewCart, self).get_context_data(**kwargs)
        user = self.request.user
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        return context

    def get_queryset(self):
        user = self.request.user
        return CourseEnrollment.objects.filter(user=user,course_enrolled=False)


class UserProfileUpdateView(LoginRequiredMixin, CurrentUserMixin, UpdateView):
    model = User
    fields = user_fields + user_extra_fields
    template_name_suffix = '_update_form'
    success_url = '/register/user/profile/'

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        return context


class CourseModulesListView(LoginRequiredMixin,ListView):
    template_name = 'portal/mentor/course_module_view.html'

    def get_context_data(self, **kwargs):
        course_id = self.kwargs['course_id']
        context = super(CourseModulesListView, self).get_context_data(**kwargs)
        context['course_id'] = course_id
        user = self.request.user
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        return CourseModules.objects.filter(course=course).order_by('module_id')


class CourseModulesCreateView(LoginRequiredMixin, FormView):
    template_name = 'portal/mentor/course_module_create.html'
    form_class = ModuleAddForm
    success_url = '/register/user/portal/mentor/module_add_success/'

    def get_context_data(self, **kwargs):
        context = super(CourseModulesCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def form_valid(self, form):
        course = self.kwargs['course_id']
        course = Course.objects.get(pk=course)
        form.instance.course = course
        form.save(commit=True)
        return FormView.form_valid(self, form)


class CourseModulesEditView(LoginRequiredMixin, UpdateView):
    model = CourseModules
    fields = course_module_fields
    template_name_suffix = '_update_form'
    success_url = '/register/user/portal/mentor/module_edit_success/'

    def get_context_data(self, **kwargs):
        context = super(CourseModulesEditView, self).get_context_data(**kwargs)
        module_id = self.kwargs['module_id']
        obj = CourseModules.objects.get(pk=module_id)
        if obj.course.get_mentor() == self.request.user:
            context['module'] = obj

        user = self.request.user
        context['total_courses'] = Course.objects.filter(approved=True).count()
        context['enrolled_courses'] = CourseEnrollment.objects.filter(user=user,course_enrolled=True).count()
        context['in_cart_items'] = CourseEnrollment.objects.filter(user=user,course_enrolled=False).count()
        return context

    def get_object(self, queryset=None):
        module_id = self.kwargs['module_id']
        obj = CourseModules.objects.get(pk=module_id)
        if obj.course.get_mentor() == self.request.user:
            return obj
        else:
            raise Http404("You are not allowed to edit that one.")


class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = CourseModules
    success_url = reverse_lazy('mentor_view')

    def get_object(self, queryset=None):
        user = self.request.user
        obj = CourseModules.objects.get(module_id=self.kwargs['module_id'])
        if obj.course.course_user == user:
            return obj
        else:
            raise Http404("You are not allowed to edit that one.")


class MentorProgressView(LoginRequiredMixin,ListView):
    template_name = 'portal/mentor/mentor_course_progress.html'

    def get_context_data(self, **kwargs):
        context = super(MentorProgressView, self).get_context_data(**kwargs)
        enrollment_id = self.kwargs['enrollment_id']
        context['enrollment_id'] = enrollment_id
        return context

    def get_queryset(self):
        enrollment_id = self.kwargs['enrollment_id']
        courseEnrollment = CourseEnrollment.objects.get(pk=enrollment_id)
        course = courseEnrollment.get_course()
        return CourseModules.objects.filter(course=course)


class MentorProgressUpdateView(LoginRequiredMixin, UpdateView):
    model = CourseProgress
    fields = progress_fields
    template_name_suffix = '_update_form'
    success_url = '/register/user/portal/mentor/course_progress/update/success/'

    def get_object(self, queryset=None):
        self.user = self.request.user
        checkout = self.kwargs['enrollment_id']
        module = self.kwargs['module_id']
        enrollemnt_item = CourseEnrollment.objects.get(pk=checkout)
        item_module = CourseModules.objects.get(pk=module)
        if item_module.course.course_user == self.request.user:
            try:
                obj = CourseProgress.objects.get(checkout=checkout,module=module)
            except self.model.DoesNotExist:
                obj = CourseProgress.objects.create_progress(enrollemnt_item, item_module)
            return obj
        else:
            raise Http404("You are not allowed to edit that one.")