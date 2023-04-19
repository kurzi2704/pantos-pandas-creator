# Pantos PANDAS Token Deploy - TESTNET
The following steps describe how deploy a PANDAS token in Pantos supported testnets. This step by step guide
should guide you through the world of PANDAS and brownie. 

## Table of Contents
1. [Setup all requirements and prerequisites](#1-setup-all-requirements-and-prerequisites)
2. [Add private key to brownie project](#2-add-private-key-to-brownie-project)
3. [Adapt your token settings](#3-adapt-mytokensol-in-contracts-folder)
4. [Deploy preparations](#4-adapt-deploy_tokenpy-in-scripts-folder)
5. [Deploy your token](#5-deploy-your-token)
6. [Register External Token](#6-register-external-token)
7. [Unregister External Token](#7-unregister-external-token)
8. [Unregister Token](#8-unregister-token)

## 1. Setup all requirements and prerequisites
* To be able to start with everything we need python installed. The version should be `3.6 or later`, but not greater 
than `3.9`
* _brownie_ needs to be installed next. This is done by `pip install eth-brownie` - 
there are also other ways of installing it, just visit the [docs](https://eth-brownie.readthedocs.io/en/stable/install.html#dependencies).
* If the installation of python and brownie was successfully, we should now be able to run `brownie` in our command line 
and should see something like: 
```shell
Brownie v1.19.3 - Python development framework for Ethereum

Usage:  brownie <command> [<args>...] [options <args>]

Commands:
  init               Initialize a new brownie project
  bake               Initialize from a brownie-mix template
  pm                 Install and manage external packages
  compile            Compile the contract source files
  console            Load the console
  test               Run test cases in the tests/ folder
  run                Run a script in the scripts/ folder
  accounts           Manage local accounts
  networks           Manage network settings
  gui                Load the GUI to view opcodes and test coverage
  analyze            Find security vulnerabilities using the MythX API

Options:
  --help -h          Display this message
  --version          Show version and exit

Type 'brownie <command> --help' for specific options and more information about
each command.
```

## 2. Add private key to brownie project
* If you already have a private key then use (where `<id>` is the identifier or name of your account):
```shell
brownie accounts new <id>
```

* If you do not have a private key then use (where `<id>` is the identifier or name of your account):
```shell
brownie accounts generate <id>
```

When a new account is generated the address is displayed to you, as well as the seed.

>Do not forget to get enough funds to your newly created account. This can be done by using the faucet, by entering your 
> account address.

## 3. Adapt MyToken.sol in /contracts folder
You just need to set a `_NAME` and a `_SYMBOL` you like your token to have.
```solidity
...
contract MyToken is PantosBaseToken {
    string private constant _NAME = "MyToken"; /* replace with your token name */
    string private constant _SYMBOL = "MT"; /* replace with your token symbol */
    uint8 private constant _DECIMALS = 18; 
...
```

## 4. Adapt deploy_token.py in /scripts folder
If you want another inital amount than 100 just adapt the `INITIAL_SUPPLY` constant. Also
`FORWARDER_ADDRESS`, `HUB_ADDRESS` and `PAN_ADDRESS` need to be copied from [here](https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses), 
based on the testnet you want to deploy:
```python
...
# Set initial token supply and minimum token stake
INITIAL_SUPPLY = 100 * 10 ** 18  # initial supply is 100 Token with 18 decimals
_MINIMUM_TOKEN_STAKE = 10 ** 3 * 10 ** 8

# Set the addresses for the Pantos forwarder, hub, and PAN token
FORWARDER_ADDRESS = ""
HUB_ADDRESS = ""
PAN_ADDRESS = ""
...
```

for BNB Chain and 10.000 initial supply it would look like the following: 
```python 
...
# Set initial token supply and minimum token stake
INITIAL_SUPPLY = 10000 * 10 ** 18  # initial supply is 10000 Token with 18 decimals
_MINIMUM_TOKEN_STAKE = 10 ** 3 * 10 ** 8

# Set the addresses for the Pantos forwarder, hub, and PAN token
FORWARDER_ADDRESS = "0x77aa11CfeD2bce4BE6d1f781077691DA1FcB6526"
HUB_ADDRESS = "0xc306ba335f4fcbe4178e3e033fc1a90c17e71831"
PAN_ADDRESS = "0xC892F1D09a7BEF98d65e7f9bD4642d36BC506441"
...
```

## 5 Deploy your token
### 5.1 Checking our networks
Before we start the deploy we should check our brownie networks by running: 
```shell 
brownie networks list
```

this should give us a list of all networks registered in brownie : 

```shell 
...
Binance Smart Chain
  ├─Testnet: bsc-test
  └─Mainnet: bsc-main
...
```

If you are not able to find the network you are searching for, you probably need to import it. Following
that [Guide](https://eth-brownie.readthedocs.io/en/stable/network-management.html#adding-a-new-network) helps you by doing that. 
### 5.2 Deploy
After choosing a network and checking if enough funds are available, we can create our first token with the following 
command, where `<name of account>` should be replaced by your brownie account id from step 2 and `<network name>` is the 
id of the desired network (ie. bsc-test for bsc testnet): 
```shell 
brownie run ./scripts/deploy_token.py deploy_token <name of account> --network <network name>
```

You will be asked for a password, which you have set for your account in step 2 and then, if everything worked as 
expected you should see something like the following:

```shell
pandas-creator % brownie run ./scripts/deploy_token.py deploy_token accountId --network avalanche-fuji
Brownie v1.19.3 - Python development framework for Ethereum

PandasCreatorProject is the active project.

Running 'scripts/deploy_token.py::deploy_token'...
Enter password for "accountId": 
Transaction sent: 0xaf09406b8b75bf81545b1c9b08fb9fcea6d7a537e3a1a125023b11330e2f7fc9
  Gas price: 25.0 gwei   Gas limit: 1236507   Nonce: 17
  MyToken.constructor confirmed   Block: 21046119   Gas used: 1124098 (90.91%)
  MyToken deployed at: 0x2FE768060c4788122Cd3A65f1ac91CDEA0f0b8C9

Transaction sent: 0x8432dec436c8f896ddb55168d75b4ebee2d402eb6692ebf236d01c1fa9bb39d3
  Gas price: 25.0 gwei   Gas limit: 52055   Nonce: 18
  MyToken.setPantosForwarder confirmed   Block: 21046120   Gas used: 47323 (90.91%)

Transaction sent: 0xce76880dfb9374bd15df37db1daff04842ccabc7873c740e5c906e25f975becd
  Gas price: 25.0 gwei   Gas limit: 50894   Nonce: 19
  PantosToken.approve confirmed   Block: 21046123   Gas used: 46268 (90.91%)

Transaction sent: 0x32397ecedd370ca1c2d7d67317ab0907626c3e80fbc61d1653ccd51fd0acd7af
  Gas price: 25.0 gwei   Gas limit: 157894   Nonce: 20
  PantosHub.registerToken confirmed   Block: 21046124   Gas used: 141787 (89.80%)
```

## 6. Register External Token
If we have deployed our token on 2 or more chains, then we need to tell the Pantos hub how the token should be mapped. 
Ie. we have our token deployed on 3 chains: `Avalanche`, `BSC` and `FTM`. Now we need to tell the hub of each of those 
chains the address of the token on the other chains, in our example we would need to call 2 registerExternalToken events
on each chain. 
### 6.1 File adaptions
To perform one registration we need to change the following in our `scripts/register_external_tokens.py` file: 
* Add the `HUB_ADDRESS` of our current hub, which can be found [here](https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses) again.
* We need to insert our data 
  * `<address of token on chain>` = the address of token on current chain (the chain where the hub is located)
  * `<chain_id>` = ID of destination chain (0 = ETH, 1 = BSC, 3 = Avalanche, 5 = Polygon, 6 = Cronos, 7 = Fantom, 8 = Celo) 
  * `<address of token on different chain>` = the address of the token of the destination chain.
```python 
hub.registerExternalToken('<address of token on chain>', '<chain id>', '<address of token on different chain>'.encode('utf-8').strip(),
            {'from': account}
    )
```
### 6.2 run registration
To run the registration we need to run the following command, where `<name of account>` should be replaced by your 
brownie account id from step 2 and `<network name>` is the id of the desired network (ie. bsc-test for bsc testnet):
```shell 
brownie run ./scripts/register_external_tokens.py register_token <name of account> --network <network name>
```

You will be asked for a password, which you have set for your account in step 2 and then, if everything worked as 
expected you should see something like the following:

```shell 
Brownie v1.19.3 - Python development framework for Ethereum

PantosPandasCreatorProject is the active project.

Running 'scripts/register_external_tokens.py::register_token'...
Enter password for "accountId": 
Transaction sent: 0x42486b717067b5cdaa6487625248fef851461998f5a70687fb3af933d9c16912
  Gas price: 25.0 gwei   Gas limit: 160167   Nonce: 27
  PantosHub.registerExternalToken confirmed   Block: 21063179   Gas used: 143838 (89.81%)
```

## 7. Unregister External Token
Sometimes we need to unregister an external token, for example to register a new one. Therefore
we can use `unregisterExternalToken`

### 7.1 File adaptions
To unregister an external token we need to change the following in our `scripts/unregister_external_tokens.py` file: 
* Add the `HUB_ADDRESS` of our current hub, which can be found [here](https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses) again.
* We need to insert our data 
  * `<address of token on chain>` = the address of token on current chain (the chain where the hub is located)
  * `<chain_id>` = ID of destination chain (0 = ETH, 1 = BSC, 3 = Avalanche, 5 = Polygon, 6 = Cronos, 7 = Fantom, 8 = Celo) 

### 7.2 revert external registration
To run the external registration revert we need to run the following command, where `<name of account>` should be replaced by your 
brownie account id from step 2 and `<network name>` is the id of the desired network (ie. bsc-test for bsc testnet):
```shell 
brownie run ./scripts/unregister_external_tokens.py unregister_external_token <name of account> --network <network name>
```

You will be asked for a password, which you have set for your account in step 2 and then, if everything worked as 
expected you should see something like the following:

```shell 
Brownie v1.19.3 - Python development framework for Ethereum

PantosPandasCreatorProject is the active project.

Running 'scripts/unregister_external_tokens.py::unregister_external_token'...
Enter password for "accountId": 
Transaction sent: 0xf62fffeca9b7d9c0ba16b507e35ea2a770047e9f37ef9ccdf54e7d904a9d26cb
  Gas price: 25.0 gwei   Gas limit: 52895   Nonce: 28
  PantosHub.unregisterExternalToken confirmed   Block: 21063498   Gas used: 47825 (90.41%)
```

## 8. Unregister Token 
Sometimes we want to unregister a token, which, if run through successfully unlocks the PAN we used for registering. 

### 8.1 File adaptions
To unregister a token we need to change the following in our `scripts/unregister_token.py` file: 
* Add the `HUB_ADDRESS` of our current hub, which can be found [here](https://pantos.gitbook.io/technical-documentation/general/deploying-token#overview-of-pantos-blockchain-ids-and-contract-addresses) again.
* Add the `TOKEN_ADDRESS` of the token you want to unregister. 

### 8.2 revert external registration
To run the registration revert we need to run the following command, where `<name of account>` should be replaced by your 
brownie account id from step 2 and `<network name>` is the id of the desired network (ie. bsc-test for bsc testnet):
```shell 
brownie run ./scripts/unregister_token.py unregister_toke <name of account> --network <network name>
```

You will be asked for a password, which you have set for your account in step 2 and then, if everything worked as 
expected you should see something like the following:

```shell 
Brownie v1.19.3 - Python development framework for Ethereum

PantosPandasCreatorProject is the active project.

Running 'scripts/unregister_token.py::unregister_token'...
Enter password for "accountId": 
Transaction sent: 0x26d7ecea2e5dd52849ea41109820775458701fce6f93b37b63e19f917c9c52dc
  Gas price: 25.0 gwei   Gas limit: 176695   Nonce: 26
  PantosHub.unregisterToken confirmed   Block: 21063039   Gas used: 158609 (89.76%)
```