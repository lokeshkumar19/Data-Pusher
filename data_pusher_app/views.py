from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests
import json
import logging

logger = logging.getLogger(__name__)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def receive_data(request):
    try:
        token = request.headers.get('CL-X-TOKEN')
        if not token:
            return Response({'error': 'Un Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        account = Account.objects.get(app_secret_token=token)

        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                # Validate data here (e.g., using jsonschema)
                # ...
                data = request.data

                for destination in Destination.objects.filter(account=account):
                    if destination.http_method == 'GET':
                        url = f"{destination.url}?{urlencode(data)}" 
                        response = requests.get(url)
                    else:
                        response = requests.request(
                            destination.http_method,
                            destination.url,
                            json=data,
                            headers=destination.headers
                        )

                    # Handle response from destination (e.g., log status, errors)
                    logger.info(f"Response from {destination.url}: {response.status_code}")

                    if not response.ok:
                        logger.error(f"Error sending data to {destination.url}: {response.text}")

                return Response({'message': 'Data sent successfully'}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.exception("Error processing data:")
                return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

    except Account.DoesNotExist:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)
# Other views for Account and Destination CRUD operations