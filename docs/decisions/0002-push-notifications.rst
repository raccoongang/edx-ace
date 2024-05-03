Implement Push Notification Channel
==================================================

Status
------
Accepted

Context
-------
The goal is to enhance the existing notification framework with push notifications. Flexibility and seamless integration with the existing framework are priorities for this new notification channel.

Decision
--------
Introduce a new push notification system. This will involve:

- PushNotificationRenderer: Responsible for formatting and structuring the content of a push notification (title, body, optional data payload).
- PushNotificationChannel: Handles sending formatted push notifications using the firebase_admin SDK. It is assumed that authorization will happen in the core edx-platform.

Consequences
--------
* add a push notification channel
* extend existing functionality to support push notifications
