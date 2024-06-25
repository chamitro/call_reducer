

pragma solidity 0.5.0;

contract Ownable {

    address private _owner;
    address private _pendingOwner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

contract PingAnToken is Ownable{

    bool private initialized = true;

    function initialize(address _owner) public {
        require(!initialized, "already initialized");
        require(_owner != address(0), "Cannot initialize the owner to zero address");

        initialized = true;
    }

}
