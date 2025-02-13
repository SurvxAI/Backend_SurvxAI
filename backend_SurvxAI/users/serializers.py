from rest_framework import serializers
from .models import User
from .services import WalletService


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    wallet_address = serializers.CharField(
        required=False)  # Optional if  automatic creation
    create_wallet = serializers.BooleanField(
        write_only=True, required=False, default=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'password_confirm', 'wallet_address', 'create_wallet')

    def validate(self, data):
        if data.get('create_wallet') and data.get('wallet_address'):
            raise serializers.ValidationError(
                "You cannot provide a wallet address and request wallet creation at the same time"
            )
        if not data.get('create_wallet') and not data.get('wallet_address'):
            raise serializers.ValidationError(
                "You must either provide a wallet address or request the creation of a new wallet"
            )
        if data.get('wallet_address') and not WalletService.validate_wallet_address(data['wallet_address']):
            raise serializers.ValidationError(
                "The wallet address is not valid"
            )
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                "Passwords do not match"
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        create_wallet = validated_data.pop('create_wallet', False)

        if create_wallet:
            # Automatic wallet creation
            wallet_info = WalletService.create_xrp_wallet()
            validated_data['wallet_address'] = wallet_info['address']
            # Securely store or email sensitive information
            # wallet_info['seed'] and wallet_info['private_key']

        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            wallet_address=validated_data['wallet_address'],
            profile_type='standard'
        )

        return user
