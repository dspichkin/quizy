from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from . import views

urlpatterns = patterns(
    "",
    # url(r"^signup/$", views.signup, name="account_signup"),
    # url(r"^login/$", views.login, name="account_login"),
    url(r"^logout/$", views.logout, name="account_logout"),

    url(r"^password/change/$", views.password_change,
        name="account_change_password"),
    url(r"^password/set/$", views.password_set, name="account_set_password"),

    url(r"^ajax-signup/$", views.ajax_signup, name="account_ajax_signup"),
    url(r"^ajax-login/$", views.ajax_login, name="account_ajax_login"),
    url(r"^ajax-logout/$", views.ajax_logout, name="account_ajax_logout"),
    url(r"^ajax-recall/$", views.ajax_recall, name="account_ajax_recall"),

    url(r"^inactive/$", views.account_inactive, name="account_inactive"),

    # E-mail
    # url(r"^email/$", views.email, name="account_email"),
    url(r"^ajax-confirm-email-send/$", views.ajax_email_verification_sent,
        name="account_email_verification_sent"),
    url(r"^ajax-confirm-email/$", views.ajax_confirm_email,
        name="account_confirm_email"),
    url(r"^ajax-confirm-email/(?P<key>\w+)/$", views.ajax_confirm_email_key,
        name="account_confirm_email"),
    # Handle old redirects
    # url(r"^ajax-confirm_email/(?P<key>\w+)/$",
    #    RedirectView.as_view(url='/accounts/confirm-email/%(key)s/',
    #                         permanent=True)),

    url(r"^ajax-profile/$", views.ajax_profile,
        name="ajax_profile/"),
    # password reset
    url(r"^password/reset/$", views.password_reset,
        name="account_reset_password"),
    url(r"^password/reset/done/$", views.password_reset_done,
        name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$", views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"),
)
