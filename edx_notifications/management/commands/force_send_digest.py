"""
Django management command to force-send the daily/weekly digest emails
"""

import logging
import logging.config
import sys

# Have all logging go to stdout with management commands
# this must be up at the top otherwise the
# configuration does not appear to take affect
import datetime
import pytz
from edx_notifications import const
from edx_notifications.digests import send_unread_notifications_digest, send_unread_notifications_namespace_digest

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
logging.config.dictConfig(LOGGING)

from django.core.management.base import BaseCommand, CommandError

log = logging.getLogger(__file__)

from optparse import make_option, OptionParser


class Command(BaseCommand):
    """
    Django management command to force-send the daily/weekly digest emails
    """

    help = 'Command to force-send the daily/weekly digest emails'

    option_list = BaseCommand.option_list + (
        make_option(
            '--daily',
            action='store_true',
            dest='send_daily_digest',
            default=False,
            help='Force send daily digest email.'
        ),
    )

    option_list = option_list + (
        make_option(
            '--weekly',
            action='store_true',
            dest='send_weekly_digest',
            default=False,
            help='Force send weekly digest email.'
        ),
    )

    option_list = option_list + (
        make_option(
            '--ns',
            dest='namespace',
            default='All',
            help='Specify the namespace. Default = All.'
        ),
    )

    def send_daily_digest(self, namespace='All'):
        """
        Sends the daily digest.
        """
        from_timestamp = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=1)
        to_timestamp = datetime.datetime.now(pytz.UTC)
        preference_name = const.NOTIFICATION_DAILY_DIGEST_PREFERENCE_NAME
        subject = const.NOTIFICATION_DAILY_DIGEST_SUBJECT
        from_email = const.NOTIFICATION_DIGEST_FROM_ADDRESS

        if namespace == "All":
            send_unread_notifications_digest(from_timestamp, to_timestamp, preference_name, subject, from_email)
        else:
            send_unread_notifications_namespace_digest(
                namespace, from_timestamp, to_timestamp, preference_name, subject, from_email
            )

    def send_weekly_digest(self, namespace='All'):
        """
        Sends the weekly digest.
        """
        from_timestamp = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=7)
        to_timestamp = datetime.datetime.now(pytz.UTC)
        preference_name = const.NOTIFICATION_WEEKLY_DIGEST_PREFERENCE_NAME
        subject = const.NOTIFICATION_WEEKLY_DIGEST_SUBJECT
        from_email = const.NOTIFICATION_DIGEST_FROM_ADDRESS

        if namespace == "All":
            send_unread_notifications_digest(from_timestamp, to_timestamp, preference_name, subject, from_email)
        else:
            send_unread_notifications_namespace_digest(
                namespace, from_timestamp, to_timestamp, preference_name, subject, from_email
            )

    def handle(self, *args, **options):
        """
        Management command entry point, simply call into the
        """

        usage = "usage: %prog [--daily] [--weekly] [--ns=NAMESPACE]"
        parser = OptionParser(usage=usage)

        log.info("Running management command ...")

        if options['send_daily_digest']:
            self.send_daily_digest(options['namespace'])
            log.info("Sending the daily digest with namespace=%s...", options['namespace'])

        if options['send_weekly_digest']:
            self.send_weekly_digest(options['namespace'])
            log.info("Sending the weekly digest with namespace=%s...", options['namespace'])

        if not options['send_weekly_digest'] and not options['send_daily_digest']:
            parser.print_help()
            raise CommandError("Neither Daily, nor Weekly digest specified.")

        log.info("Completed .")