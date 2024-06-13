





library BytesDeserializer {

  
  

  
  

  
  

  
  

  
  



}




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





library Roles {
  struct Role {
    mapping (address => bool) bearer;
  }

  
  function add(Role storage role, address addr)
    internal
  {
    role.bearer[addr] = true;
  }

  
  

  
  function check(Role storage role, address addr)
    view
    internal
  {
    require(has(role, addr));
  }

  
  function has(Role storage role, address addr)
    view
    internal
    returns (bool)
  {
    return role.bearer[addr];
  }
}




contract RBAC {
  using Roles for Roles.Role;

  mapping (string => Roles.Role) private roles;

  event RoleAdded(address addr, string roleName);
  event RoleRemoved(address addr, string roleName);

  
  string public  ROLE_ADMIN = "admin";

  
  function RBAC()
    public
  {
    addRole(msg.sender, ROLE_ADMIN);
  }

  
  function checkRole(address addr, string roleName)
    view
    public
  {
    roles[roleName].check(addr);
  }

  
  function hasRole(address addr, string roleName)
    view
    public
    returns (bool)
  {
    return roles[roleName].has(addr);
  }

  
  

  
  

  
  function addRole(address addr, string roleName)
    internal
  {
    roles[roleName].add(addr);
    RoleAdded(addr, roleName);
  }

  
  

  
  

  
  

  
  
  
  
  
  
  
  
  

  

  
  
}





contract ERC20Basic {
  
  
  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}




contract ERC20 is ERC20Basic {
  
  
  
  event Approval(address indexed owner, address indexed spender, uint256 value);
}


interface InvestorToken {
  
}



contract Exchange is RBAC {
    using SafeMath for uint256;
    using BytesDeserializer for bytes;

    
    
    string public  ROLE_FORCED = "forced";
    string public  ROLE_TRANSFER_TOKENS = "transfer tokens";
    string public  ROLE_TRANSFER_INVESTOR_TOKENS = "transfer investor tokens";
    string public  ROLE_CLAIM = "claim";
    string public  ROLE_WITHDRAW = "withdraw";
    string public  ROLE_TRADE = "trade";
    string public  ROLE_CHANGE_DELAY = "change delay";
    string public  ROLE_SET_FEEACCOUNT = "set feeaccount";
    string public  ROLE_TOKEN_WHITELIST = "token whitelist user";


    
    mapping(bytes32 => bool) public withdrawn;
    
    mapping(bytes32 => bool) public transferred;
    
    mapping(address => bool) public tokenWhitelist;
    
    mapping(address => uint256) public tokensTotal;
    
    mapping(address => mapping(address => uint256)) public balanceOf;
    
    mapping (bytes32 => uint256) public orderFilled;
    
    address public feeAccount;
    
    
    
    uint256 public delay;

    
    event TokenWhitelistUpdated(address token, bool status);
    
    event FeeAccountChanged(address newFeeAccocunt);
    
    event DelayChanged(uint256 newDelay);
    
    event Deposited(address token, address who, uint256 amount, uint256 balance);
    
    event Forced(address token, address who, uint256 amount);
    
    event Withdrawn(address token, address who, uint256 amount, uint256 balance);
    
    event Requested(address token, address who, uint256 amount, uint256 index);
    
    event TransferredInvestorTokens(address, address, address, uint256);
    
    event TransferredTokens(address, address, address, uint256, uint256, uint256);
    
    event OrderExecuted(
        bytes32 orderHash,
        address maker,
        address baseToken,
        address quoteToken,
        address feeToken,
        uint256 baseAmountFilled,
        uint256 quoteAmountFilled,
        uint256 feePaid,
        uint256 baseTokenBalance,
        uint256 quoteTokenBalance,
        uint256 feeTokenBalance
    );

    
    struct Withdrawal {
      address user;
      address token;
      uint256 amount;
      uint256 createdAt;
      bool executed;
    }

    
    
    Withdrawal[] withdrawals;

    enum OrderType {Buy, Sell}

    
    
    
    struct Order {
      OrderType orderType;
      address maker;
      address baseToken;
      address quoteToken;
      address feeToken;
      uint256 amount;
      uint256 priceNumerator;
      uint256 priceDenominator;
      uint256 feeNumerator;
      uint256 feeDenominator;
      uint256 expiresAt;
      uint256 nonce;
    }

    
    
    function Exchange(uint256 _delay) {
      delay = _delay;

      feeAccount = msg.sender;
      addRole(msg.sender, ROLE_FORCED);
      addRole(msg.sender, ROLE_TRANSFER_TOKENS);
      addRole(msg.sender, ROLE_TRANSFER_INVESTOR_TOKENS);
      addRole(msg.sender, ROLE_CLAIM);
      addRole(msg.sender, ROLE_WITHDRAW);
      addRole(msg.sender, ROLE_TRADE);
      addRole(msg.sender, ROLE_CHANGE_DELAY);
      addRole(msg.sender, ROLE_SET_FEEACCOUNT);
      addRole(msg.sender, ROLE_TOKEN_WHITELIST);
    }

    
    
    
    


    
    
    

    
    
    

    
    
    
    
    
    
    

    
    
    
    function depositEthers() external payable returns(bool) {
      depositInternal(address(0), msg.value);
      return true;
    }

    
    
    
    
    
    
    
    
    
    

    
    
    
    
    

    
    
    
    
    

    
    
    

    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    

    
    
    

    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    

    
    
    
    
    
    

    
    
    
    
    
    

    
    
    
    
    function depositInternal(address token, uint256 amount) internal {
      require(tokenWhitelist[address(token)]);

      balanceOf[token][msg.sender] = balanceOf[token][msg.sender].add(amount);
      tokensTotal[token] = tokensTotal[token].add(amount);

      Deposited(token, msg.sender, amount, balanceOf[token][msg.sender]);
    }

    
    
    
    
    
    
    

    
    
    
    

    
    
    
    
    
    
    
    
    
}
