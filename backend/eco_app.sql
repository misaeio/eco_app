-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: mysql-2f405199-ecoapp3902026.a.aivencloud.com    Database: eco_app
-- ------------------------------------------------------
-- Server version	8.0.45

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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '0b57a53b-34f1-11f1-a993-7a35e2309458:1-118,
84a88228-2ca7-11f1-bcc9-c2e454254c25:1-36,
c8713250-450c-11f1-8f76-6ad0f572c9d0:1-28,
e0512830-28bf-11f1-ae93-224523d3d948:1-56,
e1f00da8-2ddc-11f1-8a10-66d8160c5d75:1-30,
fe4d9116-3389-11f1-be91-22e15485661f:1-34';

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `comment` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,10,31,'I had a few cardboard boxes too, but I did not get a picture of them.','2026-04-20 01:16:29'),(2,11,31,'Nice!','2026-04-20 01:27:10'),(4,10,31,'Glass can be recycled too!','2026-04-20 01:36:25'),(5,5,31,'Hello Angelo!','2026-04-20 01:37:42'),(6,12,30,'good','2026-04-20 16:00:46'),(7,15,30,'lmao u suck','2026-04-20 19:05:53'),(8,16,30,'ur gay','2026-04-21 02:53:47');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `followers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `follower_id` int NOT NULL,
  `following_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `follower_id` (`follower_id`),
  KEY `following_id` (`following_id`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`following_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `follows` (
  `id` int NOT NULL AUTO_INCREMENT,
  `follower_id` int DEFAULT NULL,
  `following_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `post_id` (`post_id`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (1,9,30,'2026-04-20 00:38:58'),(2,10,31,'2026-04-20 01:27:28'),(3,12,31,'2026-04-20 15:38:27'),(4,12,30,'2026-04-20 16:00:35'),(5,15,30,'2026-04-20 19:05:56'),(6,16,30,'2026-04-21 02:53:39'),(7,11,30,'2026-04-23 16:54:51'),(8,14,30,'2026-04-29 03:11:46');
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_` varchar(100) DEFAULT NULL,
  `type_` varchar(100) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'Peoria Recycling CENTER','recyclyng',40.693600,-89.589000),(2,'Donovan Park','park',40.720000,-89.550000);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_resets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_resets`
--

LOCK TABLES `password_resets` WRITE;
/*!40000 ALTER TABLE `password_resets` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_resets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `content` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `image_url` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (5,27,'hi guys <3','2026-04-08 21:35:40',NULL),(10,31,'Recycled my weeks worth of water jugs!','2026-04-20 01:14:44','https://media.istockphoto.com/id/1203048878/photo/a-bag-of-empty-plastic-water-bottles-ready-for-recycling-sits-by-the-curb-at-the-canoga-park.jpg?s=2048x2048&w=is&k=20&c=VdzPyBYPGyeTcuVF92ETBn7A7brRTiFN-6559hL-sac='),(11,32,'Planted a tree in the local park this morning!','2026-04-20 01:26:20','https://www.treehugger.com/thmb/nkO4TVB8ta2CXeiOir8UZ3VivLo=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__mnn__images__2017__03__replant-tree-bfbbfd18d1334ee0aa03851c6800baaa.jpg'),(12,31,'How is everyone doing?','2026-04-20 01:34:31',''),(13,31,'Does anyone know where to recycle old TVs?','2026-04-20 17:57:21',''),(14,34,'Is there any way to recycle old shoes?','2026-04-20 18:36:51',''),(15,30,'hi chat','2026-04-20 19:05:44',''),(16,30,'i walked','2026-04-21 02:53:30',''),(17,30,'','2026-04-29 03:23:47','https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fscreenrant.com%2Fjojos-bizarre-adventure-part-9-release-date-hinted%2F&ved=0CBYQjRxqFwoTCMCj5u6NkpQDFQAAAAAdAAAAABAe&opi=89978449'),(18,30,'','2026-04-29 03:28:41','https://imgur.com/a/Sbw4ABk');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text,
  `points` int DEFAULT '10',
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Pick up trash','Pick up at least 5 pieces of trash',10,NULL),(2,'Go for a walk','Walk instead of driving today',5,NULL),(3,'Recycle items','Recycle plastic or paper waste',8,NULL),(4,'Pick up trash','Pick up at least 5 pieces of trash',10,NULL),(5,'Go for a walk','Walk instead of driving today',5,NULL),(6,'Recycle items','Recycle plastic or paper waste',8,NULL),(7,'Gym',NULL,10,NULL),(10,'report',NULL,10,1),(11,'report',NULL,10,1),(21,'walk',NULL,10,15),(22,'compost',NULL,10,16),(23,'Take recycling up town',NULL,10,16),(24,'Take recycling uptown',NULL,10,17),(25,'Pick up garbage in park',NULL,10,17),(27,'hi',NULL,10,22),(29,'Build greenhouse',NULL,10,31),(30,'Help community recycle on junk day',NULL,10,31);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(60) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL,
  `bio` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `username_2` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'aaron ','$2b$12$TTkSOHtIAUBA5BXCmzRPJOmKE2bmDp4dDHr6A47Icvu1KXD.I6EXi',NULL,NULL),(15,'misaaa','$2b$12$.3pZ1ADuQDsqRAYUndbyNu/uZ/bqfJiu5ehUOfBoZQaD0f1qK70.S',NULL,NULL),(17,'Aaron_Test','$2b$12$SezbC4nNxRqi9wuH8QLa/.WAjTdHtdo9LxUjF0TClLAOWP4VRfb4O',NULL,NULL),(18,'testtest','$2b$12$dQNPqFPz2E6XLGtP.M4ZP.Hnp.6lCKHqpsV5OLRhrGAPTfdt.yKG6',NULL,NULL),(19,'rsvezia','$2b$12$nukde6YIWho61VgnTx0bNebhXsmw7k0.NVwbAYWcvaeyFc2S0fzLG',NULL,NULL),(21,'misa2','$2b$12$URvO9AeGIPaB8GTdikEM6.iFNPSr3aeC0d6ew4uyKXCXWF.Jm8s8G',NULL,NULL),(22,'misssa','$2b$12$GOkDBqHp7xwb5./LU6ecMeazWgIhlsZ10ORkS0zomlLJUKX9Za/za',NULL,NULL),(23,'mis','$2b$12$/K/TrFUrIimFuyRGcnEzaeCHrnw6HB7jRd1V6XhMdLpuKe7WZ1AT.',NULL,NULL),(24,'mss','$2b$12$VrhslDhwTGRiFWoASOpaX.6R8q50VFa2XpSqMLRsyX2mssd0jZtvK',NULL,NULL),(25,'ih8aaron<3','$2b$12$/6BWjvvTDJy3D7ufgIFC3.kY8eSArGBYq3oLk4za/9T3Vw9z.mWEG',NULL,NULL),(26,'iluvADRIANuWu','$2b$12$GVLOh3yhxe25P1waE2xLcOBxPBzAKOMH2Ts9MlrxKmznuz0091GTG',NULL,NULL),(27,'angeloSUX:3','$2b$12$h.MVcxrX.3a0wS5WmaQyr.xss9hYxG3bye/m/4bOI8LwUUufbMgJ2',NULL,NULL),(28,'misaGOAted8=D','$2b$12$or8mTWKPO0hSvaxqEcOxIuGu5JDNp5KQrJz5oCNUCJxviVb2jHfWq',NULL,NULL),(29,'louieXryan1234','$2b$12$wkrdYkQ4ZklFDcZQlhKQx.ZssD6aDj/7IOeVXi5ASRARo1SnTPvnS',NULL,NULL),(30,'misaaey42999','$2b$12$yvyQky/qRZVpSXTKKO7lH.P4Hv6nin1ieAVoMuiEpG4S.vam4aGfq','','hi'),(31,'aaron4','$2b$12$sjdfaBH291CktvRcJdcMWugwshVprgkrvvhis9M/ZTmdJIIOKuVpC',NULL,NULL),(32,'aaron5','$2b$12$a/31MiRoyFarFqEg9W/NV.aKSA8WERUVGJAMUZl9M5I5xZmwTJmjS',NULL,NULL),(34,'aaron6','$2b$12$qW73BjBUB9PvtbmtQUe2xullPnRGNjJXP7WuLJeAtI.0AHQ/xWVn6',NULL,NULL),(35,'aaron7','$2b$12$immYG3MVoytGmNSCsGF0O.ER19zor3GNBCTyWRjRYtQgtnr/nxQBS',NULL,NULL),(36,'2222','$2b$12$v3TtTBAlaN4C17i8YQ2h8eZdJhiNM27wZd3rRxgWo/WnpY1s.3WYW',NULL,NULL),(37,'23323','$2b$12$BSVqlapofenzGhmF5WtNeOJJbOf4fHlHleYWuF1FiGlwpYgx0FgOe',NULL,NULL),(38,'aarontoddadams@gmail.com','$2b$12$MHmiIiI.REqlL3Hyp32xC.jHQ0QxkJHJ9DkrSjuc0X4I3uGU0tK66',NULL,NULL),(39,'Aaron_a','$2b$12$8b76uCFwVsqIeHWrVpXHI.5aKntWK./xkL8OpYDJLt9.IBhzNt4yi','',''),(41,'naaa','$2b$12$i32Hi.Ng5c.agwfNX06N1.2LaYiWanDfIRAj25yQU3F4A27fldcu6','',''),(42,'aadams1@mail.bradley.edu','$2b$12$Pay7/b1Ep8ogCGt.GApGQu/UYm1AuvbYl1Erq5e0qsqgMNdHgJW06',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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

-- Dump completed on 2026-05-01  0:32:09
