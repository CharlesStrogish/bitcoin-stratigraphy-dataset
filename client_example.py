import requests

class BitcoinStratigraphyClient:
    """
    A lightweight Python client for querying the Bitcoin Stratigraphy L402 Data Feed.
    Supports standard HTTP requests and L402 Lightning Network authorization preimages.
    """
    def __init__(self, endpoint="https://bitcoin-stratigraphy-dashboard--charlesstrogish.replit.app/api/data"):
        self.endpoint = endpoint

    def fetch_data(self, payment_preimage: str = None) -> dict:
        """
        Fetches the complete 422+ day dataset.
        If no payment_preimage is supplied, returns the 402 challenge with the Lightning invoice.
        """
        headers = {}
        if payment_preimage:
            headers["Authorization"] = f"L402 {payment_preimage}"

        response = requests.get(self.endpoint, headers=headers)

        # 402 Payment Required: Returns challenge details & invoice
        if response.status_code == 402:
            print("⚡ 402 Payment Required!")
            print("L402 Challenge:", response.headers.get("WWW-Authenticate"))
            try:
                data = response.json()
                print("Invoice:", data.get("invoice"))
            except Exception:
                pass
            return None

        # 200 OK: Data payload returned
        if response.status_code == 200:
            return response.json()

        response.raise_for_error()

# ==========================================
# EXAMPLE USAGE FOR AI AGENTS & DEVELOPERS:
# ==========================================
if __name__ == "__main__":
    client = BitcoinStratigraphyClient()
    
    # 1. First Call: Trigger the 402 challenge to retrieve the 100-sat invoice
    print("--- Attempting initial unauthenticated query ---")
    client.fetch_data()
    
    # 2. Second Call: Supply settled preimage after Lightning payment
    # data = client.fetch_data(payment_preimage="YOUR_SETTLED_LIGHTNING_PREIMAGE_HEX")
    # print("Retrieved Dataset:", data)
