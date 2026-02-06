# finance_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Finance")

# Hackathon Rule: Agents must stay within these bounds [cite: 21, 39]
USER_POLICIES = {
    "monthly_limit": 5000,
    "spent_so_far": 4200,
    "allowed_merchants": ["Utility Co", "Rent Corp", "Internet Provider"]
}

@mcp.tool()
def pay_bill(merchant: str, amount: float) -> str:
    """Pays a bill only if it meets user-defined safety rules."""
    # Policy 1: Merchant Allowlist [cite: 45, 47]
    if merchant not in USER_POLICIES["allowed_merchants"]:
        return f"BLOCKED: {merchant} is not an authorized recipient."
    
    # Policy 2: Spend Caps [cite: 39, 45]
    remaining = USER_POLICIES["monthly_limit"] - USER_POLICIES["spent_so_far"]
    if amount > remaining:
        return f"BLOCKED: Amount ${amount} exceeds remaining budget of ${remaining}."

    return f"SUCCESS: Paid ${amount} to {merchant}."

if __name__ == "__main__":
    # This keeps the server running and listening for the agent [cite: 13, 21]
    mcp.run(transport='stdio')