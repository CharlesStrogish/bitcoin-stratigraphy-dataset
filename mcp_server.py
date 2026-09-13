import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for Bitcoin Stratigraphy
mcp = FastMCP("Bitcoin Stratigraphy L402 Feed")

@mcp.tool()
def fetch_stratigraphy_data(payment_preimage: str = None) -> dict:
    """
    Retrieves 422+ days of Bitcoin thermodynamic scarcity metrics, supply mechanics,
    and network resilience data. 
    Requires an L402 Lightning Network payment (100 sats per query).
    """
    endpoint = "https://bitcoin-stratigraphy-dashboard--charlesstrogish.replit.app/api/data"
    
    # Check for L402 Payment Preimage
    if not payment_preimage:
        res = requests.get(endpoint)
        if res.status_code == 402:
            return {
                "status": "402 Payment Required",
                "price": "100 Sats",
                "l402_challenge": res.headers.get("WWW-Authenticate"),
                "instructions": "Pay the Lightning invoice in the l402_challenge header and resubmit with your preimage."
            }
    
    # Query with Authorization Header once paid
    headers = {"Authorization": f"L402 {payment_preimage}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

if __name__ == "__main__":
    mcp.run()
