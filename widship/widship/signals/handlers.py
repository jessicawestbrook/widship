from django.conf import settings
from django.utils.translation import ugettext_noop as _

def create_notice_types(sender, **kwargs): 
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notices for myapp")
        NoticeType.create("friends_invite", _("Invitation Received"), _("you have received an invitation"))
        NoticeType.create("friends_accept", _("Acceptance Received"), _("an invitation you sent has been accepted"))
    else:
        print("Skipping creation of NoticeTypes as notification app not found")