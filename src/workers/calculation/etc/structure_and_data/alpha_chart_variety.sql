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
-- Table structure for table `chart_variety`
--

DROP TABLE IF EXISTS `chart_variety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chart_variety` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange` varchar(45) NOT NULL,
  `variety` varchar(45) NOT NULL,
  `variety_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chart_variety`
--

LOCK TABLES `chart_variety` WRITE;
/*!40000 ALTER TABLE `chart_variety` DISABLE KEYS */;
INSERT INTO `chart_variety` VALUES (1,'SHFE','Cu','铜'),(2,'SHFE','Al','铝'),(3,'SHFE','Zn','锌'),(4,'SHFE','Pb','铅'),(5,'SHFE','Ni','镍'),(6,'SHFE','Rb','螺纹钢'),(7,'SHFE','Hc','热卷'),(8,'SHFE','Ru','橡胶'),(9,'DCE','Fe','铁矿'),(10,'DCE','Sl','塑料'),(11,'DCE','Jm','焦煤'),(12,'DCE','Jt','焦炭'),(13,'DCE','Dp','豆粕'),(14,'DCE','Jd','鸡蛋'),(15,'DCE','PP','PP'),(16,'DCE','PVC','PVC'),(17,'CZCE','PTA','PTA'),(18,'CZCE','Rm','菜粕'),(19,'CZCE','Ma','郑醇'),(20,'CZCE','Zc','郑煤');
/*!40000 ALTER TABLE `chart_variety` ENABLE KEYS */;
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
