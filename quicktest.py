import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom
import time

toast_xml_str = """
<toast>
  <visual>
    <binding template="ToastGeneric">
      <text>Test Toast</text>
      <text>This should appear from Python</text>
    </binding>
  </visual>
</toast>
"""

xml_doc = dom.XmlDocument()
xml_doc.load_xml(toast_xml_str)

notifier = notifications.ToastNotificationManager.create_toast_notifier("Python")
notification = notifications.ToastNotification(xml_doc)
notifier.show(notification) # type: ignore

# Keep alive briefly
time.sleep(2)
