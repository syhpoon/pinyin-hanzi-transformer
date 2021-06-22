#!/usr/bin/env python

import itertools
import spacy

from pypinyin import pinyin, Style

CJK_RANGE = list(range(0x4e00, 0x9fff))

def topinyin(chunk):
    return "".join(list(itertools.chain(*pinyin(chunk, style=Style.NORMAL, strict=True))))

nlp = spacy.load("zh_core_web_sm")

out = open("data/dataset", "w")
chars = set()

with open("data/data") as f:
    buf = []
    while True:
        char = f.read(1)

        if not char:
            break

        if ord(char) in CJK_RANGE:
            buf.append(char)

            if char not in chars:
                chars.add(char)
                p = topinyin(char)
                out.write("{}\t{}\n".format(p, char))

        elif len(buf) > 0:
            if len(buf) > 20:
                buf = buf[:20]

            string = "".join(buf)
            p = topinyin(string)
            out.write("{}\t{}\n".format(p, string))

            for token in nlp(string):
                token = token.text

                if token not in chars:
                    p = topinyin(token)
                    out.write("{}\t{}\n".format(p, token))
                    chars.add(token)

            buf = []

out.close()
