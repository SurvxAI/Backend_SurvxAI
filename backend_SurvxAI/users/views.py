from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from users.models import User
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.send_activation_email()
        return Response({
            'user': serializer.data,
            'message': 'User created and activation mail was sended successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def activate_account(request):
    email = request.data.get('email')
    code = request.data.get('code')

    try:
        user = User.objects.get(email=email)

        # Vérification du délai d'expiration (30 minutes)
        if user.activation_code_created and \
           timezone.now() > user.activation_code_created + timedelta(minutes=30):
            return Response({
                'message': 'Le code d\'activation a expiré. Veuillez en demander un nouveau.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if user.activation_code == code:
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({
                'message': 'Votre compte a été activé avec succès.'
            })
        else:
            return Response({
                'message': 'Code d\'activation invalide.'
            }, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({
            'message': 'Utilisateur non trouvé.'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def resend_activation_code(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email, is_active=False)
        user.send_activation_email()
        return Response({
            'message': 'Un nouveau code d\'activation a été envoyé.'
        })
    except User.DoesNotExist:
        return Response({
            'message': 'Utilisateur non trouvé ou déjà activé.'
        }, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # add to the blacklist
            return Response({"message": "logout successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)
