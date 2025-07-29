# run_demo.py

import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signals.settings')
django.setup()

# Now you can import your models
from django.contrib.auth.models import User
from messaging.models import Message, Notification, MessageHistory

def run():
    """
    Main function to demonstrate the signal functionality.
    """
    # 1. Preparation: Create users if they don't exist
    print("Step 1: Preparing users...")
    user1, _ = User.objects.get_or_create(username='alice', defaults={'email': 'alice@example.com'})
    user2, _ = User.objects.get_or_create(username='bob', defaults={'email': 'bob@example.com'})
    print(f"Users '{user1.username}' and '{user2.username}' are ready.\n")

    # 2. Create a new message
    print("Step 2: Creating a new message from Alice to Bob...")
    # The post_save signal will fire after this line
    msg = Message.objects.create(
        sender=user1,
        receiver=user2,
        content="Hello Bob, hope you are well."
    )
    print(f"Message (ID: {msg.id}) created.\n")

    # 3. Check if the notification was created for Bob
    print("Step 3: Checking for notifications...")
    try:
        notification = Notification.objects.get(user=user2, message=msg)
        print(f"SUCCESS: Notification found for Bob: '{notification}'\n")
    except Notification.DoesNotExist:
        print("ERROR: Notification was not created for Bob.\n")

    # 4. Edit the message
    print("Step 4: Alice is editing her message...")
    # The pre_save signal will fire before the .save() call
    msg.content = "Hello Bob, just checking in. Hope you are well."
    msg.save()
    print("Message has been updated.\n")

    # 5. Display the final message and its history
    print("Step 5: Viewing the final message and its edit history...")
    final_message = Message.objects.get(id=msg.id)

    print("\n--- Final Message Details ---")
    print(f"  ID: {final_message.id}")
    print(f"  From: {final_message.sender.username}")
    print(f"  To: {final_message.receiver.username}")
    print(f"  Content: '{final_message.content}'")
    print(f"  Status: {'Edited' if final_message.edited else 'Original'}")

    # 6. Check the message history
    history_entries = MessageHistory.objects.filter(message=final_message)
    print("\n--- Edit History ---")
    if history_entries.exists():
        for version in history_entries:
            print(f"  - Version saved at {version.edited_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Old Content: '{version.old_content}'")
    else:
        print("  No edit history found.")

if __name__ == '__main__':
    run()