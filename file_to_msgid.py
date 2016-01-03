import glob

def from_tuto(t):
    IDX = 0
    for fn in sorted(glob.glob('ext/data/tuto*.txt')):
        with open(fn) as r, open(fn + '.msgid', 'w') as w:
            for l in r.readlines():
                v = l.rstrip().split(',', 3)
                if not l.rstrip() or len(v) < 2 \
                        or not v[1].startswith('CHR'):
                    w.write(l)
                    continue
                IDX += 1
                key = 'TUTO%04d' % IDX
                t.write(('%s\t%s\r\n' % (key, v[3])))
                v[3] = key
                w.write(','.join(v))
                w.write('\r\n')

def from_news(t):
    IDX = 0
    fn = 'ext/data/news.txt'
    with open(fn) as r, open(fn + '.msgid', 'w') as w:
        for l in r.readlines():
            if l.startswith('/'):
                w.write(l)
                continue
            if l.startswith('-'):
                v = l.rstrip().split(',', 2)
                IDX += 1
                key = 'NEWS%04d' % IDX
                t.write(('%s\t%s\r\n' % (key, v[2])))
                v[2] = key
            else:
                v = l.rstrip().split(',', 3)
                if len(v) < 4:
                    w.write(l)
                    continue
                IDX += 1
                key = 'NEWS%04d' % IDX
                t.write(('%s\t%s\r\n' % (key, v[3])))
                v[3] = key
            w.write(','.join(v))
            w.write('\r\n')

def from_snews(t):
    IDX = 0
    fn = 'ext/data/snews.txt'
    with open(fn) as r, open(fn + '.msgid', 'w') as w:
        for l in r.readlines():
            v = l.rstrip().split(':', 1)
            if len(v) < 2:
                w.write(l)
                continue
            try:
                int(v[0])
            except ValueError:
                w.write(l)
                continue
            if ('%03d' % int(v[0])) != v[0]:
                w.write(l)
                continue
            IDX += 1
            key = 'SNEWS%04d' % IDX
            t.write(('%s\t%s\r\n' % (key, v[1])))
            v[1] = key
            w.write(':'.join(v))
            w.write('\r\n')

def from_kyaku_data(t):
    IDX = 0
    fn = 'ext/data/kyaku.txt'
    with open(fn) as r, open(fn + '.msgid', 'w') as w:
        for l in r.readlines():
            v = l.rstrip().split(':', 5)
            if len(v) < 2:
                w.write(l)
                continue
            try:
                int(v[0])
            except ValueError:
                w.write(l)
                continue
            if ('%03d' % int(v[0])) != v[0]:
                w.write(l)
                continue
            IDX += 1
            key = 'KYAKUNAME%04d' % IDX
            t.write(('%s\t%s\r\n' % (key, v[1])))
            v[1] = key
            w.write(':'.join(v))
            w.write('\r\n')

def from_data(t):
    # tuto*
    from_tuto(t)
    # news
    from_news(t)
    # snews
    from_snews(t)
    # kyaku
    from_kyaku_data(t)
    # TODO
    # oder
    # item
    # need item remap:
    #   enermy
    #   enermylist

def from_kyaku(t):
    IDX = 0
    for fn in sorted(glob.glob('ext/kyaku/*.txt')):
        with open(fn) as r, open(fn + '.msgid', 'w') as w:
            for l in r.readlines():
                if not l.startswith('msg'):
                    w.write(l)
                    continue
                v = l.rstrip().split(':', 4)
                IDX += 1
                key = 'KYAKU%04d' % IDX
                if len(v) < 5:
                    t.write(('%s\t%s\r\n' % (key, v[3])))
                    v[3] = key
                else:
                    t.write(('%s\t%s\r\n' % (key, v[4])))
                    v[4] = key
                w.write(':'.join(v))
                w.write('\r\n')

def from_iv(t):
    IDX = 0
    for fn in sorted(glob.glob('ext/iv/*.ivt')):
        with open(fn) as r, open(fn + '.msgid', 'w') as w:
            for l in r.readlines():
                if not l.startswith('msg:'):
                    w.write(l)
                    continue
                v = l.rstrip().split(':', 3)
                # FIX JUST ONE WRONG MSG
                # like this `msg:0:11alcohol without...`
                if len(v) < 4:
                    if not v[2].startswith('11'):
                        print l
                        w.write(l)
                        continue
                    v.append(v[2].lstrip('11'))
                    v[2] = '11'
                IDX += 1
                key = 'IV%04d' % IDX
                t.write(('%s\t%s\r\n' % (key, v[3])))
                v[3] = key
                w.write(':'.join(v))
                w.write('\r\n')

with open('msg_table.txt', 'w') as t:
    from_iv(t)
    from_kyaku(t)
    from_data(t)
