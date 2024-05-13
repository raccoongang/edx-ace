"""
Channel for sending push notifications.
"""
import logging
import re

from django.conf import settings

from push_notifications.gcm import send_message, dict_to_fcm_message
from push_notifications.models import GCMDevice

from edx_ace.channel import Channel, ChannelType
from edx_ace.errors import FatalChannelDeliveryError
from edx_ace.message import Message
from edx_ace.renderers import RenderedPushNotification

LOG = logging.getLogger(__name__)


class PushNotificationChannel(Channel):
    """
    A channel for sending push notifications.
    """

    channel_type = ChannelType.PUSH

    @classmethod
    def enabled(cls):
        """
        Returns true if the push notification settings are configured.
        """
        return getattr(settings, 'PUSH_NOTIFICATIONS_SETTINGS', None)

    def deliver(self, message: Message, rendered_message: RenderedPushNotification) -> None:
        """
        Transmit a rendered message to a recipient.

        Args:
            message: The message to transmit.
            rendered_message: The rendered content of the message that has been personalized
                for this particular recipient.
        """
        device_tokens = self.get_user_device_tokens(message.recipient.lms_user_id)
        if not device_tokens:
            LOG.info(f'Recipient {message.recipient.email_address} has no push token. Skipping push notification.')
            return

        for token in device_tokens:
            self.send_message(message, token, rendered_message)

    def send_message(self, message: Message, token: str, rendered_message: RenderedPushNotification) -> None:
        """
        Send a push notification to a device by token.
        """
        notification_data = {
            'title': self.sanitize_html(rendered_message.subject),
            'body': self.sanitize_html(rendered_message.body),
            'notification_key': token,
            **message.context.get('push_notification_extra_context', {}),
        }
        message = dict_to_fcm_message(notification_data)
        try:
            send_message(token, message, settings.FCM_APP_NAME)
        except Exception as e:
            LOG.exception(f'Failed to send push notification to {token}')
            raise FatalChannelDeliveryError(f'Failed to send push notification to {token}')

    @staticmethod
    def get_user_device_tokens(user_id: int) -> list:
        """
        Get the device tokens for a user.
        """
        return list(GCMDevice.objects.filter(
            user_id=user_id,
            cloud_message_type='FCM',
            active=True,
        ).values_list('registration_id', flat=True))

    @staticmethod
    def sanitize_html(html_str: str) -> str:
        """
        Compress spaces and remove newlines to make it easier to author templates.
        """
        return re.sub('\\s+', ' ', html_str, re.UNICODE).strip()
