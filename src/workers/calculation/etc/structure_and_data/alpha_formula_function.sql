-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: 172.16.88.140    Database: alpha
-- ------------------------------------------------------
-- Server version	5.5.52-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `formula_function`
--

DROP TABLE IF EXISTS `formula_function`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `formula_function` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据插入时间',
  `updated_at` datetime NOT NULL,
  `function_name` longtext,
  `title` varchar(64) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formula_function`
--

LOCK TABLES `formula_function` WRITE;
/*!40000 ALTER TABLE `formula_function` DISABLE KEYS */;
INSERT INTO `formula_function` VALUES (1,'2017-08-08 09:01:29','0000-00-00 00:00:00','KOPEN','获取K线图的开盘价','KOPEN(e)\n获取K线图的开盘价(当天最后的一条开盘价)'),(2,'2017-08-08 09:01:29','0000-00-00 00:00:00','KCLOSE','获取K线图的收盘价','KCLOSE(e)\n获取K线图的开盘价(当天最后的一条收盘价)'),(3,'2017-08-08 09:01:29','0000-00-00 00:00:00','KHIGH','获取K线图的最高价','KHIGH(e)\n获取K线图的最高价(当天最后的一条最高价)'),(4,'2017-08-08 09:01:29','0000-00-00 00:00:00','KLOW','获取K线图的最低价','KLOW(e)\n获取K线图的最低价(当天最后的一条最低价)'),(5,'2017-08-08 09:01:29','0000-00-00 00:00:00','KSETTLE','获取k线图的结算价或者取得当时成交均价','KSETTLE(e)\n获取K线图的结算价或者取得当时成交均价'),(6,'2017-08-08 09:01:29','0000-00-00 00:00:00','KVOL','取得K线图的成交量','KVOL(e)\n取得K线图的成交量'),(7,'2017-08-08 09:01:29','0000-00-00 00:00:00','KOPI','获取K线图的持仓量','KOPI(e)\n获取K线图的持仓量'),(8,'2017-08-08 09:01:29','0000-00-00 00:00:00','KSTOCK','获取K线图库存','KSTOCK(e)\n获取K线图库存(注意是每周)=仓单+不可交割库存'),(9,'2017-08-08 09:01:29','0000-00-00 00:00:00','KWARRANT','获取K线图仓单','KWARRANT(e)\n获取K线图仓单(注意是每周)'),(10,'2017-08-08 09:01:29','0000-00-00 00:00:00','KCONTRACT','获取K线图当前合约名称','KCONTRACT(e)\n获取K线图当前合约名称'),(11,'2017-08-08 09:01:29','0000-00-00 00:00:00','KFUTURES','获取K线图当前品种名称','KFUTURES(e)\n获取K线图当前品种名称'),(12,'2017-08-08 09:01:29','0000-00-00 00:00:00','KMARKET','获取K线图当前市场名称','KMARKET(e)\n获取K线图当前市场名称'),(13,'2017-08-08 09:01:29','0000-00-00 00:00:00','KSPOT','获取K线图现货名称','KSPOT(e)\n获取K线图现货名称'),(14,'2017-08-08 09:01:29','0000-00-00 00:00:00','KPD','获取K线图现货升贴水','KPD(e)\n获取K线图现货升贴水'),(15,'2017-08-08 09:10:13','0000-00-00 00:00:00','ABS','取的X的绝对值','ABS(e)\n取的X的绝对值'),(16,'2017-08-08 09:10:13','0000-00-00 00:00:00','SQRT','求X的平方根','SQRT(e)\n求X的平方根'),(17,'2017-08-08 09:10:13','0000-00-00 00:00:00','HHV','求N个周期内的最高值。','HHV(e, price_code, n)\n求price_code在N个周期内的最高值。'),(18,'2017-08-08 09:10:13','0000-00-00 00:00:00','LLV','求N个周期内的最小值。','LLV(e, price_code, n)\n求price_code在N个周期内的最小值。'),(19,'2017-08-08 09:10:13','0000-00-00 00:00:00','MAX','取最大值','MAX(a, b)\n取最大值。取a, b中较大者。'),(20,'2017-08-08 09:10:13','0000-00-00 00:00:00','MIN','取最小值','MIN(a, b)\n取最小值。取a, b中较小者。'),(21,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISDOWN','判断该周期是否收阴','ISDOWN(e)\n判断该周期是否收阴'),(22,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISEQUAL','判断该周期是是否平盘,即十字星','ISEQUAL(e)\n判断该周期是是否平盘,即十字星'),(23,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISUP','判断该周期是否收阳','ISUP(e)\n判断该周期是否收阳'),(24,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISCONTUP','是否持续上升(百分比)','ISCONTUP(data, inter_interval_rate=None, all_rate=None)\n判断是否持续上升'),(25,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISCONTDOWN','是否持续下降(百分比)','ISCONTDOWN(data, inter_interval_rate=None, all_rate=None)\n是否持续下降'),(26,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISCONTUPABS','是否持续上升(绝对值)','ISCONTUPABS(data, inter_interval_rate=None, all_rate=None)\n是否持续上升'),(27,'2017-08-08 09:46:11','0000-00-00 00:00:00','ISCONTDOWNABS','是否持续下降(绝对值)','ISCONTDOWNABS(data, interval_abs=None, all_abs=None)\n是否持续下降'),(28,'2017-08-08 09:46:11','0000-00-00 00:00:00','CONTUPDETAIL','获取持续上升具体数据','CONTUPDETAIL(data, interval_abs=None, all_abs=None)\n获取持续上升具体数据'),(29,'2017-08-10 08:45:12','0000-00-00 00:00:00','REF','向前引用数据','REF(e, price_code, n=0, **kwargs)\n向前引用，取得前n根K线数据，返回一维数组'),(30,'2017-08-10 08:45:12','0000-00-00 00:00:00','REFD','向前引用数据,返回值带日期','REFD(e, price_code, n=0, **kwargs)\n向前引用,返回值带日期, 取得前一根K线数据，返回一维数组'),(31,'2017-08-10 08:45:12','0000-00-00 00:00:00','ISCONTRACT','判断是否当前合约','ISCONTRACT(e, con_code, con_name)\n判断是否当前合约,是当前合约返回1，不是当前合约返回0。'),(32,'2017-08-10 08:45:12','0000-00-00 00:00:00','WEEKDAY','取当天是星期几，返回0-6','WEEKDAY(e, date)\n取当天是星期几，返回0-6'),(33,'2017-08-10 08:45:12','0000-00-00 00:00:00','CURRENTDATE','取当前年月日','CURRENTDATE(e)\n取当前年月日'),(34,'2017-08-10 08:45:12','0000-00-00 00:00:00','GETPRICE','返回合约code的二维数组','GETPRICE(e, contract, price_code, date_from, date_end)\n返回二维数组'),(35,'2017-08-10 08:45:12','0000-00-00 00:00:00','DOMINANT','取主力合约','DOMINANT(e)\n取主力合约'),(36,'2017-08-10 08:45:12','0000-00-00 00:00:00','CONTCONTRACT','获取连续合约的编码','CONTCONTRACT(e, n=1)\n获取连续合约的编码\n参数n表示连一、连二等，连一指的是离交割最近的月份'),(37,'2017-08-10 08:45:12','0000-00-00 00:00:00','DAYSTOEXPIRED','期货合约距最后交易日的天数','DAYSTOEXPIRED(e, contract)\n获取连续合约的编码，\ncontract:表示连一、连二等，连一指的是离交割最近的月份'),(38,'2017-08-10 08:45:12','0000-00-00 00:00:00','ALERT','设置发出警告','ALERT(e, message, alert=True)\n设置发出警告,  message:警告包含的消息. alert是否发出警告'),(39,'2017-08-22 07:32:27','0000-00-00 00:00:00','CHART','设置警告图表数据','CHART(e, price_code, contract=MAIN_CONTRACT)\n设置图表展示的数据\ncontract:合约');
/*!40000 ALTER TABLE `formula_function` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-22 17:00:22
