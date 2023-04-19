import brownie
import json

from brownie import MyToken

# Set the addresses for the Pantos forwarder, hub, and PAN token
# can be found here: https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses
HUB_ADDRESS = ""

# this is the token address you want to unregister
TOKEN_ADDRESS = ""

# Define the deployToken function
def unregister_token(account_name: str):
    # loading Pantos Hub abi data
    with open('./abi/pantos_hub_abi.json', 'r') as f:
        pantos_hub_abi_data = json.loads(f.read())

    # Load the PantosHub contract from the ABI
    hub = brownie.Contract.from_abi("PantosHub", HUB_ADDRESS,
                                    pantos_hub_abi_data['abi'])

    account = brownie.accounts.load(account_name)

    # unregister the custom token on the PantosHub
    hub.unregisterToken(TOKEN_ADDRESS,
                      {'from': account})
