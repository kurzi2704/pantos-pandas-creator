import brownie
import json

from brownie import MyToken

# Set initial token supply and minimum token stake
INITIAL_SUPPLY = 100 * 10 ** 18  # initial supply is 100 Token with 18 decimals
_MINIMUM_TOKEN_STAKE = 10 ** 3 * 10 ** 8

# Set the addresses for the Pantos forwarder, hub, and PAN token
# can be found here: https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses
FORWARDER_ADDRESS = ""
HUB_ADDRESS = ""
PAN_ADDRESS = ""


# Define the deployToken function
def deploy_token(account_name: str):
    # loading Pantos Hub abi data
    with open('./abi/pantos_hub_abi.json', 'r') as f:
        pantos_hub_abi_data = json.loads(f.read())

    # loading Pantos Token abi data
    with open('./abi/pantos_token_abi.json', 'r') as f:
        pantos_token_abi_data = json.loads(f.read())

    # Load the PantosHub contract from the ABI
    hub = brownie.Contract.from_abi("PantosHub", HUB_ADDRESS,
                                    pantos_hub_abi_data['abi'])

    # Load the PantosToken contract from the ABI
    pan_token = brownie.Contract.from_abi("PantosToken", PAN_ADDRESS,
                                          pantos_token_abi_data['abi'])

    # Load the specified account
    account = brownie.accounts.load(account_name)

    # Deploy the custom token contract
    myTokenContract = MyToken.deploy(INITIAL_SUPPLY, {'from': account})

    # Set the Pantos forwarder address in the custom token contract
    myTokenContract.setPantosForwarder(FORWARDER_ADDRESS,
                                       {'from': account})

    # Approve the PantosHub to spend the required minimum token stake
    pan_token.approve(HUB_ADDRESS, _MINIMUM_TOKEN_STAKE, {'from': account})

    # Register the custom token on the PantosHub
    hub.registerToken(myTokenContract.address, _MINIMUM_TOKEN_STAKE,
                      {'from': account})
