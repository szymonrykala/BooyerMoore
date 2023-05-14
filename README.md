# Booyer-Moore's algorithm

## Text generation

## Serching the pattern

Available script parameters:
* `--text-file` - optional - default: stdin
* `--pattern` - required
* `--segment-length` - text segment length pushed to worker thread - default: 2000
* `--segments-per-worker` - number of segments pushed on single worker thread - default: 3

Invoking samples:
```bash
cat text_file.txt | search.py --pattern ale

search.py --text-file text_file.txt --pattern ale

./search.py --text-file ./text.txt --pattern ale --segment-length 6000 --segments-per-worker 8
```

## Text generation script
* `--words` - required - number of words to generate
* `--word-length` - optional - length of generated words - default: random
* `--mean` - optional - mean of the normal distribution used for random generation of letters and word length - default: length of the character set / 2
* `--std-dev` - optional - standard deviation of the normal distribution used for random generation of letters and word length - default: mean / 2
* `--character-set` - optional - set of characters that words will be generated from - default: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
* `--workers` - optional - amount of thread workers used to generate text - default: 1

Invoking samples
```bash
./text_generator.py --words 10000 --mean 0 --std-dev 1 --workers 10
```