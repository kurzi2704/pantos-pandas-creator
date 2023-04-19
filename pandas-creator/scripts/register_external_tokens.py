import brownie
import json

# can be found here: https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses
HUB_ADDRESS = ""

def register_token(account_name: str):
    with open('./abi/pantos_hub_abi.json', 'r') as f:
        pantos_hub_abi_data = json.loads(f.read())
    # Load the PantosHub contract from the ABI
    hub = brownie.Contract.from_abi("PantosHub", HUB_ADDRESS,
                                    pantos_hub_abi_data['abi'])

    # Load the specified account
    account = brownie.accounts.load(account_name)

    # Call the registerExternalToken function from the PantosHub contract
    # Replace the placeholders with the correct data:
    # - <address of token on chain>: the address of your token on the current chain
    # - <chain id>: the ID of the blockchain where the external token is located
    # - <address of token on different chain>: the address of your token on the external chain
    hub.registerExternalToken('<address of token on chain>', '<chain id>', '<address of token on different chain>'.encode('utf-8').strip(),
            {'from': account}
    )
