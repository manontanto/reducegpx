#!/usr/bin/env python3
# reducegpx
#
# 2023-03-30
# manontanto
''' reduce point GPX data. 60 point/minites → 3 point/minites '''

import re
from datetime import datetime as dt
from datetime import timedelta
INTERVAL = 20

GPX_FILE = "logtest.gpx"
REDUCED_FILE = "reduced.gpx"

pattern = re.compile(r'<time>(.+)</time>')
sub_pattern = re.compile(r'\.\d+')
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def w_header(d):
    ''' write header string block to file '''
    header = re.match(r'(<\?xml (.|\s)*?<trkseg>)', d)  # d: data string
    w_file(header.group())

def w_footer():
    footer = '    </trkseg>\n  </trk>\n</gpx>\n'
    w_file(footer)

def w_file(w_tp):
    ''' write track_point string block to file '''
    with open(REDUCED_FILE, 'a', encoding='utf-8') as f_reduced:
        f_reduced.write(w_tp + '\n')

def get_pt_obj(tp):
    '''IN:  track_point string block
       OUT: its datetime object.
    '''
    point_time = pattern.search(tp)
    t = point_time.group(1)     # string
    t = sub_pattern.sub('', t)  # delete milisecond
    return conv_datetime_obj(t)

def conv_datetime_obj(t_string):
    return dt.strptime(t_string, TIME_FORMAT)

def main():
    with open(GPX_FILE, 'r', encoding='utf-8') as f_gpx:
        d = f_gpx.read()
    track_points = re.findall(r'( +<trkpt(.|\s)*?</trkpt>)', d)
    start_point = track_points[0][0]  # 1st. block

    w_header(d)
    w_file(start_point)
    t1_dt = get_pt_obj(start_point)
    nx_dt = t1_dt + timedelta(seconds=INTERVAL)

    for tp in track_points:
        tp = tp[0]   # each track_point string is in tp[0] of tp_tuple
        t2_dt = get_pt_obj(tp)
        if t2_dt >= nx_dt:
            w_file(tp)
            nx_dt =  t2_dt + timedelta(seconds=INTERVAL)

    w_footer()

if __name__ == '__main__':
    main()