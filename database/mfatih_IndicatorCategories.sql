CREATE DATABASE  IF NOT EXISTS `wdi` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `wdi`;
-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (arm64)
--
-- Host: localhost    Database: wdi
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'f77dd534-bf1f-11f0-a6d0-f71997ab92db:1-115';

--
-- Table structure for table `IndicatorCategories`
--

DROP TABLE IF EXISTS `IndicatorCategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `IndicatorCategories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(150) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `IndicatorCategories`
--

LOCK TABLES `IndicatorCategories` WRITE;
/*!40000 ALTER TABLE `IndicatorCategories` DISABLE KEYS */;
INSERT INTO `IndicatorCategories` VALUES (1,'Agriculture & Rural Development  ',NULL),(2,'Aid Effectiveness ',NULL),(3,'Economy & Growth',NULL),(4,'Education ',NULL),(5,'Energy & Mining ',NULL),(6,'Environment ',NULL),(7,'Financial Sector ',NULL),(9,'Infrastructure ',NULL),(10,'Social Protection & Labor',NULL),(11,'Poverty ',NULL),(12,'Private Sector',NULL),(13,'Public Sector ',NULL),(14,'Science & Technology ',NULL),(16,'Urban Development ',NULL),(17,'Gender',NULL),(18,'Millenium development goals',NULL),(19,'Climate Change',NULL),(20,'External Debt',NULL),(21,'Trade',NULL),(23,'Nothing','None'),(24,'Health (Auto)','Automatically assigned health indicators without an official category');
/*!40000 ALTER TABLE `IndicatorCategories` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01 16:57:16
