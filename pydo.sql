-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 25 jan. 2024 à 07:45
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `pydo`
--

-- --------------------------------------------------------

--
-- Structure de la table `etat`
--

DROP TABLE IF EXISTS `etat`;
CREATE TABLE IF NOT EXISTS `etat` (
  `etat_id` int NOT NULL AUTO_INCREMENT,
  `etat_nom` varchar(50) DEFAULT NULL,
  `tache_id` int NOT NULL,
  PRIMARY KEY (`etat_id`),
  KEY `tache_id` (`tache_id`)
) ENGINE=MyISAM AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `etat`
--

INSERT INTO `etat` (`etat_id`, `etat_nom`, `tache_id`) VALUES
(84, 'À faire', 84),
(85, 'À faire', 85),
(86, 'Terminée', 86),
(87, 'En cours', 87);

-- --------------------------------------------------------

--
-- Structure de la table `tache`
--

DROP TABLE IF EXISTS `tache`;
CREATE TABLE IF NOT EXISTS `tache` (
  `tache_id` int NOT NULL AUTO_INCREMENT,
  `tache_libelle` varchar(50) DEFAULT NULL,
  `date_creation` datetime DEFAULT NULL,
  `date_fixee` datetime DEFAULT NULL,
  `date_realisation` datetime DEFAULT NULL,
  PRIMARY KEY (`tache_id`)
) ENGINE=MyISAM AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `tache`
--

INSERT INTO `tache` (`tache_id`, `tache_libelle`, `date_creation`, `date_fixee`, `date_realisation`) VALUES
(84, 'Rendre fier M.GAMORY', '2024-01-23 11:43:57', '2024-01-30 00:00:00', NULL),
(85, 'Devenir le developpeur', '2024-01-23 11:44:14', '2024-01-30 00:00:00', NULL),
(86, 'Manger un petit peu', '2024-01-23 11:44:46', '2024-01-30 00:00:00', '2024-01-23 11:44:52'),
(87, 'Ecrivez le programme en Python', '2024-01-23 11:47:17', '2024-01-30 00:00:00', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
