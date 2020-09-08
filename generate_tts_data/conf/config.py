

#encoding=utf-8
import os

class config:

    # 实例:dts-wanli-m 库:wanwu_product
    MYSQL_DB_NAME = 'smart_call'
    ONLINE_MYSQL_URL_ONLINE = 'mysql+mysqldb://***:3306/' + MYSQL_DB_NAME + '?charset=utf8'

    GET_VOICE_TEXT_SQL = '''  '''   

    baker_mapper_pretrained_path = "./data/baker_mapper.json"

    MY_DICT = './data/mydict.dic'
    WORDS_MAPPING_PATH = "./data/words_mapping.csv"

    MIX_VOICE_TEXT = 'mix_voice_text'
    MIX_VOICE_TEXT_INDEX = 'mix_voice_text_index'
    MIX_VOICE_TEXT_DATA_PATH = './data/mix_voice_text_data.csv'


    ch_regex = "[\u4e00-\u9fa5]"
    amap1 = ['', '万', '亿']
    amap2 = ['', '十', '百', '千']
    digit = {'0':'零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}
    tone = {'#2': 0, '#1': 0, '#4': 0, '#3': 0} # '#1', '#2', '#3', '#4'
    toneMap = { "ā": "a1", "á": "a2", "ǎ": "a3", "à": "a4", "ō": "o1", "ó": "o2", "ǒ": "o3", "ò": "o4", "ē": "e1", "é": "e2", "ě": "e3", "è": "e4",
		    "ī": "i1", "í": "i2", "ǐ": "i3", "ì": "i4", "ū": "u1", "ú": "u2", "ǔ": "u3", "ù": "u4", "ü": "v0", "ǖ": "v1", "ǘ": "v2", "ǚ": "v3",
		    "ǜ": "v4", "ń": "n2", "ň": "n3", "": "m2" }
