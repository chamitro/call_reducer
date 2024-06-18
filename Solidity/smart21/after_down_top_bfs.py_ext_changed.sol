pragma solidity 0.5.0;

interface IERC20 {

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

library SafeMath {

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {

        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");

        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {

        require(b > 0, "SafeMath: division by zero");
        uint256 c = a / b;

        return c;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0, "SafeMath: modulo by zero");
        return a % b;
    }
}

contract ERC20 is IERC20 {
    using SafeMath for uint256;

    mapping (address => uint256) private _balances;

    mapping (address => mapping (address => uint256)) private _allowances;

    uint256 private _totalSupply;

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) public returns (bool) {

        return true;
    }

    function approve(address spender, uint256 value) public returns (bool) {

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {

        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {

        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {

        return true;
    }

    function _burnFrom(address account, uint256 amount) internal {

    }
}

contract CremanonToken is ERC20 {
    string public name = ""; 
    string public symbol = ""; 
    uint8 public constant decimals = 18; 
    uint256 public initialSupply = 0;

    constructor(string memory _name, string memory _symbol, uint256 _initialSupply) public {
        name = _name;
        symbol = _symbol;
        initialSupply = _initialSupply * 10**uint256(decimals);

        owner = msg.sender;
    }

    address public owner;

    event OwnershipRenounced(address indexed previousOwner);
    event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
    );

    function renounceOwnership() public           {
        emit OwnershipRenounced(owner);
        owner = address(0);
    }

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
