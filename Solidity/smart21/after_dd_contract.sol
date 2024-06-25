pragma solidity 0.5.0;

library SafeMath {

}

contract ERC20           {
    using SafeMath for uint256;

    mapping (address => uint256) private _balances;

    mapping (address => mapping (address => uint256)) private _allowances;

    uint256 private _totalSupply;

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

}

contract CremanonToken is ERC20{
    string public name = ""; 
    string public symbol = ""; 
    uint8 public constant decimals = 18; 
    uint256 public initialSupply = 0;

    address public owner;

    event OwnershipRenounced(address indexed previousOwner);
    event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
    );

    function transferOwnership(address _newOwner) public           {
        _transferOwnership(_newOwner);
    }

    function _transferOwnership(address _newOwner) internal {
        require(_newOwner != address(0), "Already owner");
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }

    address public crc;

    event CrcTransferred(
    address indexed previousCrc,
    address indexed newCrc
    );

    function transferCrc(address _newCrc) public           {
        require(_newCrc != address(0), "Invalid Address");
        emit CrcTransferred(crc, _newCrc);
        crc = _newCrc;
    }

    event Mint(address indexed to, uint256 amount);

    function mint(
        address _to,
        uint256 _amount
    )
      public        
      returns (bool)
    {

        emit Mint(_to, _amount);
        return true;
    }

    event Burn(address indexed burner, uint256 value);

    function burn(address _who, uint256 _value) public         returns (bool) {
        require(_value <= super.balanceOf(_who), "Balance is too small.");

        emit Burn(_who, _value);

        return true;
    }
}
