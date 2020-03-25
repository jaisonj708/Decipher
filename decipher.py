import numpy as np
import os,sys,argparse
import random
from utils import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--makeQ", action='store_true', help="whether probability matrix must be computed (default: False)")
    parser.add_argument("--n", type=int, default=3, help="size of grams in language model (default: 3 [trigram])")
    parser.add_argument("--corpus", type=str, default="corpus/WAP.txt", help="path to corpus file (default: corpus/WAP.txt [War and Peace text])")
    parser.add_argument("--decode", type=str, default="encoded/scrambled0.txt", help="path to encoded file (default: encoded/scrambled0.txt)")
    parser.add_argument("--output", type=str, default="log.txt", help="path to output file for all iterations of decoding (default: log.txt)")

    args = parser.parse_args()
    n = args.n

    if not args.makeQ:
        Q = np.load("Q.npy")
    else:
        # make probability matrix (Q) using corpus: 26 letters + 1 space/NL character (last index)
        Q = np.zeros((27**(n-1), 27**(n-1)))

        with open(args.corpus, 'r') as f:
            chars = np.array([ord(c) for c in f.readline().lower()])
            num = 0

            while len(chars) > 0 and num < np.inf: # change 'np.inf' to adjust max chars of corpus to use
                i = 0
                while i <= len(chars) - n:
                    gram = chars[i:i+n]
                    bad = np.argwhere([invalid(c) for c in gram])
                    if len(bad) != 0:
                        i += np.hstack(bad)[-1] + 1
                        continue

                    [x,y] = get_idx(gram)
                    Q[x][y] += 1
                    i += 1

                chars = np.array([ord(c) for c in f.readline().lower()])
                num += 1
                if num % 1000 == 0:
                    print("Read {} lines of corpus".format(num))

            eps = 1e-20
            Q = np.stack([row/(np.sum(row)+eps) for row in Q])
            np.save("Q.npy",Q)

    # set arbitrary code initially (symbol repped by i is encoded as symbol repped by number in index i)
    # for example, if code[25] = 2, then 'z' (repped by 25) is encoded as 'c' (repped by 2)
    code = np.arange(27)
    random.shuffle(code)

    decode = np.zeros(27)
    for i in range(27):
        decode[i] = np.hstack(np.argwhere(code==i))[0]

    with open(args.decode, 'r') as f, open(args.output,'w') as fw:
        f.readline() #header
        line = f.readline()
        coded = [conv_ascii(ord(c)) for c in line]
        logprob_prev = -np.inf
        same_count = 0
        idx = -1

        store = {}

        for reps in range(np.int(1e5)):

            # [idx,idx2,idx3] = np.random.choice(np.arange(27),3,replace=False)

            # [idx,idx2,idx3,idx4] = np.random.choice(np.arange(27),4,replace=False)

            # idx = random.randint(0,26)
            # idx2 = random.randint(0,26)
            # idx2 = (idx2 + (idx==idx2)) % 26
            # # # idx2 = (idx + 1) % 27
            # # idx2 = (idx + 1 + np.int(same_count/50)) % 27

            if (same_count >= 27*50):
                same_count = 0

            idx = (idx + 1) % 27
            # idx2 = (idx + 1) % 27
            idx2 = (idx + 1 + np.int(same_count/50)) % 27
            # idx2 = (idx2 + (idx==idx2)) % 27 # correction if the same-count factor results in idx=idx2


            # code_ = swap(code,idx,idx2)
            # decode_ = swap(decode,code[idx],code[idx2])
            # code_prop = swap(code_,idx2,idx3)
            # decode_prop = swap(decode_,code[idx2],code[idx3])

            # code_ = swap(code,idx,idx2)
            # decode_ = swap(decode,code[idx],code[idx2])
            # code_prop = swap(code_,idx3,idx4)
            # decode_prop = swap(decode_,code_[idx3],code_[idx4])

            code_prop = swap(code,idx,idx2)
            decode_prop = swap(decode,code[idx],code[idx2])

            decoded = [decode_prop[c] for c in coded]
            logprob = 0
            for i in range(len(decoded) - n + 1):
                gram = decoded[i:i+n]
                [x,y] = get_idx([deconv_ascii(c) for c in gram])
                logprob += np.log(Q[x][y] + 1e-30)

            adaptive_push = min(same_count*0.0001,0.01)
            if random.random() < min(1, np.exp(np.clip(logprob-logprob_prev, -10, 10)) + adaptive_push):
                code = code_prop
                decode = decode_prop
                logprob_prev = logprob
                if logprob in store:
                    store[logprob] += 1
                else:
                    store[logprob] = 1

            if logprob_prev != logprob:
                same_count += 1
            else:
                if (logprob in store) and (store[logprob] > 3):
                    same_count += 1 # accounts for possible cycle (returning to previous logprob's)
                else:
                    same_count = 0

            if reps % 500 == 0:
                # if reps % 1000 == 0:
                #     print(reps)
                #     print(same_count)
                #     print(logprob)
                # print(logprob_prev)
                # print(logprob)
                decoded = [decode[c] for c in coded]
                ascii_decoded = [deconv_ascii(c) for c in decoded]
                str_ = "".join(chr(a) for a in ascii_decoded)
                # print(code)
                fw.write(str_)
                print(str(reps) + "   " + str_[:100] + "...")
