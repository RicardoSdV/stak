## trimLog

### Generally compresses redundant and removes not very useful info from logs.

It works in several stages:

- Prefix removal: Removes datatime and log type prefixes, which are useful sometimes but mostly just take up space
- Lines compression: It identifies patterns in the lines of logs and compresses them, see: src/compress.py
- Line compression: This stage is designed to work with logs produced with the omropocs() from the stak repo, it
applies the same compression principles to individual lines.

### Setup
It was developed and tested in python312, uses no dependencies other than the standard library and nothing wierd
so, it ought to work in older versions.
