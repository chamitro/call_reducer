contract Ownable {
    address         _pendingOwner;
    function transferOwnership(address _newOwner) public           {
        _pendingOwner = _newOwner;
    }
}
