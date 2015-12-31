import os
import urllib
import glob
import config

def load_font_table():
    fonts = dict()
    with open('font.table') as f:
        for l in f.readlines():
            v, k = l.strip().split('=')
            fonts[k.decode('utf-8')] = eval('"\\x%s\\x%s"' % (v[:2], v[2:]))
    return fonts

def trans(v, fonts):
    vv = v.decode('utf-8')
    return [fonts.get(x, x) for x in vv]

def load_text_table(fonts):
    f = urllib.urlopen(config.SHEET_URL)
    text_map = dict()
    for l in f.readlines():
        v = l.split('\t')
        if v[2]:
            print v[0]
        text_map[v[0]] = trans(v[2], fonts) or v[1]
    return text_map

fonts = load_font_table()
text_map = load_text_table(fonts)

def translate():
    for fn in sorted(glob.glob('ext/**/*.msgid')):
        out_fn = fn.replace('ext/', 'out/').replace('.msgid', '')
        outdir = os.path.dirname(out_fn)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open(fn) as r, open(out_fn, 'w') as w:
            for l in r.readlines():
                l = l.rstrip()
                for n, x in enumerate(l.split(',')):
                    if n:
                        w.write(',')
                    for m, y in enumerate(x.split(':')):
                        if m:
                            w.write(':')
                        if not text_map.get(y):
                            w.write(y)
                            continue
                        for z in text_map[y]:
                            w.write(z)
                w.write('\r\n')

if __name__ == '__main__':
    translate()
