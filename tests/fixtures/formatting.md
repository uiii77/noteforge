# Markdown and C fragments

Keep the code exactly, including operators and string contents:

```c
if (ready || retry) {
    puts("a|b & <ok>");
}
```

The literal pattern is `*_item_[0]` and the relative path is `notes/a_b.md`.
The three backticks below are part of a Markdown example, not the end of these notes:

````markdown
```c
int mask = a | b;
```
````

For a quick comparison: `||` means logical OR; `|` means bitwise OR.
