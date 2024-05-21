Implement Push Notification Channel
==================================================

Status
------
Accepted

Context
------
The goal is to enhance the existing notification framework with push notifications.
Flexibility and seamless integration with the existing framework are priorities
for this new notification channel. Currently, edx-ace supports various email channels
like django and Sailthru, but lacks support for mobile push notifications. This feature will
enable real-time communication with users through their mobile devices, enhancing user
engagement and ensuring timely delivery of important information.

Decision
------
Introduce a new push notification system.

This will involve:
  - PushNotificationRenderer: Responsible for formatting and structuring the content
    of a push notification. This includes setting the notification's title, body,
    and optional data payload. The renderer will ensure that the notification content
    adheres to the specifications required by the `firebase_admin SDK <https://github.com/firebase/firebase-admin-python/>`_.
  - PushNotificationChannel: Handles sending formatted push notifications using
    the `firebase_admin SDK <https://github.com/firebase/firebase-admin-python/>`_.
    The channel will integrate with `django-push-notifications<https://github.com/jazzband/django-push-notifications/>`_
    to streamline the process of dispatching notifications. The core edx-platform
    will handle authorization and manage Firebase credentials, ensuring secure and
    authenticated communication with the Firebase Cloud Messaging (FCM) service.


Responsibilities:
------
Accept notification content and metadata.
Format the content to match the requirements of mobile push notifications.
Include optional data payloads for enhanced functionality (e.g., deep links, custom actions).

Consequences
------

Positive:
  - Adds a new push notification channel, enhancing the notification system's capabilities.
  - Allows real-time communication with users, improving engagement and user experience.
  - Seamless integration with existing edx-ace framework, maintaining consistency and reliability.
  - Utilizes django-push-notifications and firebase_admin, leveraging robust and widely-used
    technologies for push notifications.

Negative:
  - Additional complexity in the notification system, requiring maintenance and potential updates.
  - Dependency on Firebase Cloud Messaging (FCM) service, which might introduce external service dependency risks.

Rejection
------

