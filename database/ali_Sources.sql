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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'f77dd534-bf1f-11f0-a6d0-f71997ab92db:1-101';

--
-- Table structure for table `Sources`
--

DROP TABLE IF EXISTS `Sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source_name` varchar(150) DEFAULT NULL,
  `source_organization` varchar(200) DEFAULT NULL,
  `source_url` varchar(300) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sources`
--

LOCK TABLES `Sources` WRITE;
/*!40000 ALTER TABLE `Sources` DISABLE KEYS */;
INSERT INTO `Sources` VALUES (1,'Doing Business',NULL,NULL,NULL),(2,'World Development Indicators',NULL,NULL,NULL),(11,'Africa Development Indicators',NULL,NULL,NULL),(12,'Education Statistics',NULL,NULL,NULL),(13,'Enterprise Surveys',NULL,NULL,NULL),(14,'Gender Statistics',NULL,NULL,NULL),(15,'Global Economic Monitor',NULL,NULL,NULL),(18,'IDA Results Measurement System',NULL,NULL,NULL),(19,'Millennium Development Goals',NULL,NULL,NULL),(20,'Quarterly Public Sector Debt',NULL,NULL,NULL),(22,'Quarterly External Debt Statistics SDDS',NULL,NULL,NULL),(23,'Quarterly External Debt Statistics GDDS',NULL,NULL,NULL),(27,'Global Economic Prospects',NULL,NULL,NULL),(28,'Global Findex database',NULL,NULL,NULL),(29,'The Atlas of Social Protection: Indicators of Resilience and Equity',NULL,NULL,NULL),(30,'Exporter Dynamics Database – Indicators at Country-Year Level',NULL,NULL,NULL),(32,'Global Financial Development',NULL,NULL,NULL),(33,'G20 Financial Inclusion Indicators',NULL,NULL,NULL),(34,'Global Partnership for Education',NULL,NULL,NULL),(35,'Sustainable Energy for All',NULL,NULL,NULL),(37,'LAC Equity Lab',NULL,NULL,NULL),(41,'Country Partnership Strategy for India (FY2013 - 17)',NULL,NULL,NULL),(43,'Adjusted Net Savings',NULL,NULL,NULL),(45,'Indonesia Database for Policy and Economic Research',NULL,NULL,NULL),(46,'Sustainable Development Goals ',NULL,NULL,NULL),(57,'WDI Database Archives',NULL,NULL,NULL),(59,'Wealth Accounts',NULL,NULL,NULL),(60,'Economic Fitness',NULL,NULL,NULL),(61,'PPPs Regulatory Quality',NULL,NULL,NULL),(63,'Human Capital Index',NULL,NULL,NULL),(64,'Worldwide Bureaucracy Indicators',NULL,NULL,NULL),(65,'Health Equity and Financial Protection Indicators',NULL,NULL,NULL),(66,'Logistics Performance Index',NULL,NULL,NULL),(69,'Global Financial Inclusion and Consumer Protection Survey',NULL,NULL,NULL),(70,'Economic Fitness 2',NULL,NULL,NULL),(71,'International Comparison Program (ICP) 2005',NULL,NULL,NULL),(73,'Global Financial Inclusion and Consumer Protection Survey (Internal)',NULL,NULL,NULL),(75,'Environment, Social and Governance (ESG) Data',NULL,NULL,NULL),(78,'ICP 2017',NULL,NULL,NULL),(79,'PEFA_GRPFM',NULL,NULL,NULL),(80,'Gender Disaggregated Labor Database (GDLD)',NULL,NULL,NULL),(81,' International Debt Statistics: DSSI',NULL,NULL,NULL),(82,'Global Public Procurement',NULL,NULL,NULL),(86,'Global Jobs Indicators Database (JOIN)',NULL,NULL,NULL),(87,'Country Climate and Development Report (CCDR)',NULL,NULL,NULL),(88,'Food Prices for Nutrition',NULL,NULL,NULL),(89,'Identification for Development (ID4D) Data',NULL,NULL,NULL),(91,'PEFA_CRPFM',NULL,NULL,NULL),(92,'Disability Data Hub (DDH)',NULL,NULL,NULL),(93,'FPN Datahub Archive',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Sources` ENABLE KEYS */;
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

-- Dump completed on 2025-11-22 15:38:19
