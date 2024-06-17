pragma solidity ^0.4.21;

interface ERC165 {

}

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  function transferOwnership(address newOwner) public           {
    require(newOwner != address(0));
    emit OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}

contract ERC721 is ERC165 {
    event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);

    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) public payable;
    function safeTransferFrom(address _from, address _to, uint256 _tokenId) public payable;
    function transferFrom(address _from, address _to, uint256 _tokenId) external payable;
    function approve(address _approved, uint256 _tokenId) external payable;

}

interface ERC721TokenReceiver {

}

interface ERC721Metadata  {

}

interface ERC721Enumerable  {

    function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256);
}

contract PublishInterfaces is ERC165 {

    mapping(bytes4 => bool) internal supportedInterfaces;

}

contract Metadata {

}

contract GanNFT is ERC165, ERC721, ERC721Enumerable, PublishInterfaces, Ownable {

  bytes4 private constant ERC721_RECEIVED = bytes4(keccak256("onERC721Received(address,uint256,bytes)"));

  uint256 public claimPrice = 0;

  uint256 public maxSupply = 300;

  Metadata public erc721Metadata;

  uint256[] public tokenIds;

  mapping(uint256 => address) public tokenIdToOwner;

  mapping(address => uint256) public ownershipCounts;

  mapping(address => uint256[]) public ownerBank;

  mapping(uint256 => address) public tokenApprovals;

  mapping (address => mapping (address => bool)) internal operatorApprovals;

  function setMetadataAddress(address _contractAddress) public           {
      erc721Metadata = Metadata(_contractAddress);
  }

  event Transfer(address indexed _from, address indexed _to, uint256 _value);

  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);

  event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);

  function setMaxSupply(uint max) external payable           {
    require(max > tokenIds.length);

    maxSupply = max;
  }

  function setClaimPrice(uint256 price) external payable           {
    claimPrice = price;
  }

  function newGanToken(uint256 _noise) external payable {
    require(msg.sender != address(0));
    require(tokenIdToOwner[_noise] == 0x0);
    require(tokenIds.length < maxSupply);
    require(msg.value >= claimPrice);

    tokenIds.push(_noise);
    ownerBank[msg.sender].push(_noise);
    tokenIdToOwner[_noise] = msg.sender;
    ownershipCounts[msg.sender]++;

    emit Transfer(address(0), msg.sender, 0);
  }

  function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) public payable
  {
      _safeTransferFrom(_from, _to, _tokenId, data);
  }

  function safeTransferFrom(address _from, address _to, uint256 _tokenId) public payable
  {
      _safeTransferFrom(_from, _to, _tokenId, "");
  }

  function transferFrom(address _from, address _to, uint256 _tokenId) external payable {
    require(_to != 0x0);
    require(_to != address(this));
    require(tokenApprovals[_tokenId] == msg.sender);
    require(tokenIdToOwner[_tokenId] == _from);

    _transfer(_tokenId, _to);
  }

  function approve(address _to, uint256 _tokenId) external                payable {

      tokenApprovals[_tokenId] = _to;

      emit Approval(msg.sender, _to, _tokenId);
  }

  function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256 _tokenId) {
      require(_owner != address(0));
      require(_index < ownerBank[_owner].length);
      _tokenId = ownerBank[_owner][_index];
  }

  function _transfer(uint256 _tokenId, address _to) internal {
    require(_to != address(0));

    address from = tokenIdToOwner[_tokenId];
    uint256 tokenCount = ownershipCounts[from];

    for (uint256 i = 0; i < tokenCount; i++) {
      uint256 ownedId = ownerBank[from][i];
      if (_tokenId == ownedId) {
        delete ownerBank[from][i];
        if (i != tokenCount) {
          ownerBank[from][i] = ownerBank[from][tokenCount - 1];
        }
        break;
      }
    }

    ownershipCounts[from]--;
    ownershipCounts[_to]++;
    ownerBank[_to].push(_tokenId);

    tokenIdToOwner[_tokenId] = _to;
    tokenApprovals[_tokenId] = address(0);
    emit Transfer(from, _to, 1);
  }

  function _safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data)
      private

  {
      address owner = tokenIdToOwner[_tokenId];

      require(owner == _from);
      require(_to != address(0));
      require(_to != address(this));
      _transfer(_tokenId, _to);

      uint256 codeSize;
      assembly { codeSize := extcodesize(_to) }
      if (codeSize == 0) {
          return;
      }
      bytes4 retval                                                                   ;
      require(retval == ERC721_RECEIVED);
  }

  function _toString(bytes32[4] _rawBytes, uint256 _stringLength) private pure returns (string) {
      string memory outputString = new string(_stringLength);
      uint256 outputPtr;
      uint256 bytesPtr;

      assembly {
          outputPtr := add(outputString, 32)
          bytesPtr := _rawBytes
      }

      return outputString;
  }

  function tokenMetadata(uint256 _tokenId, string _preferredTransport) external view returns (string infoUrl) {
      require(erc721Metadata != address(0));
      uint256 count;
      bytes32[4] memory buffer;

      (buffer, count)                                                            ;

      return _toString(buffer, count);
  }

}

contract GanTokenMain is GanNFT {

  struct Offer {
    bool isForSale;
    uint256 tokenId;
    address seller;
    uint value;          
    address onlySellTo;     
  }

  struct Bid {
    bool hasBid;
    uint256 tokenId;
    address bidder;
    uint value;
  }

  mapping(address => uint256) public pendingWithdrawals;

  mapping(uint256 => Offer) public ganTokenOfferedForSale;

  mapping(uint256 => Bid) public tokenBids;

  event BidForGanTokenOffered(uint256 tokenId, uint256 value, address sender);
  event BidWithdrawn(uint256 tokenId, uint256 value, address bidder);
  event GanTokenOfferedForSale(uint256 tokenId, uint256 minSalePriceInWei, address onlySellTo);
  event GanTokenNoLongerForSale(uint256 tokenId);

  function ganTokenNoLongerForSale(uint256 tokenId) public payable               {
    ganTokenOfferedForSale[tokenId] = Offer(false, tokenId, msg.sender, 0, 0x0);

    emit GanTokenNoLongerForSale(tokenId);
  }

  function offerGanTokenForSale(uint tokenId, uint256 minSalePriceInWei) external payable               {
    ganTokenOfferedForSale[tokenId] = Offer(true, tokenId, msg.sender, minSalePriceInWei, 0x0);

    emit GanTokenOfferedForSale(tokenId, minSalePriceInWei, 0x0);
  }

  function offerGanTokenForSaleToAddress(uint tokenId, address sendTo, uint256 minSalePriceInWei) external payable {
    require(tokenIdToOwner[tokenId] == msg.sender);
    ganTokenOfferedForSale[tokenId] = Offer(true, tokenId, msg.sender, minSalePriceInWei, sendTo);

    emit GanTokenOfferedForSale(tokenId, minSalePriceInWei, sendTo);
  }

  function buyGanToken(uint256 id) public payable {
    Offer memory offer = ganTokenOfferedForSale[id];
    require(offer.isForSale);
    require(offer.onlySellTo == msg.sender && offer.onlySellTo != 0x0);
    require(msg.value == offer.value);
    require(tokenIdToOwner[id] == offer.seller);

    safeTransferFrom(offer.seller, offer.onlySellTo, id);

    ganTokenOfferedForSale[id] = Offer(false, id, offer.seller, 0, 0x0);

    pendingWithdrawals[offer.seller] += msg.value;
  }

  function enterBidForGanToken(uint256 tokenId) external payable {
    Bid memory existing = tokenBids[tokenId];
    require(tokenIdToOwner[tokenId] != msg.sender);
    require(tokenIdToOwner[tokenId] != 0x0);
    require(msg.value > existing.value);
    if (existing.value > 0) {

      pendingWithdrawals[existing.bidder] += existing.value;
    }

    tokenBids[tokenId] = Bid(true, tokenId, msg.sender, msg.value);
    emit BidForGanTokenOffered(tokenId, msg.value, msg.sender);
  }

  function acceptBid(uint256 tokenId, uint256 price) external payable {
    require(tokenIdToOwner[tokenId] == msg.sender);
    Bid memory bid = tokenBids[tokenId];
    require(bid.value != 0);
    require(bid.value == price);

    safeTransferFrom(msg.sender, bid.bidder, tokenId);

    tokenBids[tokenId] = Bid(false, tokenId, address(0), 0);
    pendingWithdrawals[msg.sender] += bid.value;
  }

  function withdrawBid(uint256 tokenId) external payable {
      Bid memory bid = tokenBids[tokenId];
      require(tokenIdToOwner[tokenId] != msg.sender);
      require(tokenIdToOwner[tokenId] != 0x0);
      require(bid.bidder == msg.sender);

      emit BidWithdrawn(tokenId, bid.value, msg.sender);
      uint amount = bid.value;
      tokenBids[tokenId] = Bid(false, tokenId, 0x0, 0);

      msg.sender.transfer(amount);
  }

}
