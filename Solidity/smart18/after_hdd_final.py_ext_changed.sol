

pragma solidity 0.5.0;

interface IERC165 {

}

pragma solidity 0.5.0;

contract IERC721 is IERC165 {

  event Transfer(
    address indexed from,
    address indexed to,
    uint256 indexed tokenId
  );
  event Approval(
    address indexed owner,
    address indexed approved,
    uint256 indexed tokenId
  );
  event ApprovalForAll(
    address indexed owner,
    address indexed operator,
    bool approved
  );

  function transferFrom(address from, address to, uint256 tokenId) public;

}

pragma solidity 0.5.0;

contract IERC721Enumerable is IERC721 {

}

pragma solidity 0.5.0;

contract IERC721Receiver {

}

pragma solidity 0.5.0;

library SafeMath {

}

pragma solidity 0.5.0;

library Address {

}

pragma solidity 0.5.0;

contract ERC165 is IERC165 {

  bytes4 private constant _InterfaceId_ERC165 = 0x01ffc9a7;

  mapping(bytes4 => bool) internal _supportedInterfaces;

}

pragma solidity 0.5.0;

contract ERC721 is ERC165, IERC721 {

  using SafeMath for uint256;
  using Address for address;

  bytes4 private constant _ERC721_RECEIVED = 0x150b7a02;

  mapping (uint256 => address) private _tokenOwner;

  mapping (uint256 => address) private _tokenApprovals;

  mapping (address => uint256) private _ownedTokensCount;

  mapping (address => mapping (address => bool)) private _operatorApprovals;

  bytes4 private constant _InterfaceId_ERC721 = 0x80ac58cd;

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
    require(_tokenOwner[tokenId] == address(0));
    _tokenOwner[tokenId] = to;
    _ownedTokensCount[to]                               ;
  }

}

pragma solidity 0.5.0;

contract ERC721Enumerable is ERC165, ERC721, IERC721Enumerable {

  mapping(address => uint256[]) private _ownedTokens;

  mapping(uint256 => uint256) private _ownedTokensIndex;

  uint256[] private _allTokens;

  mapping(uint256 => uint256) private _allTokensIndex;

  bytes4 private constant _InterfaceId_ERC721Enumerable = 0x780e9d63;

  function _addTokenTo(address to, uint256 tokenId) internal {
    super._addTokenTo(to, tokenId);
    uint256 length = _ownedTokens[to].length;
    _ownedTokens[to].push(tokenId);
    _ownedTokensIndex[tokenId] = length;
  }

}

pragma solidity 0.5.0;

contract IERC721Metadata is IERC721 {

}

pragma solidity 0.5.0;

contract NametagToken  is ERC721Enumerable, IERC721Metadata {

  string internal _name = 'NametagToken';

  string internal _symbol = 'NTT';

  mapping(uint256 => string) private _tokenURIs;
  mapping(uint256 => address) private reservedTokenId;

    bytes4 private constant InterfaceId_ERC721Metadata = 0x5b5e139f;

}
