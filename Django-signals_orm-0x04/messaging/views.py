from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .serializers import MessageThreadSerializer
from .models import Message


@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted successfully."}, status=HTTP_204_NO_CONTENT)
class ThreadedMessageListView(APIView):
    def get(self, request):
        messages = Message.objects.filter(parent_message__isnull=True)\
            .select_related('sender')\
                .prefetch_related(
                    'replies',
                    'replies__replies',
                    'replies__sender',
                    'replies__replies__sender'
                )
        serializer = MessageThreadSerializer(messages, many=True)
        return Response(serializer.data)