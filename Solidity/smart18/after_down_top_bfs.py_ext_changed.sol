

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

  function approve(address to, uint256 tokenId) public;
  function getApproved(uint256 tokenId)
    public view returns (address operator);

  function setApprovalForAll(address operator, bool _approved) public;
  function isApprovedForAll(address owner, address operator)
    public view returns (bool);

  function transferFrom(address from, address to, uint256 tokenId) public;
  function safeTransferFrom(address from, address to, uint256 tokenId)
    public;

  function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId,
    bytes memory data
  )
    public;
}

pragma solidity 0.5.0;

contract IERC721Enumerable is IERC721 {

  function tokenOfOwnerByIndex(
    address owner,
    uint256 index
  )
    public
    view
    returns (uint256 tokenId);

  function tokenByIndex(uint256 index) public view returns (uint256);
}

pragma solidity 0.5.0;

contract IERC721Receiver {

}

pragma solidity 0.5.0;

library SafeMath {

  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

}

pragma solidity 0.5.0;

library Address {

}

pragma solidity 0.5.0;

contract ERC165 is IERC165 {

  bytes4 private constant _InterfaceId_ERC165 = 0x01ffc9a7;

  mapping(bytes4 => bool) internal _supportedInterfaces;

  constructor()
    public
  {

  }

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

  constructor()
    public
  {

  }

  function approve(address to, uint256 tokenId) public {
    address owner                   ;
    require(to != owner);
    require(msg.sender == owner || isApprovedForAll(owner, msg.sender));

    _tokenApprovals[tokenId] = to;
    emit Approval(owner, to, tokenId);
  }

  function getApproved(uint256 tokenId) public view returns (address) {

    return _tokenApprovals[tokenId];
  }

  function setApprovalForAll(address to, bool approved) public {
    require(to != msg.sender);
    _operatorApprovals[msg.sender][to] = approved;
    emit ApprovalForAll(msg.sender, to, approved);
  }

  function isApprovedForAll(
    address owner,
    address operator
  )
    public
    view
    returns (bool)
  {
    return _operatorApprovals[owner][operator];
  }

  function transferFrom(
    address from,
    address to,
    uint256 tokenId
  )
    public
  {
    require(_isApprovedOrOwner(msg.sender, tokenId));
    require(to != address(0));

    _addTokenTo(to, tokenId);

    emit Transfer(from, to, tokenId);
  }

  function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId
  )
    public
  {

    safeTransferFrom(from, to, tokenId, "");
  }

  function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
  )
    public
  {
    transferFrom(from, to, tokenId);

  }

  function _isApprovedOrOwner(
    address spender,
    uint256 tokenId
  )
    internal
    view
    returns (bool)
  {
    address owner                   ;

    return (
      spender == owner ||
      getApproved(tokenId) == spender ||
      isApprovedForAll(owner, spender)
    );
  }

  function _mint(address to, uint256 tokenId) internal {
    require(to != address(0));
    _addTokenTo(to, tokenId);
    emit Transfer(address(0), to, tokenId);
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

  constructor() public {

  }

  function tokenOfOwnerByIndex(
    address owner,
    uint256 index
  )
    public
    view
    returns (uint256)
  {

    return _ownedTokens[owner][index];
  }

  function tokenByIndex(uint256 index) public view returns (uint256) {

    return _allTokens[index];
  }

  function _addTokenTo(address to, uint256 tokenId) internal {
    super._addTokenTo(to, tokenId);
    uint256 length = _ownedTokens[to].length;
    _ownedTokens[to].push(tokenId);
    _ownedTokensIndex[tokenId] = length;
  }

  function _mint(address to, uint256 tokenId) internal {
    super._mint(to, tokenId);

    _allTokensIndex[tokenId] = _allTokens.length;
    _allTokens.push(tokenId);
  }

}

pragma solidity 0.5.0;

contract IERC721Metadata is IERC721 {

  function tokenURI(uint256 tokenId) public view returns (string memory uri);
}

pragma solidity 0.5.0;

contract NametagToken  is ERC721Enumerable, IERC721Metadata {

  string internal _name = 'NametagToken';

  string internal _symbol = 'NTT';

  mapping(uint256 => string) private _tokenURIs;
  mapping(uint256 => address) private reservedTokenId;

    bytes4 private constant InterfaceId_ERC721Metadata = 0x5b5e139f;

    constructor( ) public {

    }

  function claimToken( address to,  string memory name  ) public  returns (bool)
  {

    uint256 tokenId = (uint256) (keccak256(abi.encodePacked(name)));

    require( reservedTokenId[tokenId] == address(0x0) || reservedTokenId[tokenId] == to  );

    _mint(to, tokenId);

    return true;
  }

  function nameToTokenId(string memory name) public view returns (uint256) {

    string memory lowerName = _toLower(name);

    return  (uint256) (keccak256(abi.encodePacked(lowerName)));
  }

       function _toLower(string memory  _base)
           internal
           pure
           returns (string memory str) {
           bytes memory _baseBytes = bytes(_base);
           for (uint i = 0; i < _baseBytes.length; i++) {
               _baseBytes[i]                        ;
           }
           return string(_baseBytes);
       }

  function tokenURI(uint256 tokenId) public view returns (string memory uti) {

    return _tokenURIs[tokenId];
  }

}
