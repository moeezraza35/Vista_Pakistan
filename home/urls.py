from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name="Login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profilePage, name="profile"),
    path("profile/settings/", views.settings_Page, name="settings_page"),
    path("profile/settings/edit/", views.settings_edit, name="settings_edit"),
    path("contact/", views.contact, name="contact"),
	path("signup/", views.signup, name="signup"),
	path("signup/request/", views.signup_request, name="signup-request"),
	path("signup/email-verification/", views.signup_otp_page, name="otp-page"),
	path("signup/email-verification/verify/", views.otp_verify, name="otp-verify"),
	path("forget/", views.forget_password, name="forget-password"),
	path("forget/request/", views.forget_password_request, name="forget-email"),
	path("forget/verify/", views.forget_otp_page, name="otp-page"),
	path("forget/verify/request/", views.otp_check, name="otp-check"),
	path("forget/new-password/", views.new_password, name="new-password"),
	path("forget/new-password/request/", views.new_password_set, name="new-password-request"),
	path("package/", views.packagePage, name="package"),
	path("package/book/", views.booking, name="book"),
	path("package/payment/", views.paymentPage, name="paymentPage"),
	path("package/payment/proceed/", views.payment, name="payment"),
	path("package/review/", views.review, name="review"),
]