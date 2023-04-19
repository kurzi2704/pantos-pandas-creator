// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <0.9.0;
pragma abicoder v2;

import "./PantosBaseToken.sol";
/**
 * @title Pantos-compatible Example Token
 */
contract MyToken is PantosBaseToken {
    string private constant _NAME = "MyToken";
    string private constant _SYMBOL = "MT";
    uint8 private constant _DECIMALS = 18;

    /// @dev msg.sender receives all existing tokens.
    constructor(uint256 initialSupply)
        PantosBaseToken(_NAME, _SYMBOL, _DECIMALS)
    {
        ERC20._mint(msg.sender, initialSupply);
        // Contract is paused until it is fully initialized
    }
    /// @dev See {PantosBaseToken-_setPantosForwarder}.
    function setPantosForwarder(address pantosForwarder)
        external
        onlyOwner
    {
        _setPantosForwarder(pantosForwarder);
    }
}