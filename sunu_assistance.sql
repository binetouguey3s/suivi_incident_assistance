-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: sen_assistance
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `numero_ticket` int NOT NULL AUTO_INCREMENT,
  `id_utilisateur` int NOT NULL,
  `titre` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `niveau_urgence` enum('Faible','Moyenne','Élevée') DEFAULT 'Élevée',
  `statut` enum('En attente','En cours','Résolu') DEFAULT 'En attente',
  PRIMARY KEY (`numero_ticket`),
  KEY `id_utilisateur` (`id_utilisateur`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateurs` (`id_utilisateur`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (1,1,'Chargeur HP','Rapide et puissant','Faible','Résolu'),(2,1,'Portable samsumg S20','Ecran cassé et en noir','Faible','En cours');
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateurs` (
  `id_utilisateur` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(300) NOT NULL,
  `role` enum('apprenant','admin') DEFAULT 'apprenant',
  PRIMARY KEY (`id_utilisateur`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateurs`
--

LOCK TABLES `utilisateurs` WRITE;
/*!40000 ALTER TABLE `utilisateurs` DISABLE KEYS */;
INSERT INTO `utilisateurs` VALUES (1,'diop','anta','antadiop@gmail.com','$2b$12$EwNmbI5oiBd0Xq7IPLGWCeDlMJHz8tSPbWekhdeQBSOWpk8qfjIJW','apprenant'),(2,'gueye','binetou','binetougueye@gmail.com','$2b$12$3DtBJh4ZuS1F3ntksueI9el1Y0UQe6KvuyUMrVuxzDpQ/aChn.fzm','apprenant'),(3,'GUEYE','Binetou Rassoul','binetourassoul@gmail.com','$2b$12$OjVuPEEEmCPce1W0nNRZrO1UBqFINNSHV0gdSP9UO4DVyXTL3PMFi','admin'),(4,'SAMB','Ndeye Fassa','ndeyefassa@gmail.com','$2b$12$hxua4Rfay7gjC5kSRGEWqOs3c6szxgqczgbdxll.gQtql6YwPJBQO','apprenant'),(5,'GUEYE','Sokhna Fatou','sokhnafatou@gmail.com','$2b$12$OOXfz3Ya0RlRYoo.zvRsS.6rt3vtmra3tof3W/vrumKthIb2uxNHm','admin'),(6,'LO','Mouhamed','mouhamedlo@gmail.com','$2b$12$AnlRGxgqayYM1k.e5mcZsOeHwTncG9MNvPmJTCGM2ZUpaQrDjJjzu','apprenant');
/*!40000 ALTER TABLE `utilisateurs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-13 14:36:32
