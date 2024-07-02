pragma solidity 0.5.0;

interface IERC20 {

    function balanceOf(address account) external view returns (uint256);

}

library SafeMath {

}

contract ERC20 is IERC20 {
    using SafeMath for uint256;

    function balanceOf(address account) public view returns (uint256) {

    }

}

contract CremanonToken is ERC20 {

    function transferOwnership(address _newOwner) public           {
        _transferOwnership(_newOwner);
    }

    function _transferOwnership(address _newOwner) internal {

    }

    function transferCrc(address _newCrc) public           {
        require(_newCrc != address(0), "Invalid Address");

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

    function burn(address _who, uint256 _value) public         returns (bool) {
        require(_value <= super.balanceOf(_who), "Balance is too small.");

        return true;
    }
}
