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
-- Table structure for table `varieties_record`
--

DROP TABLE IF EXISTS `varieties_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `varieties_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) CHARACTER SET latin1 NOT NULL,
  `exchange` varchar(10) CHARACTER SET latin1 NOT NULL,
  `short_name` varchar(10) DEFAULT NULL,
  `long_name` varchar(20) DEFAULT NULL,
  `display_name` varchar(32) DEFAULT NULL,
  `is_disabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `varieties_record`
--

LOCK TABLES `varieties_record` WRITE;
/*!40000 ALTER TABLE `varieties_record` DISABLE KEYS */;
INSERT INTO `varieties_record` VALUES (1,'al','SHFE','沪铝','铝','沪铝',0),(2,'cu','SHFE','沪铜','铜','沪铜',0),(3,'hc','SHFE','热卷','热轧板','热卷',0),(4,'i','DCE','铁矿','铁矿石','铁矿',0),(5,'j','DCE','焦炭','焦炭','焦炭',0),(6,'jd','DCE','鸡蛋','鲜鸡蛋','鸡蛋',0),(7,'jm','DCE','焦煤','焦煤','焦煤',0),(8,'l','DCE','塑料','聚乙烯','塑料',0),(9,'m','DCE','豆粕','豆粕','豆粕',0),(10,'ni','SHFE','沪镍','镍','沪镍',0),(11,'pb','SHFE','沪铅','铅','沪铅',0),(12,'pp','DCE','PP','聚丙烯','PP',0),(13,'rb','SHFE','螺纹','螺纹钢','螺纹',0),(14,'RM','CZCE','菜粕','菜籽粕','菜粕',0),(15,'ru','SHFE','橡胶','天然橡胶','橡胶',0),(16,'TA','CZCE','PTA','化纤','PTA',0),(17,'zn','SHFE','沪锌','锌','沪锌',0);
/*!40000 ALTER TABLE `varieties_record` ENABLE KEYS */;
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
