contract GanNFT                                                                 {
  uint256[]        tokenIds;
  mapping(address => uint256[])        ownerBank;
  function newGanToken(uint256 _noise)                  {
    tokenIds.push(_noise);
    ownerBank[msg.sender].push(_noise);
  }
  function _transfer(uint256 _tokenId, address _to)          {
    ownerBank[_to].push(_tokenId);
  }
}
