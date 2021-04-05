# Arth DEX V1

## Arth  Dex Pair

pool fee is configurable at run time by the pool deployer 

Swap function
```
swap(uint amount0Out, uint amount1Out, address to, bytes calldata data)
```

* The function is entered after caller transfers amount to be exchanged(amount0In or amount1In depending on exchange direction)

* Obtain token amounts before swap: _reserve0, _reserve1
* The pair transfers amount0Out and/or amount1Out to the caller's address(to)
* Obtain token amounts after swap: balance0, balance1
* calculate amount0In and/or amount1In (usually one) based on reserves and balances. This is the amount caller transferred before calling this swap function.
* check the acceptable reserve ratio (taking in to account the applicable pool fee)
  - Knew = (balance0 - amount0In * fee/1000) * (balance1 - amount0In * fee/1000)
  - Kold = _reserve0 * _reserve1
  - Knew >= Kold (usually equal)