# Booyer-Moore's algorithm

## Text generation

## Serching the pattern

Available script parameters:
* `--text-file` - optional - default: stdin
* `--pattern` - required
* `--segment-length` - text segment length pushed to worker thread - default: 100
* `--segments-per-worker` - number of segments pushed on single worker thread - default: 2

Invoking samples:
```bash
cat text_file.txt | search.py --pattern alc
search.py --text-file text_file.txt --pattern alc
```
