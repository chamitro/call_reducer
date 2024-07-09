

pragma solidity 0.5.0;

pragma solidity 0.5.0;

contract IERC721{

  event Transfer(
    address indexed from,
    address indexed to,
    uint256 indexed tokenId
  );

  function transferFrom(address from, address to, uint256 tokenId) public;

}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

library SafeMath {

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

pragma solidity 0.5.0;

library Address {

}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

contract ERC721 is IERC721{

  using SafeMath for uint256;
  using Address for address;

  function transferFrom(
    address from,
    address to,
    uint256 tokenId
  )
    public
  {

    require(to != address(0));

    _addTokenTo(to, tokenId);

    emit Transfer(from, to, tokenId);
  }

  function _addTokenTo(address to, uint256 tokenId) internal {

  }

}

pragma solidity 0.5.0;

contract ERC721Enumerable is ERC721{

  mapping(address => uint256[]) private _ownedTokens;

  function _addTokenTo(address to, uint256 tokenId) internal {
    super._addTokenTo(to, tokenId);
    uint256 length = _ownedTokens[to].length;
    _ownedTokens[to].push(tokenId);

  }

}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

