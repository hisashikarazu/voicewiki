import time
import re
from ctypes import CDLL
from pathlib import Path
from pprint import pprint


onrt = "dll/onnxruntime.dll"
CDLL(str(Path(onrt).resolve(strict=True)))

from voicevox_core import VoicevoxCore, METAS


def this_date(return_type: int = 0):

    #月を桁合わせず代入
    date_m = time.strftime('%m')
    if date_m[0] == '0':
        date_m = date_m.replace('0', '', 1)
    #日を桁合わせず代入
    date_d = time.strftime('%d')
    if date_d[0] == '0':
        date_d = date_d.replace('0', '', 1)
    
    #return_type==2のとき月日なしのlistで返す
    if return_type == 2:
        md = [date_m, date_d]
        return md

    date_m += '月'
    date_d += '日'

    #return_type==1のときlistで返す
    if return_type == 1:
        date_md = [date_m, date_d]
        return date_md
    
    #strで返す
    return (date_m + date_d)


def list2text(
        text_list: list,
        start_text: str = None,
        fin_text: str = None,
        text_length_type: int = 0
        ) -> str:

    #文の先頭初期化
    if start_text is None:
        date = this_date()
        start_text = f'今日{date}にあった出来事は、'

    #文の末尾初期化
    if fin_text is None:
        fin_text = 'です。'

    #取得するwikiページのタイプ: 0=small, 1=large
    if text_length_type == 0:
        wt = ''
        cap_str = '\(\d.+?\)|\（\d.+?\）' 
        for s in text_list[1:]:
            #cap_strに当てはまる文字列(年号、日付)があればcapに代入
            match = re.search(cap_str, s)
            if match:
                cap = match.group()
                #(年号、日付)を結合
                wt += cap

            #(年号、日付)を除いたものを代入
            wt += re.sub(cap_str, '', s)
            wt += '、'

    else:
        wt = '、'.join(text_list)

    #文字の結合
    wav_text = start_text + wt + fin_text
    
    return wav_text


def text_replace(text: str) -> str:
    delete_char = '\[.+?\]'
    text = re.sub(delete_char, '', text)
    return text


def create_wav(from_wiki, speaker_id=3, wav_name=time.strftime('%m%d')) -> None:

    wav_text = from_wiki[0]
    text_length_type = from_wiki[2]

    if type(wav_text) is not str:
        if type(wav_text) is list:
            wav_text = list2text(
                wav_text, 
                text_length_type=text_length_type
            )

    jtalk_dic = '../open_jtalk_dic_utf_8-1.11'
    core = VoicevoxCore(open_jtalk_dict_dir=Path(jtalk_dic))

    #人及び声の選択
    #pprint(METAS)
    print(f'selected id: {speaker_id}')

    #文字の正規化
    wav_text = text_replace(wav_text)
    print('replaced:\n',wav_text)

    if not core.is_model_loaded(speaker_id):
        core.load_model(speaker_id)

    wave_bytes = core.tts(wav_text, speaker_id)

    wav_path = f'../wav/{wav_name}.wav'

    with open(wav_path, 'wb') as f:
        f.write(wave_bytes)