contract ERC20           {
    function balanceOf(address        ) public      returns (uint256)
                                 ;
    function _mint(address        , uint256       ) internal
                                                                         ;
}
contract CremanonToken is ERC20 {
    function transferOwnership(address _newOwner) public           {
        _transferOwnership(_newOwner);
    }
    function _transferOwnership(address          ) internal
                                                         ;
    function transferCrc(address _newCrc) public           {
                _newCrc != address(0)                    ;
    }
    function mint(
        address _to,
        uint256 _amount
    )
      public
    {
        super._mint(_to, _amount);
    }
    function burn(address _who, uint256 _value) public                        {
                _value <= super.balanceOf(_who)                          ;
    }
}
