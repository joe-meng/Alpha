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
-- Table structure for table `chart_sidebar`
--

DROP TABLE IF EXISTS `chart_sidebar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chart_sidebar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange` varchar(45) NOT NULL,
  `variety` varchar(45) NOT NULL,
  `sidebar` varchar(45) NOT NULL,
  `sidebar_name` varchar(45) NOT NULL,
  `panorama` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chart_sidebar`
--

LOCK TABLES `chart_sidebar` WRITE;
/*!40000 ALTER TABLE `chart_sidebar` DISABLE KEYS */;
INSERT INTO `chart_sidebar` VALUES (1,'SHFE','Cu','spot','现货报价',0),(2,'SHFE','Cu','position','期货持仓',0),(3,'SHFE','Cu','stock','库存',0),(4,'SHFE','Cu','basis','基差',0),(5,'SHFE','Cu','e_and_i','进出口',0),(6,'SHFE','Cu','p_and_s','产销量',0),(7,'SHFE','Cu','process_cost','加工费',0),(8,'SHFE','Cu','copper_price','废铜价格',0),(9,'SHFE','Cu','e_and_i_pl','进出口盈亏',0),(10,'SHFE','Cu','exchage_rate','汇率',0),(11,'SHFE','Cu','tc_rc','TC/RC',0),(12,'SHFE','Cu','panorama_1','期货/库存[期货主力合约价格]',1),(13,'SHFE','Cu','panorama_2','期货/现货',1),(14,'SHFE','Cu','panorama_3','年库存对比',1),(15,'SHFE','Cu','panorama_4','当月升贴水/上月升贴水/n-2升贴水',1),(16,'SHFE','Cu','panorama_5','沪伦比值',1),(17,'SHFE','Cu','panorama_6','基差',1),(18,'SHFE','Cu','panorama_7','产销',1),(19,'SHFE','Cu','panorama_8','TC/RC',1),(20,'SHFE','Al','spot','现货报价',0),(21,'SHFE','Al','position','期货持仓',0),(22,'SHFE','Al','stock','库存',0),(23,'SHFE','Al','basis','基差',0),(24,'SHFE','Al','e_and_i','进出口',0),(25,'SHFE','Al','p_and_s','产销量',0),(26,'SHFE','Al','process_cost','加工费',0),(27,'SHFE','Al','alumina_price','氧化铝价格',0),(28,'SHFE','Al','e_and_i_pl','进出口盈亏',0),(29,'SHFE','Al','exchage_rate','汇率',0),(30,'SHFE','Al','tc_rc','TC/RC',0),(31,'SHFE','Al','panorama_1','期货/库存[期货主力合约价格]',1),(32,'SHFE','Al','panorama_2','期货/现货',1),(33,'SHFE','Al','panorama_3','年库存对比',1),(34,'SHFE','Al','panorama_4','当月升贴水/上月升贴水/n-2升贴水',1),(35,'SHFE','Al','panorama_5','沪伦比值',1),(36,'SHFE','Al','panorama_6','基差',1),(37,'SHFE','Al','panorama_7','产销',1),(38,'SHFE','Al','panorama_8','TC/RC',1),(39,'SHFE','Zn','spot','现货报价',0),(40,'SHFE','Zn','position','期货持仓',0),(41,'SHFE','Zn','stock','库存',0),(42,'SHFE','Zn','basis','基差',0),(43,'SHFE','Zn','e_and_i','进出口',0),(44,'SHFE','Zn','p_and_s','产销量',0),(45,'SHFE','Zn','process_cost','加工费',0),(46,'SHFE','Zn','e_and_i_pl','进出口盈亏',0),(47,'SHFE','Zn','exchage_rate','汇率',0),(48,'SHFE','Zn','tc_rc','TC/RC',0),(49,'SHFE','Zn','panorama_1','期货/库存[期货主力合约价格]',1),(50,'SHFE','Zn','panorama_2','期货/现货',1),(51,'SHFE','Zn','panorama_3','年库存对比',1),(52,'SHFE','Zn','panorama_4','当月升贴水/上月升贴水/n-2升贴水',1),(53,'SHFE','Zn','panorama_5','沪伦比值',1),(54,'SHFE','Zn','panorama_6','基差',1),(55,'SHFE','Zn','panorama_7','产销',1),(56,'SHFE','Zn','panorama_8','TC/RC',1),(57,'SHFE','Pb','spot','现货报价',0),(58,'SHFE','Pb','position','期货持仓',0),(59,'SHFE','Pb','stock','库存',0),(60,'SHFE','Pb','basis','基差',0),(61,'SHFE','Pb','exchage_rate','汇率',0),(62,'SHFE','Pb','panorama_1','期货/库存[期货主力合约价格]',1),(63,'SHFE','Pb','panorama_2','期货/现货',1),(64,'SHFE','Pb','panorama_3','年库存对比',1),(65,'SHFE','Pb','panorama_4','当月升贴水/上月升贴水/n-2升贴水',1),(66,'SHFE','Pb','panorama_6','基差',1),(67,'SHFE','Ni','spot','现货报价',0),(68,'SHFE','Ni','position','期货持仓',0),(69,'SHFE','Ni','stock','库存',0),(70,'SHFE','Ni','basis','基差',0),(71,'SHFE','Ni','e_and_i','进出口',0),(72,'SHFE','Ni','p_and_s','产销量',0),(73,'SHFE','Ni','e_and_i_pl','进出口盈亏',0),(74,'SHFE','Ni','exchage_rate','汇率',0),(75,'SHFE','Ni','panorama_1','期货/库存[期货主力合约价格]',1),(76,'SHFE','Ni','panorama_2','期货/现货',1),(77,'SHFE','Ni','panorama_3','年库存对比',1),(78,'SHFE','Ni','panorama_4','当月升贴水/上月升贴水/n-2升贴水',1),(79,'SHFE','Ni','panorama_5','沪伦比值',1),(80,'SHFE','Ni','panorama_6','基差',1),(81,'SHFE','Ni','panorama_7','产销',1),(82,'SHFE','Ni','panorama_8','TC/RC',1),(83,'SHFE','Rb','spot','现货报价',0),(84,'SHFE','Rb','position','期货持仓',0),(85,'SHFE','Rb','stock','库存',0),(86,'SHFE','Rb','basis','基差',0),(87,'SHFE','Rb','panorama_1','期货/库存[期货主力合约价格]',1),(88,'SHFE','Rb','panorama_2','期货/现货',1),(89,'SHFE','Rb','panorama_3','年库存对比',1),(90,'SHFE','Rb','panorama_6','基差',1),(91,'SHFE','Hc','spot','现货报价',0),(92,'SHFE','Hc','position','期货持仓',0),(93,'SHFE','Hc','stock','库存',0),(94,'SHFE','Hc','basis','基差',0),(95,'SHFE','Hc','panorama_1','期货/库存[期货主力合约价格]',1),(96,'SHFE','Hc','panorama_2','期货/现货',1),(97,'SHFE','Hc','panorama_3','年库存对比',1),(98,'SHFE','Hc','panorama_6','基差',1),(99,'SHFE','Ru','spot','现货报价',0),(100,'SHFE','Ru','position','期货持仓',0),(101,'SHFE','Ru','stock','库存',0),(102,'SHFE','Ru','basis','基差',0),(103,'SHFE','Ru','panorama_1','期货/库存[期货主力合约价格]',1),(104,'SHFE','Ru','panorama_2','期货/现货',1),(105,'SHFE','Ru','panorama_3','年库存对比',1),(106,'SHFE','Ru','panorama_6','基差',1),(107,'DCE','Fe','spot','现货报价',0),(108,'DCE','Fe','position','期货持仓',0),(109,'DCE','Fe','stock','库存',0),(110,'DCE','Fe','basis','基差',0),(111,'DCE','Fe','panorama_1','期货/库存[期货主力合约价格]',1),(112,'DCE','Fe','panorama_2','期货/现货',1),(113,'DCE','Fe','panorama_3','年库存对比',1),(114,'DCE','Fe','panorama_6','基差',1),(115,'DCE','Sl','spot','现货报价',0),(116,'DCE','Sl','position','期货持仓',0),(117,'DCE','Sl','stock','库存',0),(118,'DCE','Sl','basis','基差',0),(119,'DCE','Sl','panorama_1','期货/库存[期货主力合约价格]',1),(120,'DCE','Sl','panorama_2','期货/现货',1),(121,'DCE','Sl','panorama_3','年库存对比',1),(122,'DCE','Sl','panorama_6','基差',1),(123,'DCE','Jm','spot','现货报价',0),(124,'DCE','Jm','position','期货持仓',0),(125,'DCE','Jm','stock','库存',0),(126,'DCE','Jm','basis','基差',0),(127,'DCE','Jm','panorama_1','期货/库存[期货主力合约价格]',1),(128,'DCE','Jm','panorama_2','期货/现货',1),(129,'DCE','Jm','panorama_3','年库存对比',1),(130,'DCE','Jm','panorama_6','基差',1),(131,'DCE','Jt','spot','现货报价',0),(132,'DCE','Jt','position','期货持仓',0),(133,'DCE','Jt','stock','库存',0),(134,'DCE','Jt','basis','基差',0),(135,'DCE','Jt','panorama_1','期货/库存[期货主力合约价格]',1),(136,'DCE','Jt','panorama_2','期货/现货',1),(137,'DCE','Jt','panorama_3','年库存对比',1),(138,'DCE','Jt','panorama_6','基差',1),(139,'DCE','Dp','spot','现货报价',0),(140,'DCE','Dp','position','期货持仓',0),(141,'DCE','Dp','stock','库存',0),(142,'DCE','Dp','basis','基差',0),(143,'DCE','Dp','panorama_1','期货/库存[期货主力合约价格]',1),(144,'DCE','Dp','panorama_2','期货/现货',1),(145,'DCE','Dp','panorama_3','年库存对比',1),(146,'DCE','Dp','panorama_6','基差',1),(147,'DCE','Jd','spot','现货报价',0),(148,'DCE','Jd','position','期货持仓',0),(149,'DCE','Jd','stock','库存',0),(150,'DCE','Jd','basis','基差',0),(151,'DCE','Jd','panorama_1','期货/库存[期货主力合约价格]',1),(152,'DCE','Jd','panorama_2','期货/现货',1),(153,'DCE','Jd','panorama_3','年库存对比',1),(154,'DCE','Jd','panorama_6','基差',1),(155,'DCE','PP','spot','现货报价',0),(156,'DCE','PP','position','期货持仓',0),(157,'DCE','PP','stock','库存',0),(158,'DCE','PP','basis','基差',0),(159,'DCE','PP','panorama_1','期货/库存[期货主力合约价格]',1),(160,'DCE','PP','panorama_2','期货/现货',1),(161,'DCE','PP','panorama_3','年库存对比',1),(162,'DCE','PP','panorama_6','基差',1),(163,'DCE','PVC','spot','现货报价',0),(164,'DCE','PVC','position','期货持仓',0),(165,'DCE','PVC','stock','库存',0),(166,'DCE','PVC','basis','基差',0),(167,'DCE','PVC','panorama_1','期货/库存[期货主力合约价格]',1),(168,'DCE','PVC','panorama_2','期货/现货',1),(169,'DCE','PVC','panorama_3','年库存对比',1),(170,'DCE','PVC','panorama_6','基差',1),(171,'CZCE','PTA','spot','现货报价',0),(172,'CZCE','PTA','position','期货持仓',0),(173,'CZCE','PTA','stock','库存',0),(174,'CZCE','PTA','basis','基差',0),(175,'CZCE','PTA','panorama_1','期货/库存[期货主力合约价格]',1),(176,'CZCE','PTA','panorama_2','期货/现货',1),(177,'CZCE','PTA','panorama_3','年库存对比',1),(178,'CZCE','PTA','panorama_6','基差',1),(179,'CZCE','Rm','spot','现货报价',0),(180,'CZCE','Rm','position','期货持仓',0),(181,'CZCE','Rm','stock','库存',0),(182,'CZCE','Rm','basis','基差',0),(183,'CZCE','Rm','panorama_1','期货/库存[期货主力合约价格]',1),(184,'CZCE','Rm','panorama_2','期货/现货',1),(185,'CZCE','Rm','panorama_3','年库存对比',1),(186,'CZCE','Rm','panorama_6','基差',1),(187,'CZCE','Ma','spot','现货报价',0),(188,'CZCE','Ma','position','期货持仓',0),(189,'CZCE','Ma','stock','库存',0),(190,'CZCE','Ma','basis','基差',0),(191,'CZCE','Ma','panorama_1','期货/库存[期货主力合约价格]',1),(192,'CZCE','Ma','panorama_2','期货/现货',1),(193,'CZCE','Ma','panorama_3','年库存对比',1),(194,'CZCE','Ma','panorama_6','基差',1),(195,'CZCE','Zc','spot','现货报价',0),(196,'CZCE','Zc','position','期货持仓',0),(197,'CZCE','Zc','stock','库存',0),(198,'CZCE','Zc','basis','基差',0),(199,'CZCE','Zc','panorama_1','期货/库存[期货主力合约价格]',1),(200,'CZCE','Zc','panorama_2','期货/现货',1),(201,'CZCE','Zc','panorama_3','年库存对比',1),(202,'CZCE','Zc','panorama_6','基差',1);
/*!40000 ALTER TABLE `chart_sidebar` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-22 17:00:23
