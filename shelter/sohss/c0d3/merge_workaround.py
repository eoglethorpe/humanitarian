"""work around for merging just hno data without having to re-pull. he pulls!!!!!!"""
import pandas as pd

def main():
    master = pd.read_csv('../d0cz/master_manual_merge_rm_hno_dups.csv')
    add = pd.read_csv('../d0cz/hno_process_out.csv')
    mrg = master.merge(add, left_on='sc.uid', right_on='hno_uid', how='left')
    mrg.to_csv('../d0cz/master_new_merge.csv')


if __name__ == '__main__':
    main()