pragma solidity ^0.8.0;

interface I_ERC20 {
  function transfer(address to, uint256 amount);
  function transferFrom(address from, address to, uint256 amount);
  function balanceOf(address _address);
}

contract Wallet {
  
  address public owner;
  uint256 public maxPledgeAmount;
  uint256 public maxNumPledged;
  uint256 public targetAmount;
  uint256 public numPledged = 0;
  uint256 public numClaimed = 0;
  uint256 public totalPledged = 0;

  mapping(uint256 => address) public pledgers;
  mapping(address => uint256) public pledgeAmounts;

  event Pledged(address pledger, address token, address amount);
  event Claimed(address pledger, address token, address amount);

  constructor(uint256 _maxPledgeAmount, uint256 _maxNumPledged uint256 _targetAmount) public {
    owner = msg.sender;
    maxPledgeAmount = _maxPledgeAmount;
    targetAmount = _targetAmount;
  }

  function pledge(address token, uint256 amount) public {
    require(pledgeAmounts[msg.sender] + amount < maxPledgeAmount, "Cannot pledge more than maxPledgeAmount");

    I_ERC20(token).transferFrom(msg.sender, address(this), amount);
  }

  function setMaxPledgeAmount(uint256 _maxPledgeAmount) public {
    require(msg.sender == owner);
    maxPledgeAmount = _maxPledgeAmount;
  }

  function setMaxNumPledged(uint256 _maxNumPledged) {
    require(msg.sender == owner);
    maxNumPledged = _maxNumPledged;
  }

  
}