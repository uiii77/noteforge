# C logical operators — class fragments

`||` is logical OR; `|` is bitwise OR. Do not interchange them.
Logical OR evaluates the right operand only when the left operand compares equal to zero. Its result is an `int`, either 0 or 1.

```c
int count = 0;
int ok = (1 || ++count);
/* ok == 1; count == 0 */
```

Precedence in this excerpt: `&&` binds more tightly than `||`. Parentheses can make the intended grouping explicit. The example is C, not C++.
