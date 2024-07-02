contract ERC721           {
  function transferFrom(
    address     ,
    address to,
    uint256 tokenId
  )
    public
  {
    _addTokenTo(to, tokenId);
  }
  function _addTokenTo(address   , uint256        ) internal {
  }
}
contract ERC721Enumerable is ERC721{
  mapping(address => uint256[])         _ownedTokens;
  function _addTokenTo(address to, uint256 tokenId) internal {
    _ownedTokens[to].push(tokenId);
  }
}
