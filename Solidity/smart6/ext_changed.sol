pragma solidity ^0.4.21;



interface ERC165 {
    
}



contract Ownable {
  address public owner;


  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);


  
  

  
  

  
  

}









contract ERC721 is ERC165 {
    event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
    
    
    function transferFrom(address _from, address _to, uint256 _tokenId) external payable;
    
    
    
    
}


interface ERC721TokenReceiver {
	
}


interface ERC721Metadata  {
    
    
    
}


interface ERC721Enumerable  {
    
    
    
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

  
  

  
  

  
  
  
  

  modifier canTransfer(uint256 _tokenId, address _from, address _to) {
    address owner = tokenIdToOwner[_tokenId];
    require(tokenApprovals[_tokenId] == _to || owner == _from || operatorApprovals[_to][_to]);
    _;
  }
  
  
  

  
  event Transfer(address indexed _from, address indexed _to, uint256 _value);

  
  
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);

  
  
  event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);

  
  

  
  

  
  

  
  
  
  

  
  
  
  

  
  

  
  
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

  
  
  
  
  
  
  
  
  
  
  
  
  

  
  
  
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  function transferFrom(address _from, address _to, uint256 _tokenId) external payable {
    require(_to != 0x0);
    require(_to != address(this));
    require(tokenApprovals[_tokenId] == msg.sender);
    require(tokenIdToOwner[_tokenId] == _from);

    _transfer(_tokenId, _to);
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


  
  
  

  
  
  
  

  
  
  

  
  
  
  

  
  
  

  
  
  
  

  
  
  
  

  
  
  
  

  
  
  
  

  
  
  

  
  

}
