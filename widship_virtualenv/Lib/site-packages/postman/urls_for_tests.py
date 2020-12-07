"""
URLconf for tests.py usage.

"""
from django import VERSION
from django.conf import settings
if VERSION < (2, 0):
    from django.conf.urls import include, url as re_path
else:
    from django.urls import include, re_path
from django.contrib.auth import views as auth_views
from django.forms import ValidationError
if getattr(settings, 'POSTMAN_I18N_URLS', False):
    from django.utils.translation import pgettext_lazy
else:
    def pgettext_lazy(c, m): return m
from django.views.generic import TemplateView

from .views import (InboxView, SentView, ArchivesView, TrashView,
        WriteView, ReplyView, MessageView, ConversationView,
        ArchiveView, DeleteView, UndeleteView, MarkReadView, MarkUnreadView,
        IndexView)


# user_filter function set
def user_filter_reason(user):
    if user.get_username() == 'bar':
        return 'some reason'
    return None
def user_filter_no_reason(user):
    return ''
def user_filter_false(user):
    return False
def user_filter_exception(user):
    if user.get_username() == 'bar':
        raise ValidationError(['first good reason', "anyway, I don't like {0}".format(user.get_username())])
    return None

# exchange_filter function set
def exch_filter_reason(sender, recipient, recipients_list):
    if recipient.get_username() == 'bar':
        return 'some reason'
    return None
def exch_filter_no_reason(sender, recipient, recipients_list):
    return ''
def exch_filter_false(sender, recipient, recipients_list):
    return False
def exch_filter_exception(sender, recipient, recipients_list):
    if recipient.get_username() == 'bar':
        raise ValidationError(['first good reason', "anyway, I don't like {0}".format(recipient.get_username())])
    return None

# auto-moderation function set
def moderate_as_51(message):
    return 51
def moderate_as_48(message):
    return (48, "some reason")
moderate_as_48.default_reason = 'some default reason'

# quote formatters
def format_subject(subject):
    return "Re_ " + subject
def format_body(sender, body):
    return "{0} _ {1}".format(sender, body)

postman_patterns = [
    # Basic set
    re_path(pgettext_lazy('postman_url', r'^inbox/(?:(?P<option>m)/)?$'), InboxView.as_view(), name='inbox'),
    re_path(pgettext_lazy('postman_url', r'^sent/(?:(?P<option>m)/)?$'), SentView.as_view(), name='sent'),
    re_path(pgettext_lazy('postman_url', r'^archives/(?:(?P<option>m)/)?$'), ArchivesView.as_view(), name='archives'),
    re_path(pgettext_lazy('postman_url', r'^trash/(?:(?P<option>m)/)?$'), TrashView.as_view(), name='trash'),
    re_path(pgettext_lazy('postman_url', r'^write/(?:(?P<recipients>[^/#]+)/)?$'), WriteView.as_view(), name='write'),
    re_path(pgettext_lazy('postman_url', r'^reply/(?P<message_id>[\d]+)/$'), ReplyView.as_view(), name='reply'),
    re_path(pgettext_lazy('postman_url', r'^view/(?P<message_id>[\d]+)/$'), MessageView.as_view(), name='view'),
    re_path(pgettext_lazy('postman_url', r'^view/t/(?P<thread_id>[\d]+)/$'), ConversationView.as_view(), name='view_conversation'),
    re_path(pgettext_lazy('postman_url', r'^archive/$'), ArchiveView.as_view(), name='archive'),
    re_path(pgettext_lazy('postman_url', r'^delete/$'), DeleteView.as_view(), name='delete'),
    re_path(pgettext_lazy('postman_url', r'^undelete/$'), UndeleteView.as_view(), name='undelete'),
    re_path(pgettext_lazy('postman_url', r'^mark-read/$'), MarkReadView.as_view(), name='mark-read'),
    re_path(pgettext_lazy('postman_url', r'^mark-unread/$'), MarkUnreadView.as_view(), name='mark-unread'),
    re_path(r'^$', IndexView.as_view()),

    # Customized set
    # 'success_url'
    re_path(r'^write_sent/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(success_url='postman:sent'), name='write_with_success_url_to_sent'),
    re_path(r'^reply_sent/(?P<message_id>[\d]+)/$', ReplyView.as_view(success_url='postman:sent'), name='reply_with_success_url_to_sent'),
    re_path(r'^archive_arch/$', ArchiveView.as_view(success_url='postman:archives'), name='archive_with_success_url_to_archives'),
    re_path(r'^delete_arch/$', DeleteView.as_view(success_url='postman:archives'), name='delete_with_success_url_to_archives'),
    re_path(r'^undelete_arch/$', UndeleteView.as_view(success_url='postman:archives'), name='undelete_with_success_url_to_archives'),
    # 'max'
    re_path(r'^write_max/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(max=1), name='write_with_max'),
    re_path(r'^reply_max/(?P<message_id>[\d]+)/$', ReplyView.as_view(max=1), name='reply_with_max'),
    # 'user_filter' on write
    re_path(r'^write_user_filter_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_reason), name='write_with_user_filter_reason'),
    re_path(r'^write_user_filter_no_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_no_reason), name='write_with_user_filter_no_reason'),
    re_path(r'^write_user_filter_false/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_false), name='write_with_user_filter_false'),
    re_path(r'^write_user_filter_exception/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_exception), name='write_with_user_filter_exception'),
    # 'user_filter' on reply
    re_path(r'^reply_user_filter_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_reason), name='reply_with_user_filter_reason'),
    re_path(r'^reply_user_filter_no_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_no_reason), name='reply_with_user_filter_no_reason'),
    re_path(r'^reply_user_filter_false/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_false), name='reply_with_user_filter_false'),
    re_path(r'^reply_user_filter_exception/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_exception), name='reply_with_user_filter_exception'),
    # 'exchange_filter' on write
    re_path(r'^write_exch_filter_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_reason), name='write_with_exch_filter_reason'),
    re_path(r'^write_exch_filter_no_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_no_reason), name='write_with_exch_filter_no_reason'),
    re_path(r'^write_exch_filter_false/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_false), name='write_with_exch_filter_false'),
    re_path(r'^write_exch_filter_exception/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_exception), name='write_with_exch_filter_exception'),
    # 'exchange_filter' on reply
    re_path(r'^reply_exch_filter_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_reason), name='reply_with_exch_filter_reason'),
    re_path(r'^reply_exch_filter_no_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_no_reason), name='reply_with_exch_filter_no_reason'),
    re_path(r'^reply_exch_filter_false/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_false), name='reply_with_exch_filter_false'),
    re_path(r'^reply_exch_filter_exception/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_exception), name='reply_with_exch_filter_exception'),
    # 'auto_moderators'
    re_path(r'^write_moderate/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(auto_moderators=(moderate_as_51,moderate_as_48)), name='write_moderate'),
    re_path(r'^reply_moderate/(?P<message_id>[\d]+)/$', ReplyView.as_view(auto_moderators=(moderate_as_51,moderate_as_48)), name='reply_moderate'),
    # 'formatters'
    re_path(r'^reply_formatters/(?P<message_id>[\d]+)/$', ReplyView.as_view(formatters=(format_subject, format_body)), name='reply_formatters'),
    re_path(r'^view_formatters/(?P<message_id>[\d]+)/$', MessageView.as_view(formatters=(format_subject, format_body)), name='view_formatters'),
    # auto-complete
    re_path(r'^write_ac/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(autocomplete_channels=('postman_multiple_as1-1', None)), name='write_auto_complete'),
    re_path(r'^reply_ac/(?P<message_id>[\d]+)/$', ReplyView.as_view(autocomplete_channel='postman_multiple_as1-1'), name='reply_auto_complete'),
    # 'template_name'
    re_path(pgettext_lazy('postman_url', r'^inbox_template/(?:(?P<option>m)/)?$'), InboxView.as_view(template_name='postman/fake.html'), name='inbox_template'),
    re_path(pgettext_lazy('postman_url', r'^sent_template/(?:(?P<option>m)/)?$'), SentView.as_view(template_name='postman/fake.html'), name='sent_template'),
    re_path(pgettext_lazy('postman_url', r'^archives_template/(?:(?P<option>m)/)?$'), ArchivesView.as_view(template_name='postman/fake.html'), name='archives_template'),
    re_path(pgettext_lazy('postman_url', r'^trash_template/(?:(?P<option>m)/)?$'), TrashView.as_view(template_name='postman/fake.html'), name='trash_template'),
    re_path(r'^write_template/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(template_name='postman/fake.html'), name='write_template'),
    re_path(r'^reply_template/(?P<message_id>[\d]+)/$', ReplyView.as_view(template_name='postman/fake.html'), name='reply_template'),
    re_path(r'^view_template/(?P<message_id>[\d]+)/$', MessageView.as_view(template_name='postman/fake.html'), name='view_template'),
    re_path(r'^view_template/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(template_name='postman/fake.html'), name='view_conversation_template'),
    # context processors
    re_path(r'^context_processors/$', TemplateView.as_view(template_name='postman_for_tests/context_processors.html'), name='context_processors'),
    re_path(r'^no_context_processors/$',
        TemplateView.as_view(template_name='postman_for_tests/email_html_and_empty_txt.txt'),  # this one is fine, as it's empty
        name='no_context_processors'),
]

urlpatterns = [
    re_path(r'^accounts/login/$', auth_views.LoginView.as_view()),  # because of the login_required decorator
    re_path(r'^messages/',
        # (<patterns object>, <application namespace>), namespace=<instance namespace>
        include((postman_patterns, 'postman'), namespace='postman')),
]

# because of fields.py/AutoCompleteWidget/render()/reverse()
if 'ajax_select' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^ajax_select/', include('ajax_select.urls')),  # django-ajax-selects
    ]
