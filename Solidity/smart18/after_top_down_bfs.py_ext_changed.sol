

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

  function ownerOf(uint256 tokenId) public view returns (address owner);

  function getApproved(uint256 tokenId)
    public view returns (address operator);

  function isApprovedForAll(address owner, address operator)
    public view returns (bool);

  function transferFrom(address from, address to, uint256 tokenId) public;

}

pragma solidity 0.5.0;

contract IERC721Enumerable is IERC721 {
  function totalSupply() public view returns (uint256);

}

pragma solidity 0.5.0;

contract IERC721Receiver {

  function onERC721Received(
    address operator,
    address from,
    uint256 tokenId,
    bytes memory data
  )
    public
    returns(bytes4);
}

pragma solidity 0.5.0;

library SafeMath {

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

pragma solidity 0.5.0;

library Address {

  function isContract(address account) internal view returns (bool) {
    uint256 size;

    assembly { size := extcodesize(account) }
    return size > 0;
  }

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

  function ownerOf(uint256 tokenId) public view returns (address) {
    address owner = _tokenOwner[tokenId];
    require(owner != address(0));
    return owner;
  }

  function getApproved(uint256 tokenId) public view returns (address) {
    require(_exists(tokenId));
    return _tokenApprovals[tokenId];
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

    _clearApproval(from, tokenId);
    _removeTokenFrom(from, tokenId);
    _addTokenTo(to, tokenId);

    emit Transfer(from, to, tokenId);
  }

  function _exists(uint256 tokenId) internal view returns (bool) {
    address owner = _tokenOwner[tokenId];
    return owner != address(0);
  }

  function _isApprovedOrOwner(
    address spender,
    uint256 tokenId
  )
    internal
    view
    returns (bool)
  {
    address owner = ownerOf(tokenId);

    return (
      spender == owner ||
      getApproved(tokenId) == spender ||
      isApprovedForAll(owner, spender)
    );
  }

  function _clearApproval(address owner, uint256 tokenId) internal {
    require(ownerOf(tokenId) == owner);
    if (_tokenApprovals[tokenId] != address(0)) {
      _tokenApprovals[tokenId] = address(0);
    }
  }

  function _addTokenTo(address to, uint256 tokenId) internal {
    require(_tokenOwner[tokenId] == address(0));
    _tokenOwner[tokenId] = to;
    _ownedTokensCount[to] = _ownedTokensCount[to].add(1);
  }

  function _removeTokenFrom(address from, uint256 tokenId) internal {
    require(ownerOf(tokenId) == from);
    _ownedTokensCount[from] = _ownedTokensCount[from].sub(1);
    _tokenOwner[tokenId] = address(0);
  }

}

pragma solidity 0.5.0;

contract ERC721Enumerable is ERC165, ERC721, IERC721Enumerable {

  mapping(address => uint256[]) private _ownedTokens;

  mapping(uint256 => uint256) private _ownedTokensIndex;

  uint256[] private _allTokens;

  mapping(uint256 => uint256) private _allTokensIndex;

  bytes4 private constant _InterfaceId_ERC721Enumerable = 0x780e9d63;

  function totalSupply() public view returns (uint256) {
    return _allTokens.length;
  }

  function _addTokenTo(address to, uint256 tokenId) internal {
    super._addTokenTo(to, tokenId);
    uint256 length = _ownedTokens[to].length;
    _ownedTokens[to].push(tokenId);
    _ownedTokensIndex[tokenId] = length;
  }

  function _removeTokenFrom(address from, uint256 tokenId) internal {
    super._removeTokenFrom(from, tokenId);

    uint256 tokenIndex = _ownedTokensIndex[tokenId];
    uint256 lastTokenIndex = _ownedTokens[from].length.sub(1);
    uint256 lastToken = _ownedTokens[from][lastTokenIndex];

    _ownedTokens[from][tokenIndex] = lastToken;

    _ownedTokens[from].length--;

    _ownedTokensIndex[tokenId] = 0;
    _ownedTokensIndex[lastToken] = tokenIndex;
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

    function containsOnlyLower(string memory str) public view returns (bool) {
        bytes memory bStr = bytes(str);

        for (uint i = 0; i < bStr.length; i++) {
            bytes1   char = bStr[i];

            if ( !((char >= 0x61) && (char <= 0x7A))   ) {
            return false;
          }
        }

        return true;

      }

   function _lower(bytes1 _b1)
       private
       pure
       returns (bytes1) {

       if (_b1 >= 0x41 && _b1 <= 0x5A) {
           return bytes1(uint8(_b1)+32);
       }

       return _b1;
   }

}
