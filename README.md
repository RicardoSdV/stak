# Stak
The idea is to pretty print call stacks and all available introspection for debugging purposes in python27

### trimLog was merged into stak to combine their function!

trimLog: Generally compresses redundant and removes not very useful info from logs.

It works in several stages:

- Prefix removal: Removes datatime and log type prefixes, which are useful sometimes but mostly just take up space
- Lines compression: It identifies patterns in the lines of logs and compresses them, see: src/compress.py
- Line compression: This stage is designed to work with logs produced with the omropocs() from the stak repo, it
applies the same compression principles to individual lines.


TODO: Update this, completely out of date
