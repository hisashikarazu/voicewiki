import time


from lib import spreadsheet, sendtext
from lib import text2wav, receivewiki


start_time = time.time()

def to_ss(from_wiki):
    ss = spreadsheet.spread_sheet(from_wiki)
    ss.write_ss()


def run_time():
    p = time.time() - start_time
    p_time = []
    p_time.append(int(p / 60))
    p_time.append(int(p_time[0] / 60))
    p_time.append(int(p_time[1] / 24))

    print('実行時間: %d日 %d時間 %d分 %d秒' % 
            (p_time[2], p_time[1]%24, p_time[0]-p_time[1]*60, p%60))
    print('実行時間: %.2f[s]' % p)


def do_main():
    fw = receivewiki.from_wiki(0) # 0: small, 1: large

    to_ss(fw)
    sendtext.to_csv(fw)
    text2wav.create_wav(fw, 2)
    run_time()


if __name__ == '__main__':
    do_main()