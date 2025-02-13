from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient


class WalletService:
    @staticmethod
    def create_xrp_wallet():
        # Connexion to  XRP client
        client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
        # wallet creation
        wallet = generate_faucet_wallet(client, debug=True)
        return {
            'address': wallet.classic_address,
            'seed': wallet.seed,
            'private_key': wallet.private_key
        }

    @staticmethod
    def validate_wallet_address(address):
        # Basic validation of the format of an XRP address
        if not address.startswith('r'):
            return False
        if len(address) < 25 or len(address) > 35:
            return False
        return True
