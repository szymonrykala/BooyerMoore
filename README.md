# Booyer-Moore's algorithm

## Text generation

## Serching the pattern

Available script parameters:
* `--text-file` - optional - default: stdin
* `--pattern` - required
* `--worker` - number of segments pushed on single worker thread - default: 3

Invoking samples:
```bash
cat text_file.txt | search.py --pattern ale

search.py --text-file text_file.txt --pattern ale

./search.py --text-file ./text.txt --pattern ale --worker 8
```

## Text generation script
* `--length` - required - number of characters to generate
* `--distribution` - optional - distribution of generated characters - available: normal, uniform - default: normal
* `--mean` - optional - mean of the distribution used for random generation of letters - default: 1
* `--std-dev` - optional - standard deviation of the distribution used for random generation of letters - default: 0
* `--character-set` - optional - set of characters that words will be generated from - default: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
* `--workers` - optional - amount of thread workers used to generate text - default: 1

Invoking samples
```bash
./text_generator.py --length 10000 --mean 1 --std-dev 0
```

## Text visualization script
* `--input` - required - input stream of characters to visualize
* `--output` - optional - output path of the image - default: foo.png

Invoking samples
```bash
./text_generator.py --length 10000 | ./text_visualization.py
```