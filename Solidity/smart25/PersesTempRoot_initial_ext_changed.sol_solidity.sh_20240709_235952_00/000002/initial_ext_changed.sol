pragma solidity ^0.4.23;
contract Ownable {
    address ownerCEO;
    address ownerMoney;
    address privAddress;
    address addressAdmixture;
    function transferOwnership(address add) public           {
        if (add != address(0)) {
            ownerCEO = add;
        }
    }
    function transferOwnerMoney(address _ownerMoney) public            {
        if (_ownerMoney != address(0)) {
            ownerMoney = _ownerMoney;
        }
    }
}
contract Whitelist is Ownable{
    mapping(address => bool) public whitelist;
    mapping(uint  => address)   whitelistCheck;
    uint public countAddress = 0;
    event WhitelistedAddressAdded(address addr);
    event WhitelistedAddressRemoved(address addr);
    function addAddressToWhitelist(address addr)                 public returns(bool success) {
        if (!whitelist[addr]) {
            whitelist[addr] = true;
            countAddress = countAddress + 1;
            whitelistCheck[countAddress] = addr;
            emit WhitelistedAddressAdded(addr);
            success = true;
        }
    }
    function getWhitelistCheck(uint key)                 view public returns(address) {
        return whitelistCheck[key];
    }
    function getInWhitelist(address addr) public view returns(bool) {
        return whitelist[addr];
    }
}
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
