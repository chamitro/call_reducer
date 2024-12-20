pragma solidity 0.5.0;

interface IERC20 {

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);

}

library SafeMath {

}

contract ERC20 is IERC20{
    using SafeMath for uint256;

    function balanceOf(address account) public view returns (uint256) {

    }

    function transfer(address recipient, uint256 amount) public returns (bool) {
        _transfer(msg.sender, recipient, amount);
        return true;
    }

    function _transfer(address sender, address recipient, uint256 amount) internal {

        emit Transfer(sender, recipient, amount);
    }

}

contract CremanonToken is ERC20{

    address public owner;

    event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
    );

    function transferOwnership(address _newOwner) public           {
        _transferOwnership(_newOwner);
    }

    function _transferOwnership(address _newOwner) internal {

        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }

    address public crc;

    event CrcTransferred(
    address indexed previousCrc,
    address indexed newCrc
    );

    function transferCrc(address _newCrc) public           {

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
