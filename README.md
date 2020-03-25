# README

Decodes substitution ciphers by MCMC Metropolis (see [Diaconis, 2009](https://math.uchicago.edu/~shmuel/Network-course-readings/MCMCRev.pdf)).




## Usage
In project folder:
```bash
python decipher.py [-h] [--makeQ] [--n N] [--corpus CORPUS] [--decode DECODE]
                   [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --makeQ          whether probability matrix must be computed (default:
                   False)
  --n N            size of grams in language model (default: 3 [trigram])
  --corpus CORPUS  path to corpus file (default: corpus/WAP.html [War and
                   Peace text])
  --decode DECODE  path to encoded file (default: encoded/scrambled0.txt)
  --output OUTPUT  path to output file for all iterations of decoding
                   (default: log.txt)
```

## Sample Result
~14000 iterations till convergence. Trigram model.
```
0 v mtvlfzlmt vvhmolsa thvmaytvxtvhmolltqvoev ma vhmolvvugttugtcv...
2000 ualouzhszloauudlnzp aodul wouroudlnzzotuneual audlnzuuxcooxc...
4000 slo bcublos elibmasoe lavo wo elibbor ig slas elib xyooxy...
6000 sho bcubhos lhibtasol havo wo lhibboe ig shas lhib xrooxr...
8000 tho fcufhot shifmatos havo wo shiffoe ir that shif xnooxn...
10000 the fdofhet shifmates have ye shiffew in that shif qreeq...
12000 the crochet shicmates have ye shicced in that shic queeq...
14000 the prophet shipmates have ye shipped in that ship queeq...
```
