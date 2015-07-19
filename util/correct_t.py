inr = '/Volumes/transport/data/puzzle/050714-test/track/050714_s13_type-markers_4RT5H7JN.csv'
out = '/Volumes/transport/data/puzzle/050714-test/track/050714_s13_type-markers_4RT5H7JN_2.csv'

with open(inr, 'r') as i:
  with open(out, 'w+') as o:
    o.write('expt,series,channel,id,t,r,c\n')
    for line in i.readlines():
      if 'expt' not in line:
        line = line.rstrip().split(',')
        t = int(line[4]) - 1
        line[4] = str(t)
        line = ','.join(line) + '\n'
        o.write(line)
