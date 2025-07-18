from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

# --- 1. Admin Configuration for the Custom User Model ---

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Configuration for the custom User model in the admin interface.
    """
    # Use the custom fieldsets to include the 'role' and 'phone_number' fields
    # This adds a new section called 'Custom Fields' to the user edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )
    
    # Display these fields in the main list view of users
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    
    # Add 'role' to the filters on the right-hand side
    list_filter = UserAdmin.list_filter + ('role',)
    
    # Enable searching by these fields
    search_fields = ('email', 'first_name', 'last_name')
    
    # Default ordering
    ordering = ('email',)


# --- 2. Admin Configuration for the Conversation Model ---

class MessageInline(admin.TabularInline):
    """
    Allows viewing and adding messages directly from the conversation change page.
    This is a "read-only" view for quick reference.
    """
    model = Message
    extra = 0  # Don't show any extra blank forms for adding new messages
    readonly_fields = ('sender', 'message_body', 'sent_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Configuration for the Conversation model in the admin interface.
    """
    # Fields to display in the main conversation list
    list_display = ('conversation_id', 'created_at', 'display_participants')
    
    # Use the much better horizontal filter for selecting participants
    filter_horizontal = ('participants',)
    
    # Enable filtering by creation date
    list_filter = ('created_at',)
    
    # Show messages inline within the conversation detail view
    inlines = [MessageInline]

    def display_participants(self, obj):
        """
        Creates a comma-separated string of participant emails for the list display.
        """
        return ", ".join([user.email for user in obj.participants.all()])
    
    # Sets the column header name for the custom method
    display_participants.short_description = 'Participants'


# --- 3. Admin Configuration for the Message Model ---

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Configuration for the Message model in the admin interface.
    """
    # Fields to display in the message list
    list_display = ('message_id', 'sender', 'conversation', 'sent_at', 'short_body')
    
    # Make fields read-only. A message, once sent, should not be altered.
    readonly_fields = ('sender', 'conversation', 'sent_at', 'message_body')
    
    # Enable filtering
    list_filter = ('sent_at', 'sender')
    
    # Enable searching the message body
    search_fields = ('message_body',)
    
    # Default ordering, newest first
    ordering = ('-sent_at',)

    def short_body(self, obj):
        """
        Returns the first 50 characters of the message body.
        """
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    
    short_body.short_description = 'Message Preview'