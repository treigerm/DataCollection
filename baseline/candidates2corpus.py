#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import sys

from ccdownloader import CCDownloader
from html2text import html2text
from textsanitzer import TextSanitizer
from external_processor import TextProcessor


def process_candidates(candidates, outfile):
    if candidates[0][-1] == "" or candidates[1][-1] == "":
        return
    src_url, src_text, src_html = candidates[0]
    tgt_url, tgt_text, tgt_html = candidates[1]

    outfile.write("\t".join((src_url,
                             tgt_url,
                             base64.b64encode(src_text.encode('utf-8')),
                             base64.b64encode(tgt_text.encode('utf-8')),
                             base64.b64encode(src_html.encode('utf-8')),
                             base64.b64encode(tgt_html.encode('utf-8')),)))
    outfile.write("\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-outfile', type=argparse.FileType('w'),
                        help='output file', default=sys.stdout)
    parser.add_argument('-source_tokenizer',
                        help='call to source tokenizer, incl. args')
    parser.add_argument('-source_splitter',
                        help='call to source sentence splitter, incl. args')
    parser.add_argument('-target_tokenizer',
                        help='call to target tokenizer, incl. args')
    parser.add_argument('-target_splitter',
                        help='call to target sentence splitter, incl. args')
    args = parser.parse_args(sys.argv[1:])

    downloader = CCDownloader()
    source_text_processor = TextProcessor(splitter=args.source_splitter,
                                          tokenizer=args.source_tokenizer)
    target_text_processor = TextProcessor(splitter=args.target_splitter,
                                          tokenizer=args.target_tokenizer)

    candidates = []
    for linenr, line in enumerate(sys.stdin):
        if linenr > 0:
            if linenr % 100 == 0:
                sys.stderr.write('.')
            if linenr % 1000 == 0:
                sys.stderr.write("[%d]\n" % linenr)
        url, _crawl, data = line.split('\t', 2)
        data = json.loads(data)
        # Workaround server error
        if 'offset:' in data:
            data['offset'] = data.pop('offset:')

        html = downloader.download(data['filename'],
                                   int(data[u'offset']),
                                   int(data['length']),
                                   html_only=True)
        html = TextSanitizer.to_unicode(html)
        text = html2text(html.encode('utf-8'), sanitize=True)
        if len(candidates) == 0:
            text = source_text_processor.process(text)
        else:
            assert len(candidates) == 1
            text = target_text_processor.process(text)
        candidates.append((url, text, html))

        if len(candidates) == 2:
            process_candidates(candidates, args.outfile)
            candidates = []
