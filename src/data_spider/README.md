# What
数据爬虫


# Usage
使用时需要指定 DJANGO_SETTINGS_MODULE 为 `alpha.settings.env`, 其中 env 为 defaults / develop / test / prod


# 数据来源以及品类
上期所: 铜 铝 锌 铅 镍 螺纹 橡胶 热卷
郑交所: PTA() 菜粕(菜籽粕RM)
大交所: 焦煤 焦炭 铁矿石 豆粕 鸡蛋 PP(聚丙烯) PVC(聚氯乙烯) PE(聚乙烯)
国内品种：铜铝锌铅镍、焦煤、焦炭、铁矿、螺纹、热卷、橡胶、塑料、PTA、PP、豆粕、菜粕、鸡蛋
国外品种（可以与国内联动显示）：
SGX：铁矿FE，TSR20
LME：铜、铝、铅、锌、镍
CMX：金、银、铜
TSR20是天然橡胶
