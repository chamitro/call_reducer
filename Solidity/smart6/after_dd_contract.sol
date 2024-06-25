pragma solidity ^0.4.21;

contract PublishInterfaces           {

    mapping(bytes4 => bool) internal supportedInterfaces;

}

contract Metadata {

}

contract GanNFT is PublishInterfaces{

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

  function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes data) public payable
  {
      _safeTransferFrom(_from, _to, _tokenId, data);
  }

  function safeTransferFrom(address _from, address _to, uint256 _tokenId) public payable
  {
      _safeTransferFrom(_from, _to, _tokenId, "");
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

}

