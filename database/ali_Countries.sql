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
-- Table structure for table `Countries`
--

DROP TABLE IF EXISTS `Countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Countries` (
  `country_code` char(3) NOT NULL,
  `country_name` varchar(100) DEFAULT NULL,
  `capital_city` varchar(100) DEFAULT NULL,
  `region_id` int DEFAULT NULL,
  `income_level` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`country_code`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `countries_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `Regions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Countries`
--

LOCK TABLES `Countries` WRITE;
/*!40000 ALTER TABLE `Countries` DISABLE KEYS */;
INSERT INTO `Countries` VALUES ('ABW','Aruba','Oranjestad',3,'High income'),('AFG','Afghanistan','Kabul',4,'Low income'),('AGO','Angola','Luanda',7,'Lower middle income'),('ALB','Albania','Tirane',2,'Upper middle income'),('AND','Andorra','Andorra la Vella',2,'High income'),('ARE','United Arab Emirates','Abu Dhabi',4,'High income'),('ARG','Argentina','Buenos Aires',3,'Upper middle income'),('ARM','Armenia','Yerevan',2,'Upper middle income'),('ASM','American Samoa','Pago Pago',1,'High income'),('ATG','Antigua and Barbuda','Saint John\'s',3,'High income'),('AUS','Australia','Canberra',1,'High income'),('AUT','Austria','Vienna',2,'High income'),('AZE','Azerbaijan','Baku',2,'Upper middle income'),('BDI','Burundi','Bujumbura',7,'Low income'),('BEL','Belgium','Brussels',2,'High income'),('BEN','Benin','Porto-Novo',7,'Lower middle income'),('BFA','Burkina Faso','Ouagadougou',7,'Low income'),('BGD','Bangladesh','Dhaka',6,'Lower middle income'),('BGR','Bulgaria','Sofia',2,'High income'),('BHR','Bahrain','Manama',4,'High income'),('BHS','Bahamas, The','Nassau',3,'High income'),('BIH','Bosnia and Herzegovina','Sarajevo',2,'Upper middle income'),('BLR','Belarus','Minsk',2,'Upper middle income'),('BLZ','Belize','Belmopan',3,'Upper middle income'),('BMU','Bermuda','Hamilton',5,'High income'),('BOL','Bolivia','La Paz',3,'Lower middle income'),('BRA','Brazil','Brasilia',3,'Upper middle income'),('BRB','Barbados','Bridgetown',3,'High income'),('BRN','Brunei Darussalam','Bandar Seri Begawan',1,'High income'),('BTN','Bhutan','Thimphu',6,'Lower middle income'),('BWA','Botswana','Gaborone',7,'Upper middle income'),('CAF','Central African Republic','Bangui',7,'Low income'),('CAN','Canada','Ottawa',5,'High income'),('CHE','Switzerland','Bern',2,'High income'),('CHL','Chile','Santiago',3,'High income'),('CHN','China','Beijing',1,'Upper middle income'),('CIV','Cote d\'Ivoire','Yamoussoukro',7,'Lower middle income'),('CMR','Cameroon','Yaounde',7,'Lower middle income'),('COD','Congo, Dem. Rep.','Kinshasa',7,'Low income'),('COG','Congo, Rep.','Brazzaville',7,'Lower middle income'),('COL','Colombia','Bogota',3,'Upper middle income'),('COM','Comoros','Moroni',7,'Lower middle income'),('CPV','Cabo Verde','Praia',7,'Upper middle income'),('CRI','Costa Rica','San Jose',3,'High income'),('CUB','Cuba','Havana',3,'Upper middle income'),('CUW','Curacao','Willemstad',3,'High income'),('CYM','Cayman Islands','George Town',3,'High income'),('CYP','Cyprus','Nicosia',2,'High income'),('CZE','Czechia','Prague',2,'High income'),('DEU','Germany','Berlin',2,'High income'),('DJI','Djibouti','Djibouti',4,'Lower middle income'),('DMA','Dominica','Roseau',3,'Upper middle income'),('DNK','Denmark','Copenhagen',2,'High income'),('DOM','Dominican Republic','Santo Domingo',3,'Upper middle income'),('DZA','Algeria','Algiers',4,'Upper middle income'),('ECU','Ecuador','Quito',3,'Upper middle income'),('EGY','Egypt, Arab Rep.','Cairo',4,'Lower middle income'),('ERI','Eritrea','Asmara',7,'Low income'),('ESP','Spain','Madrid',2,'High income'),('EST','Estonia','Tallinn',2,'High income'),('ETH','Ethiopia','Addis Ababa',7,'Not classified'),('FIN','Finland','Helsinki',2,'High income'),('FJI','Fiji','Suva',1,'Upper middle income'),('FRA','France','Paris',2,'High income'),('FRO','Faroe Islands','Torshavn',2,'High income'),('FSM','Micronesia, Fed. Sts.','Palikir',1,'Lower middle income'),('GAB','Gabon','Libreville',7,'Upper middle income'),('GBR','United Kingdom','London',2,'High income'),('GEO','Georgia','Tbilisi',2,'Upper middle income'),('GHA','Ghana','Accra',7,'Lower middle income'),('GIN','Guinea','Conakry',7,'Lower middle income'),('GMB','Gambia, The','Banjul',7,'Low income'),('GNB','Guinea-Bissau','Bissau',7,'Low income'),('GNQ','Equatorial Guinea','Malabo',7,'Upper middle income'),('GRC','Greece','Athens',2,'High income'),('GRD','Grenada','Saint George\'s',3,'Upper middle income'),('GRL','Greenland','Nuuk',2,'High income'),('GTM','Guatemala','Guatemala City',3,'Upper middle income'),('GUM','Guam','Agana',1,'High income'),('GUY','Guyana','Georgetown',3,'High income'),('HND','Honduras','Tegucigalpa',3,'Lower middle income'),('HRV','Croatia','Zagreb',2,'High income'),('HTI','Haiti','Port-au-Prince',3,'Lower middle income'),('HUN','Hungary','Budapest',2,'High income'),('IDN','Indonesia','Jakarta',1,'Upper middle income'),('IMN','Isle of Man','Douglas',2,'High income'),('IND','India','New Delhi',6,'Lower middle income'),('IRL','Ireland','Dublin',2,'High income'),('IRN','Iran, Islamic Rep.','Tehran',4,'Upper middle income'),('IRQ','Iraq','Baghdad',4,'Upper middle income'),('ISL','Iceland','Reykjavik',2,'High income'),('ITA','Italy','Rome',2,'High income'),('JAM','Jamaica','Kingston',3,'Upper middle income'),('JOR','Jordan','Amman',4,'Lower middle income'),('JPN','Japan','Tokyo',1,'High income'),('KAZ','Kazakhstan','Astana',2,'Upper middle income'),('KEN','Kenya','Nairobi',7,'Lower middle income'),('KGZ','Kyrgyz Republic','Bishkek',2,'Lower middle income'),('KHM','Cambodia','Phnom Penh',1,'Lower middle income'),('KIR','Kiribati','Tarawa',1,'Lower middle income'),('KNA','St. Kitts and Nevis','Basseterre',3,'High income'),('KOR','Korea, Rep.','Seoul',1,'High income'),('KWT','Kuwait','Kuwait City',4,'High income'),('LAO','Lao PDR','Vientiane',1,'Lower middle income'),('LBN','Lebanon','Beirut',4,'Lower middle income'),('LBR','Liberia','Monrovia',7,'Low income'),('LBY','Libya','Tripoli',4,'Upper middle income'),('LCA','St. Lucia','Castries',3,'Upper middle income'),('LIE','Liechtenstein','Vaduz',2,'High income'),('LKA','Sri Lanka','Colombo',6,'Lower middle income'),('LSO','Lesotho','Maseru',7,'Lower middle income'),('LTU','Lithuania','Vilnius',2,'High income'),('LUX','Luxembourg','Luxembourg',2,'High income'),('LVA','Latvia','Riga',2,'High income'),('MAF','St. Martin (French part)','Marigot',3,'High income'),('MAR','Morocco','Rabat',4,'Lower middle income'),('MCO','Monaco','Monaco',2,'High income'),('MDA','Moldova','Chisinau',2,'Upper middle income'),('MDG','Madagascar','Antananarivo',7,'Low income'),('MDV','Maldives','Male',6,'Upper middle income'),('MEX','Mexico','Mexico City',3,'Upper middle income'),('MHL','Marshall Islands','Majuro',1,'Upper middle income'),('MKD','North Macedonia','Skopje',2,'Upper middle income'),('MLI','Mali','Bamako',7,'Low income'),('MLT','Malta','Valletta',4,'High income'),('MMR','Myanmar','Naypyidaw',1,'Lower middle income'),('MNE','Montenegro','Podgorica',2,'Upper middle income'),('MNG','Mongolia','Ulaanbaatar',1,'Upper middle income'),('MNP','Northern Mariana Islands','Saipan',1,'High income'),('MOZ','Mozambique','Maputo',7,'Low income'),('MRT','Mauritania','Nouakchott',7,'Lower middle income'),('MUS','Mauritius','Port Louis',7,'Upper middle income'),('MWI','Malawi','Lilongwe',7,'Low income'),('MYS','Malaysia','Kuala Lumpur',1,'Upper middle income'),('NAM','Namibia','Windhoek',7,'Lower middle income'),('NCL','New Caledonia','Noum\'ea',1,'High income'),('NER','Niger','Niamey',7,'Low income'),('NGA','Nigeria','Abuja',7,'Lower middle income'),('NIC','Nicaragua','Managua',3,'Lower middle income'),('NLD','Netherlands','Amsterdam',2,'High income'),('NOR','Norway','Oslo',2,'High income'),('NPL','Nepal','Kathmandu',6,'Lower middle income'),('NRU','Nauru','Yaren District',1,'High income'),('NZL','New Zealand','Wellington',1,'High income'),('OMN','Oman','Muscat',4,'High income'),('PAK','Pakistan','Islamabad',4,'Lower middle income'),('PAN','Panama','Panama City',3,'High income'),('PER','Peru','Lima',3,'Upper middle income'),('PHL','Philippines','Manila',1,'Lower middle income'),('PLW','Palau','Koror',1,'High income'),('PNG','Papua New Guinea','Port Moresby',1,'Lower middle income'),('POL','Poland','Warsaw',2,'High income'),('PRI','Puerto Rico (US)','San Juan',3,'High income'),('PRK','Korea, Dem. People\'s Rep.','Pyongyang',1,'Low income'),('PRT','Portugal','Lisbon',2,'High income'),('PRY','Paraguay','Asuncion',3,'Upper middle income'),('PYF','French Polynesia','Papeete',1,'High income'),('QAT','Qatar','Doha',4,'High income'),('ROU','Romania','Bucharest',2,'High income'),('RUS','Russian Federation','Moscow',2,'High income'),('RWA','Rwanda','Kigali',7,'Low income'),('SAU','Saudi Arabia','Riyadh',4,'High income'),('SDN','Sudan','Khartoum',7,'Low income'),('SEN','Senegal','Dakar',7,'Lower middle income'),('SGP','Singapore','Singapore',1,'High income'),('SLB','Solomon Islands','Honiara',1,'Lower middle income'),('SLE','Sierra Leone','Freetown',7,'Low income'),('SLV','El Salvador','San Salvador',3,'Upper middle income'),('SMR','San Marino','San Marino',2,'High income'),('SOM','Somalia, Fed. Rep.','Mogadishu',7,'Low income'),('SRB','Serbia','Belgrade',2,'Upper middle income'),('SSD','South Sudan','Juba',7,'Low income'),('STP','Sao Tome and Principe','Sao Tome',7,'Lower middle income'),('SUR','Suriname','Paramaribo',3,'Upper middle income'),('SVK','Slovak Republic','Bratislava',2,'High income'),('SVN','Slovenia','Ljubljana',2,'High income'),('SWE','Sweden','Stockholm',2,'High income'),('SWZ','Eswatini','Mbabane',7,'Lower middle income'),('SXM','Sint Maarten (Dutch part)','Philipsburg',3,'High income'),('SYC','Seychelles','Victoria',7,'High income'),('SYR','Syrian Arab Republic','Damascus',4,'Low income'),('TCA','Turks and Caicos Islands','Grand Turk',3,'High income'),('TCD','Chad','N\'Djamena',7,'Low income'),('TGO','Togo','Lome',7,'Low income'),('THA','Thailand','Bangkok',1,'Upper middle income'),('TJK','Tajikistan','Dushanbe',2,'Lower middle income'),('TKM','Turkmenistan','Ashgabat',2,'Upper middle income'),('TLS','Timor-Leste','Dili',1,'Lower middle income'),('TON','Tonga','Nuku\'alofa',1,'Upper middle income'),('TTO','Trinidad and Tobago','Port-of-Spain',3,'High income'),('TUN','Tunisia','Tunis',4,'Lower middle income'),('TUR','Turkiye','Ankara',2,'Upper middle income'),('TUV','Tuvalu','Funafuti',1,'Upper middle income'),('TZA','Tanzania','Dodoma',7,'Lower middle income'),('UGA','Uganda','Kampala',7,'Low income'),('UKR','Ukraine','Kiev',2,'Upper middle income'),('URY','Uruguay','Montevideo',3,'High income'),('USA','United States','Washington D.C.',5,'High income'),('UZB','Uzbekistan','Tashkent',2,'Lower middle income'),('VCT','St. Vincent and the Grenadines','Kingstown',3,'Upper middle income'),('VEN','Venezuela, RB','Caracas',3,'Not classified'),('VGB','British Virgin Islands','Road Town',3,'High income'),('VIR','Virgin Islands (U.S.)','Charlotte Amalie',3,'High income'),('VNM','Viet Nam','Hanoi',1,'Lower middle income'),('VUT','Vanuatu','Port-Vila',1,'Lower middle income'),('WSM','Samoa','Apia',1,'Upper middle income'),('XKX','Kosovo','Pristina',2,'Upper middle income'),('YEM','Yemen, Rep.','Sana\'a',4,'Low income'),('ZAF','South Africa','Pretoria',7,'Upper middle income'),('ZMB','Zambia','Lusaka',7,'Lower middle income'),('ZWE','Zimbabwe','Harare',7,'Lower middle income');
/*!40000 ALTER TABLE `Countries` ENABLE KEYS */;
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

-- Dump completed on 2025-11-22 15:38:20
