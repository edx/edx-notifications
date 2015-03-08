"""
Lists of constants that can be used in the Notifications subsystem
"""

from django.conf import settings

NOTIFICATION_PRIORITY_NONE = 0
NOTIFICATION_PRIORITY_LOW = 1
NOTIFICATION_PRIORITY_MEDIUM = 2
NOTIFICATION_PRIORITY_HIGH = 3
NOTIFICATION_PRIORITY_URGENT = 4

NOTIFICATION_MAX_LIST_SIZE = getattr(settings, 'NOTIFICATION_MAX_LIST_SIZE', 100)

# client side rendering via Backbone/Underscore
RENDER_FORMAT_UNDERSCORE = 'underscore'

# for future use
RENDER_FORMAT_EMAIL = 'email'
RENDER_FORMAT_SMS = 'sms'
RENDER_FORMAT_DIGEST = 'digest'

NOTIFICATION_BULK_PUBLISH_CHUNK_SIZE = getattr(settings, 'NOTIFICATION_BULK_PUBLISH_CHUNK_SIZE', 100)
