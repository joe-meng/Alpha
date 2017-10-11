# 2017-7-13
ALTER TABLE `alpha`.`alert_alert`
ADD COLUMN `variety` VARCHAR(10) NOT NULL AFTER `is_pushed`,
ADD COLUMN `price` VARCHAR(30) NOT NULL AFTER `variety`;

# 2017-7-14
ALTER TABLE `alpha`.`alert_alert`
CHANGE COLUMN `user_id` `user_id` VARCHAR(11) NOT NULL DEFAULT '' ;

# 2017-7-17
ALTER TABLE `alpha`.`alert_alert`
ADD COLUMN `exchange` VARCHAR(10) NULL DEFAULT NULL AFTER `price`,
ADD COLUMN `source` VARCHAR(45) NULL DEFAULT NULL AFTER `exchange`;


# 2017-7-19
CREATE TABLE `alpha`.`day_basis` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `varieties` VARCHAR(16) NULL DEFAULT NULL,
  `amount` DOUBLE NULL DEFAULT NULL,
  `desc` VARCHAR(30) NULL DEFAULT NULL,
  `symbol` VARCHAR(64) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`));
ALTER TABLE `alpha`.`day_basis`
ADD COLUMN `date` DATE NOT NULL AFTER `symbol`;



INSERT INTO `alpha`.`symbol` (`title`, `symbol`, `table_name`, `unit`, `source`, `duration_unit`, `varieties`) VALUES ('基差:铜:连一连二', 'PE001037', 'day_preprocess', '元/吨', '预计算', 'd', 'Cu');
INSERT INTO `alpha`.`symbol` (`title`, `symbol`, `table_name`, `unit`, `source`, `duration_unit`, `varieties`) VALUES ('基差:铜:连一连三', 'PE001038', 'day_preprocess', '元/吨', '预计算', 'd', 'Cu');
INSERT INTO `alpha`.`symbol` (`title`, `symbol`, `table_name`, `unit`, `source`, `duration_unit`, `varieties`) VALUES ('基差:铜:连二连三', 'PE001039', 'day_preprocess', '元/吨', '预计算', 'd', 'Cu');

# cu连一连二差值
insert into day_basis (`date`, `amount`, `desc`, `symbol`, `varieties`)
select a.settlement_date, (a.settlement_price-b.settlement_price) as amount, '连一连二差值', 'PE001037', 'Cu' from (select a.settlement_date, a.serial_contract1, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract1=b.contract
and a.settlement_date=b.date_time
where varieties='cu') as a left join
(select a.settlement_date, a.serial_contract2, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract2=b.contract
and a.settlement_date=b.date_time
where varieties='cu') as b on a.settlement_date=b.settlement_date;

# cu连一连三差值
insert into day_basis (`date`, `amount`, `desc`, `symbol`, `varieties`)
select a.settlement_date, (a.settlement_price-b.settlement_price) as amount, '连一连三差值', 'PE001038', 'Cu' from (select a.settlement_date, a.serial_contract1, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract1=b.contract
and a.settlement_date=b.date_time
where varieties='cu') as a left join
(select a.settlement_date, a.serial_contract3, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract3=b.contract
and a.settlement_date=b.date_time
where varieties='cu') as b on a.settlement_date=b.settlement_date;

# cu连二连三差值
insert into day_basis (`date`, `amount`, `desc`, `symbol`, `varieties`)
select a.settlement_date, (a.settlement_price-b.settlement_price) as amount, '连二连三差值', 'PE001039', 'Cu' from (select a.settlement_date, a.serial_contract2, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract2=b.contract
and a.settlement_date=b.date_time
where varieties='cu') as a left join
(select a.settlement_date, a.serial_contract3, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract3=b.contract
and a.settlement_date=b.date_time
where varieties='cu') as b on a.settlement_date=b.settlement_date;


INSERT INTO `alpha`.`symbol` (`title`, `symbol`, `table_name`, `unit`, `source`, `duration_unit`, `varieties`) VALUES ('基差:锌:连一连二', 'PE011037', 'day_preprocess', '元/吨', '预计算', 'd', 'Zn');
INSERT INTO `alpha`.`symbol` (`title`, `symbol`, `table_name`, `unit`, `source`, `duration_unit`, `varieties`) VALUES ('基差:锌:连一连三', 'PE011038', 'day_preprocess', '元/吨', '预计算', 'd', 'Zn');
INSERT INTO `alpha`.`symbol` (`title`, `symbol`, `table_name`, `unit`, `source`, `duration_unit`, `varieties`) VALUES ('基差:锌:连一连三', 'PE011039', 'day_preprocess', '元/吨', '预计算', 'd', 'Zn');

# zn连一连二差值
insert into day_basis (`date`, `amount`, `desc`, `symbol`, `varieties`)
select a.settlement_date, (a.settlement_price-b.settlement_price) as amount, '连一连二差值', 'PE011037', 'Zn' from (select a.settlement_date, a.serial_contract1, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract1=b.contract
and a.settlement_date=b.date_time
where varieties='zn') as a left join
(select a.settlement_date, a.serial_contract2, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract2=b.contract
and a.settlement_date=b.date_time
where varieties='zn') as b on a.settlement_date=b.settlement_date;

# zn连一连三差值
insert into day_basis (`date`, `amount`, `desc`, `symbol`, `varieties`)
select a.settlement_date, (a.settlement_price-b.settlement_price) as amount, '连一连三差值', 'PE011038', 'Zn' from (select a.settlement_date, a.serial_contract1, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract1=b.contract
and a.settlement_date=b.date_time
where varieties='zn') as a left join
(select a.settlement_date, a.serial_contract3, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract3=b.contract
and a.settlement_date=b.date_time
where varieties='zn') as b on a.settlement_date=b.settlement_date;

# zn连二连三差值
select a.settlement_date, (a.settlement_price-b.settlement_price) as amount, '连二连三差值', 'PE011039', 'Zn' from (select a.settlement_date, a.serial_contract2, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract2=b.contract
and a.settlement_date=b.date_time
where varieties='zn') as a left join
(select a.settlement_date, a.serial_contract3, b.settlement_price from main_contract as a left join day_kline as b on a.serial_contract3=b.contract
and a.settlement_date=b.date_time
where varieties='zn') as b on a.settlement_date=b.settlement_date;



UPDATE `alpha`.`symbol` SET `column`='price' WHERE `symbol`='USE00045';
UPDATE `alpha`.`symbol` SET `column`='price' WHERE `symbol`='USE00046';
UPDATE `alpha`.`symbol` SET `column`='price' WHERE `symbol`='USE00150';
UPDATE `alpha`.`symbol` SET `column`='price' WHERE `symbol`='USE00145';
UPDATE `alpha`.`symbol` SET `varieties`='Zn' WHERE `symbol`='USE00150';
