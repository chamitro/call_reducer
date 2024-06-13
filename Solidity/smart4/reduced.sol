pragma solidity ^0.4.21;
// ----------------------------------------------------------------------------
// NRM token main contract
//
// Symbol       : NRM
// Name         : Neuromachine
// Total supply : 4.958.333.333,000000000000000000 (burnable)
// Decimals     : 18
// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------
// Safe math
// ----------------------------------------------------------------------------
library SafeMath {
}
// ----------------------------------------------------------------------------
// ERC Token Standard #20 Interface
// https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20-token-standard.md
// ----------------------------------------------------------------------------
contract ERC20Interface {
}
// ----------------------------------------------------------------------------
// Contract function to receive approval and execute function in one call
// ----------------------------------------------------------------------------
contract ApproveAndCallFallBack {
    function receiveApproval(address , uint256 , address , bytes ) public;
}
// ----------------------------------------------------------------------------
// Owned contract
// ----------------------------------------------------------------------------
contract Owned {
    modifier onlyOwner {
        _;
    }
}
// ----------------------------------------------------------------------------
// NRM ERC20 Token - Neuromachine token contract
// ----------------------------------------------------------------------------
contract NRM is ERC20Interface, Owned {
    using SafeMath for uint;
    // ------------------------------------------------------------------------
    // Contract init. Set symbol, name, decimals and initial fixed supply
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Team and tokens unfreeze after 365 days from contract deploy
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Start-stop contract functions:
    // transfer, approve, transferFrom, approveAndCall
    // ------------------------------------------------------------------------
    modifier isRunnning {
        _;
    }
    // ------------------------------------------------------------------------
    // Total supply
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Get the token balance for account `tokenOwner`
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Transfer the balance from token owner's account to `to` account
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Token owner can approve for `spender` to transferFrom(...) `tokens`
    // from the token owner's account
    //
    // https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20-token-standard.md
    // recommends that there are no checks for the approval double-spend attack
    // as this should be implemented in user interfaces 
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Transfer `tokens` from the `from` account to the `to` account
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Returns the amount of tokens approved by the owner that can be
    // transferred to the spender's account
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Token owner can approve for `spender` to transferFrom(...) `tokens`
    // from the token owner's account. The `spender` contract function
    // `receiveApproval(...)` is then executed
    // ------------------------------------------------------------------------
    function approveAndCall(address , uint , bytes ) public isRunnning returns (bool ) {
    }
    // ------------------------------------------------------------------------
    // Owner can transfer out any accidentally sent ERC20 tokens
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Tokens burn
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Tokens multisend from owner only by owner
    // ------------------------------------------------------------------------
    function multisend(address[] , uint256[] ) public onlyOwner returns (uint256) {
    }
}
