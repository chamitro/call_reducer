

library BytesDeserializer {

}

library SafeMath {

}

contract ERC20{

}

contract Exchange{
    using SafeMath for uint256;
    using BytesDeserializer for bytes;

    mapping(bytes32 => bool) public transferred;

    enum OrderType {Buy, Sell}

    function setFeeAccount(address _feeAccount) external                               {

    }

    function transferTokens(ERC20 token, address from, address to, uint256 amount, uint256 fee, uint256 nonce, uint256 expires, uint8 v, bytes32 r, bytes32 s) external                                {
      bytes32 hash = keccak256(this, token, from, to, amount, fee, nonce, expires);
      require(expires >= now);
      require(transferred[hash] == false);
      require(ecrecover(keccak256("\x19Ethereum Signed Message:\n32", hash), v, r, s) == from);

    }

}
