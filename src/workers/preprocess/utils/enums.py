# -- coding: utf-8 --
from models.models import MinPreprocess, DayPreprocess, PreprocessDayCrossStar, \
                            PreprocessDayHlunDeff, PreprocessDayPositionChain, PreprocessDayStockRadio, \
                            PreprocessMinCrossStar, PreprocessMinHlunDeff, PreprocessDayShmetPriceDeff, \
                            PreprocessMinShmetPriceDeff, PreprocessDaySmmPriceDeff, PreprocessMinSmmPriceDeff, \
                            PreprocessDayWarehouseReceipts, PreprocessDayPositionDeff, PreprocessMinPositionDeff, \
                            PreprocessDaySmmSpotMonthDeff, PreprocessDaySmmSpotYearDeff, PreprocessDayShmetSpotMonthDeff, \
                            PreprocessDayShmetSpotYearDeff, PreprocessDayMonthWarehouseDeff, PreprocessDayDeliveryMonthPositionDeff,\
                            PreprocessDayDeliveryMonthBwdDeff, PreprocessDayDataArtificial


ALLOW_VARIETIES = [
    "cu",
    "zn",
    "al",
    "pb",
    "ni",
    "a", #豆一
    "ag", #沪银
    "au", #沪金
    "b", #豆二
    "bb", #胶板
    "bu", #沥青
    "c", #玉米
    "cf", #棉花
    "cs", #淀粉
    "fb", #纤板
    "fg", #玻璃
    "fu", #燃油
    "hc", #热卷
    "i", #铁矿
    "j", #焦炭
    "jd", #鸡蛋
    "jm", #焦煤
    "jr", #粳稻
    "l", #塑料
    "lr", #晚稻
    "m", #豆粕
    "ma", #郑醇
    "oi", #郑油
    "p", #棕榈
    "pm", #普麦
    "pp", #PP
    "rb", #螺纹
    "ri", #早稻
    "rm", #菜粕
    "rs", #菜籽
    "ru", #橡胶
    "sf", #硅铁
    "sm", #锰硅
    "sn", #沪锡
    "t", #十债
    "ta", #PTA
    "tf", #标胶20
    "v", #PVC
    "wh", #郑麦
    "wr", #线材
    "y", #豆油
    "zc", #郑煤
]
ALLOW_EXCHANGE = ['SHFE']

EXTRA_PRICE = {"cu":150, "ni":200, "al":100, "pb":100, "zn":100, "nife":600}

METAL_RATE_DICT = {
    "cu": 1,
    "zn": 1.01,
    "ni": 1.01,
    "al": 1,
    "pb": 1.03,
    "nife": 1.01,
}

CHANGE_DICT = {
    "0": 1,
    "1": 2/3,
    "2": 1/3,
    "3": 0,
    "4": -1/3,
    "5": -2/3,
    "6": -1,
    "7": -4/3,
    "8": -5/3,
    "9": -2,
    "10": -7/3,
    "11": -8/3,
    "12": -3,
}

PRE_SYMBOL = {
    "change": "000",
    "change_1m": "001",
    "change_2m": "002",
    "change_3m": "003",
    "change_6m": "004",
    "profit": "005",
    "profit_1m": "006",
    "profit_2m": "007",
    "profit_3m": "008",
    "profit_6m": "009",
    "import_cost": "010",
    "import_cost_1m": "011",
    "import_cost_2m": "012",
    "import_cost_3m": "013",
    "import_cost_6m": "014",
    "domestic_price": "015",
    "domestic_price_1m": "016",
    "domestic_price_2m": "017",
    "domestic_price_3m": "018",
    "domestic_price_6m": "019",
    "rate": "020",
    "rate_1m": "021",
    "rate_2m": "022",
    "rate_3m": "023",
    "rate_6m": "024",
    "no_exchange_rate": "025",
    "no_exchange_rate_1m": "026",
    "no_exchange_rate_2m": "027",
    "no_exchange_rate_3m": "028",
    "no_exchange_rate_6m": "029",
    "import_rate": "030",
    "import_rate_1m": "031",
    "import_rate_2m": "032",
    "import_rate_3m": "033",
    "import_rate_6m": "034",
    "hulun_1m": "035",
    "hulun_3m": "036",
    "basic_1_2": "037",
    "basic_1_3": "038",
    "basic_2_3": "039",

    'cross_star': '040', #十字星比值
    'hlun_price_diff': '041', #沪伦差价
    'position_chain': '042', #月持仓环比
    'stock_ratio': '043', #月库存环比

    "basic_1_2_rate": "044", #连一连二价差比
    "basic_1_3_rate": "045", #连一连三价差比
    "basic_2_3_rate": "046", #连二连三价差比

    'smm_spot_price_diff': '047', #有色网现货价差
    'shmet_spot_price_diff': '048', #上海金属网现货价差
    'warehouse_receipts': '049', #库存环比

    'position_deff': '050', #今天和昨天持仓差值(今天 - 昨天)

    'smm_spot_month_deff': '051', #有色网现货价格月差
    'smm_spot_year_deff': '052', #有色网现货价格年差
    'shmet_spot_month_deff': '053', #上海金属网现货价格月差
    'shmet_spot_year_deff': '054', #上海金属网现货价格年差
    'delivery_month_position_deff': '055', #持仓月差
    'month_warehouse_deff': '056', #仓单月差
    'delivery_month_bwd_deff': '057', #持仓月升贴水差

    'total_output': '058', #总产量

}

DAY_VARIEYIES_DICT = {
    "cu": "PE100",
    "zn": "PE101",
    "al": "PE102",
    "pb": "PE103",
    "ni": "PE104",
    # "a": "PE105", #豆一
    # "ag": "PE106", #沪银
    # "au": "PE107", #沪金
    # "b": "PE108", #豆二
    # "bb": "PE109", #胶板
    # "bu": "PE110", #沥青
    # "c": "PE111", #玉米
    # "cf": "PE112", #棉花
    # "cs": "PE113", #淀粉
    # "fb": "PE114", #纤板
    # "fg": "PE115", #玻璃
    # "fu": "PE116", #燃油
    "hc": "PE117", #热卷
    "i": "PE110", #铁矿
    "j": "PE119", #焦炭
    "jd": "PE120", #鸡蛋
    "jm": "PE121", #焦煤
    # "jr": "PE122", #粳稻
    "l": "PE123", #塑料
    # "lr": "PE124", #晚稻
    "m": "PE125", #豆粕
    "ma": "PE126", #甲醇
    # "oi": "PE127", #郑油
    # "p": "PE120", #棕榈
    # "pm": "PE129", #普麦
    "pp": "PE130", #PP
    "rb": "PE131", #螺纹
    # "ri": "PE132", #早稻
    "rm": "PE133", #菜粕
    # "rs": "PE134", #菜籽
    "ru": "PE135", #橡胶
    # "sf": "PE136", #硅铁
    # "sm": "PE137", #锰硅
    # "sn": "PE130", #沪锡
    # "t": "PE139", #十债
    "ta": "PE140", #PTA
    # "tf": "PE141", #标胶20
    "v": "PE142", #PVC
    # "wh": "PE143", #郑麦
    # "wr": "PE144", #线材
    # "y": "PE145", #豆油
    "zc": "PE146", #郑煤

}

MIN_VARIEYIES_DICT = {
    "cu": "PE000",
    "zn": "PE001",
    "al": "PE002",
    "pb": "PE003",
    "ni": "PE004",
    # "a": "PE005", #豆一
    # "ag": "PE006", #沪银
    # "au": "PE007", #沪金
    # "b": "PE008", #豆二
    # "bb": "PE009", #胶板
    # "bu": "PE010", #沥青
    # "c": "PE011", #玉米
    # "cf": "PE012", #棉花
    # "cs": "PE013", #淀粉
    # "fb": "PE014", #纤板
    # "fg": "PE015", #玻璃
    # "fu": "PE016", #燃油
    "hc": "PE017", #热卷
    "i": "PE010", #铁矿
    "j": "PE019", #焦炭
    "jd": "PE020", #鸡蛋
    "jm": "PE021", #焦煤
    # "jr": "PE022", #粳稻
    "l": "PE023", #塑料
    # "lr": "PE024", #晚稻
    "m": "PE025", #豆粕
    "ma": "PE026", #甲醇
    # "oi": "PE027", #郑油
    # "p": "PE020", #棕榈
    # "pm": "PE029", #普麦
    "pp": "PE030", #PP
    "rb": "PE031", #螺纹
    # "ri": "PE032", #早稻
    "rm": "PE033", #菜粕
    # "rs": "PE034", #菜籽
    "ru": "PE035", #橡胶
    # "sf": "PE036", #硅铁
    # "sm": "PE037", #锰硅
    # "sn": "PE030", #沪锡
    # "t": "PE039", #十债
    "ta": "PE040", #PTA
    # "tf": "PE041", #标胶20
    "v": "PE042", #PVC
    # "wh": "PE043", #郑麦
    # "wr": "PE044", #线材
    # "y": "PE045", #豆油
    "zc": "PE046", #郑煤

}

TCP_VARIEYIES_DICT = {
    "cu": "PE201",
    "zn": "PE211",
    "al": "PE221",
    "pb": "PE231",
    "ni": "PE241",
    # "a": "PE305", #豆一
    # "ag": "PE306", #沪银
    # "au": "PE307", #沪金
    # "b": "PE308", #豆二
    # "bb": "PE309", #胶板
    # "bu": "PE310", #沥青
    # "c": "PE311", #玉米
    # "cf": "PE312", #棉花
    # "cs": "PE313", #淀粉
    # "fb": "PE314", #纤板
    # "fg": "PE315", #玻璃
    # "fu": "PE316", #燃油
    "hc": "PE317", #热卷
    "i": "PE310", #铁矿
    "j": "PE319", #焦炭
    "jd": "PE320", #鸡蛋
    "jm": "PE321", #焦煤
    # "jr": "PE322", #粳稻
    "l": "PE323", #塑料
    # "lr": "PE324", #晚稻
    "m": "PE325", #豆粕
    "ma": "PE326", #郑醇
    # "oi": "PE327", #郑油
    # "p": "PE320", #棕榈
    # "pm": "PE329", #普麦
    "pp": "PE330", #PP
    "rb": "PE331", #螺纹
    # "ri": "PE332", #早稻
    "rm": "PE333", #菜粕
    # "rs": "PE334", #菜籽
    "ru": "PE335", #橡胶
    # "sf": "PE336", #硅铁
    # "sm": "PE337", #锰硅
    # "sn": "PE330", #沪锡
    # "t": "PE339", #十债
    "ta": "PE340", #PTA
    # "tf": "PE341", #标胶20
    "v": "PE342", #PVC
    # "wh": "PE343", #郑麦
    # "wr": "PE344", #线材
    # "y": "PE345", #豆油
    "zc": "PE346", #郑煤
}


COMMON_MIN_VARIEYIES_DICT = {
    "cu": "PE800",
    "zn": "PE801",
    "al": "PE802",
    "pb": "PE803",
    "ni": "PE804",
    "a": "PE805", #豆一
    "ag": "PE806", #沪银
    "au": "PE807", #沪金
    "b": "PE808", #豆二
    "bb": "PE809", #胶板
    "bu": "PE810", #沥青
    "c": "PE811", #玉米
    "cf": "PE812", #棉花
    "cs": "PE813", #淀粉
    "fb": "PE814", #纤板
    "fg": "PE815", #玻璃
    "fu": "PE816", #燃油
    "hc": "PE817", #热卷
    "i": "PE818", #铁矿
    "j": "PE819", #焦炭
    "jd": "PE820", #鸡蛋
    "jm": "PE821", #焦煤
    "jr": "PE822", #粳稻
    "l": "PE823", #塑料
    "lr": "PE824", #晚稻
    "m": "PE825", #豆粕
    "ma": "PE826", #郑醇
    "oi": "PE827", #郑油
    "p": "PE828", #棕榈
    "pm": "PE829", #普麦
    "pp": "PE830", #PP
    "rb": "PE831", #螺纹
    "ri": "PE832", #早稻
    "rm": "PE833", #菜粕
    "rs": "PE834", #菜籽
    "ru": "PE835", #橡胶
    "sf": "PE836", #硅铁
    "sm": "PE837", #锰硅
    "sn": "PE838", #沪锡
    "t": "PE839", #十债
    "ta": "PE840", #PTA
    "tf": "PE841", #标胶20
    "v": "PE842", #PVC
    "wh": "PE843", #郑麦
    "wr": "PE844", #线材
    "y": "PE845", #豆油
    "zc": "PE846", #郑煤
}


MIN_PARA_MODEL_MAP = {
    "change": MinPreprocess,
    "change_1m": MinPreprocess,
    "change_2m": MinPreprocess,
    "change_3m": MinPreprocess,
    "change_6m": MinPreprocess,
    "profit": MinPreprocess,
    "profit_1m": MinPreprocess,
    "profit_2m": MinPreprocess,
    "profit_3m": MinPreprocess,
    "profit_6m": MinPreprocess,
    "import_cost": MinPreprocess,
    "import_cost_1m": MinPreprocess,
    "import_cost_2m": MinPreprocess,
    "import_cost_3m": MinPreprocess,
    "import_cost_6m": MinPreprocess,
    "domestic_price": MinPreprocess,
    "domestic_price_1m": MinPreprocess,
    "domestic_price_2m": MinPreprocess,
    "domestic_price_3m": MinPreprocess,
    "domestic_price_6m": MinPreprocess,
    "rate": MinPreprocess,
    "rate_1m": MinPreprocess,
    "rate_2m": MinPreprocess,
    "rate_3m": MinPreprocess,
    "rate_6m": MinPreprocess,
    "no_exchange_rate": MinPreprocess,
    "no_exchange_rate_1m": MinPreprocess,
    "no_exchange_rate_2m": MinPreprocess,
    "no_exchange_rate_3m": MinPreprocess,
    "no_exchange_rate_6m": MinPreprocess,
    "import_rate": MinPreprocess,
    "import_rate_1m": MinPreprocess,
    "import_rate_2m": MinPreprocess,
    "import_rate_3m": MinPreprocess,
    "import_rate_6m": MinPreprocess,
    "hulun_1m": MinPreprocess,
    "hulun_3m": MinPreprocess,
    "basic_1_2": MinPreprocess,
    "basic_1_3": MinPreprocess,
    "basic_2_3": MinPreprocess,
    "basic_1_2_rate": MinPreprocess, #连一连二价差比
    "basic_1_3_rate": MinPreprocess, #连一连三价差比
    "basic_2_3_rate": MinPreprocess, #连二连三价差比

    'cross_star': PreprocessMinCrossStar,
    'hlun_price_diff': PreprocessMinHlunDeff,
    'position_chain': PreprocessDayPositionChain,
    'stock_ratio': PreprocessDayStockRadio,

    'smm_spot_price_diff': PreprocessMinSmmPriceDeff,
    'shmet_spot_price_diff': PreprocessMinShmetPriceDeff,

    'position_deff': PreprocessMinPositionDeff,

}


DAY_PARA_MODEL_MAP = {
    "change": DayPreprocess,
    "change_1m": DayPreprocess,
    "change_2m": DayPreprocess,
    "change_3m": DayPreprocess,
    "change_6m": DayPreprocess,
    "profit": DayPreprocess,
    "profit_1m": DayPreprocess,
    "profit_2m": DayPreprocess,
    "profit_3m": DayPreprocess,
    "profit_6m": DayPreprocess,
    "import_cost": DayPreprocess,
    "import_cost_1m": DayPreprocess,
    "import_cost_2m": DayPreprocess,
    "import_cost_3m": DayPreprocess,
    "import_cost_6m": DayPreprocess,
    "domestic_price": DayPreprocess,
    "domestic_price_1m": DayPreprocess,
    "domestic_price_2m": DayPreprocess,
    "domestic_price_3m": DayPreprocess,
    "domestic_price_6m": DayPreprocess,
    "rate": DayPreprocess,
    "rate_1m": DayPreprocess,
    "rate_2m": DayPreprocess,
    "rate_3m": DayPreprocess,
    "rate_6m": DayPreprocess,
    "no_exchange_rate": DayPreprocess,
    "no_exchange_rate_1m": DayPreprocess,
    "no_exchange_rate_2m": DayPreprocess,
    "no_exchange_rate_3m": DayPreprocess,
    "no_exchange_rate_6m": DayPreprocess,
    "import_rate": DayPreprocess,
    "import_rate_1m": DayPreprocess,
    "import_rate_2m": DayPreprocess,
    "import_rate_3m": DayPreprocess,
    "import_rate_6m": DayPreprocess,
    "hulun_1m": DayPreprocess,
    "hulun_3m": DayPreprocess,
    "basic_1_2": DayPreprocess,
    "basic_1_3": DayPreprocess,
    "basic_2_3": DayPreprocess,
    "basic_1_2_rate": DayPreprocess, #连一连二价差比
    "basic_1_3_rate": DayPreprocess, #连一连三价差比
    "basic_2_3_rate": DayPreprocess, #连二连三价差比

    'cross_star': PreprocessDayCrossStar,
    'hlun_price_diff': PreprocessDayHlunDeff,
    'position_chain': PreprocessDayPositionChain,
    'stock_ratio': PreprocessDayStockRadio,

    'smm_spot_price_diff': PreprocessDaySmmPriceDeff,
    'shmet_spot_price_diff': PreprocessDayShmetPriceDeff,
    'warehouse_receipts': PreprocessDayWarehouseReceipts,

    'position_deff': PreprocessDayPositionDeff,

    'smm_spot_month_deff': PreprocessDaySmmSpotMonthDeff,  # 有色网现货价格月差
    'smm_spot_year_deff': PreprocessDaySmmSpotYearDeff,  # 有色网现货价格年差
    'shmet_spot_month_deff': PreprocessDayShmetSpotMonthDeff,  # 上海金属网现货价格月差
    'shmet_spot_year_deff': PreprocessDayShmetSpotYearDeff,  # 上海金属网现货价格年差
    'delivery_month_position_deff': PreprocessDayDeliveryMonthPositionDeff,  # 持仓月差
    'month_warehouse_deff': PreprocessDayMonthWarehouseDeff,  # 仓单月差
    'delivery_month_bwd_deff': PreprocessDayDeliveryMonthBwdDeff, #升贴水持仓月差
    'total_output': PreprocessDayDataArtificial, #总产量

}



PRODUCT_CLASS_MAP = {
# CU 沪铜，AL 沪铝，PB 沪铅，ZN 沪锌，NI 沪镍
    'cu': '1', #有色金属
    'al': '1', #有色金属
    'pb': '1', #有色金属
    'zn': '1', #有色金属
    'ni': '1', #有色金属
# HC 热卷，RB 螺纹，I 铁矿，J 焦炭，JM 焦煤
    'hc': '2', #黑色
    'rb': '2', #黑色
    'i': '2', #黑色
    'j': '2', #黑色
    'jm': '2', #黑色
# MA 甲醇，TA PTA，L 乙烯，PP 丙烯，V PVC，RU 橡胶
    'ma': '3', #化工
    'ta': '3', #化工
    'l': '3', #化工
    'pp': '3', #化工
    'v': '3', #化工
    'ru': '3', #化工
# C 玉米，M 豆粕，RM 菜粕，JD 鸡蛋
# CS 淀粉，Y 豆油，OI 菜油，P 棕榈油
    'c': '4', #农产品
    'm': '4', #农产品
    'rm': '4', #农产品
    'jd': '4', #农产品
    'cs': '4', #农产品
    'y': '4', #农产品
    'oi': '4', #农产品
    'p': '4', #农产品

}

OUTPUT_SYMBOL_MAP = {
    'cu': 'S0116244',
    'al': 'S0027567',
    'zn': 'S5808351',
    'pb': 'S0027579',
}

IMPORT_AMOUNT_MAP = {
    'cu': 'S0027555',
    'al': 'S0116254',
    'zn': 'S0116262',
    'pb': 'S0116260',
}