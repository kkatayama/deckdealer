#!/usr/bin/env python3
import argparse
import pandas as pd

def compute_hours(b_id, s_id, start, end, wage, tips):
    s = pd.to_datetime(start)
    e = pd.to_datetime(end)
    h = (e - s).total_seconds()/60.0/60.0
    worked = round(h, 2)
    earn = round(worked * wage + tips, 2)
    print(f'Hours Worked: {worked:.2f}')
    print(f'Total Earnings: {earn:.2f}')
    print(f'/bartender_id/{b_id}/shift_id/{s_id}/hourly_wage/{wage:.2f}/clock_in/{s}/clock_out/{e}/hours_worked/{worked:.2f}/tips/{tips:.2f}/total_earnings/{earn:.2f}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--bartender_id', help='bartender_id')
    ap.add_argument('--shift_id', help='shift_id')
    ap.add_argument('-s', '--start', help='clock_in')
    ap.add_argument('-e', '--end', help='clock_out')
    ap.add_argument('-w', '--wage', help='hourly_wage')
    ap.add_argument('-t', '--tips', help='reported_tips')
    args = ap.parse_args()
    
    # -- compute_hours('2022-10-20 09:45:00', '2022-10-20 14:10:00', 2.33, 85)
    compute_hours(args.bartender_id, args.shift_id, args.start, args.end, float(args.wage), float(args.tips))
