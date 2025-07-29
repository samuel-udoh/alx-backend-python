from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_204_NO_CONTENT


@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted successfully."}, status=HTTP_204_NO_CONTENT)