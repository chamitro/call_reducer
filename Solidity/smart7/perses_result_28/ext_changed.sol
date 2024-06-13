contract Exchange         {
    mapping(bytes32 => bool)        transferred;
    function transferTokens(                                                                                                                                 )                                         {
      bytes32 hash                                                                ;
              transferred[hash] == false ;
    }
}
