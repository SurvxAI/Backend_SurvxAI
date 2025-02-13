# test_xrpl.py
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests import AccountInfo
from xrpl.utils import str_to_hex


def test_xrpl_connection():
    try:
        #  testnet Connexion
        client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

        # Create wallet test
        test_wallet = generate_faucet_wallet(client, debug=True)

        print("Wallet créé avec succès!")
        print(f"Adresse classique: {test_wallet.classic_address}")
        print(f"Clé privée: {test_wallet.private_key}")
        print(f"Seed: {test_wallet.seed}")

        # Retrieves informations account
        acct_info = AccountInfo(
            account=test_wallet.classic_address,
            ledger_index="validated",
            strict=True,
        )

        response = client.request(acct_info)
        print("\nInformations du compte:", response.result)

        return True

    except Exception as e:
        print(f"Erreur lors du test: {str(e)}")
        return False


if __name__ == "__main__":
    test_xrpl_connection()
