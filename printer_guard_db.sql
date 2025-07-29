-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : ven. 04 avr. 2025 à 23:15
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `printer_guard_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `alerte`
--

CREATE TABLE `alerte` (
  `id_alerte` int(11) NOT NULL,
  `id_imprimante` int(11) NOT NULL,
  `description` text NOT NULL,
  `date_alerte` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `historique`
--

CREATE TABLE `historique` (
  `id` int(11) NOT NULL,
  `imprimante_id` int(11) NOT NULL,
  `date_historique` date NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `imprimante`
--

CREATE TABLE `imprimante` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `modele` varchar(100) NOT NULL,
  `address_ip` varchar(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `imprimante`
--

INSERT INTO `imprimante` (`id`, `nom`, `modele`, `address_ip`) VALUES
(1, 'Imprimante Reception', 'HP Color LaserJet MFP M 283fdw', '10.11.99.86'),
(2, 'Imprimante Direction', 'HP Color LaserJet Pro MFP M479fdw', '10.11.99.20'),
(3, 'Imprimante Centrale', 'HP LaserJet Enterprise M776', '10.11.99.43');

-- --------------------------------------------------------

--
-- Structure de la table `maintenance`
--

CREATE TABLE `maintenance` (
  `id` int(11) NOT NULL,
  `imprimante_id` int(11) NOT NULL,
  `date_maintenance` date NOT NULL,
  `description` text NOT NULL,
  `nom_technicien` varchar(100) DEFAULT NULL,
  `type_maintenance` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `alerte`
--
ALTER TABLE `alerte`
  ADD PRIMARY KEY (`id_alerte`),
  ADD KEY `fk_alerte_imprimante` (`id_imprimante`);

--
-- Index pour la table `historique`
--
ALTER TABLE `historique`
  ADD PRIMARY KEY (`id`),
  ADD KEY `imprimante_id` (`imprimante_id`);

--
-- Index pour la table `imprimante`
--
ALTER TABLE `imprimante`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `maintenance`
--
ALTER TABLE `maintenance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `imprimante_id` (`imprimante_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `alerte`
--
ALTER TABLE `alerte`
  MODIFY `id_alerte` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `historique`
--
ALTER TABLE `historique`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `imprimante`
--
ALTER TABLE `imprimante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `maintenance`
--
ALTER TABLE `maintenance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `alerte`
--
ALTER TABLE `alerte`
  ADD CONSTRAINT `fk_alerte_imprimante` FOREIGN KEY (`id_imprimante`) REFERENCES `imprimante` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `historique`
--
ALTER TABLE `historique`
  ADD CONSTRAINT `historique_ibfk_1` FOREIGN KEY (`imprimante_id`) REFERENCES `imprimante` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `maintenance`
--
ALTER TABLE `maintenance`
  ADD CONSTRAINT `maintenance_ibfk_1` FOREIGN KEY (`imprimante_id`) REFERENCES `imprimante` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

CREATE TRIGGER `after_insert_imprimante`
AFTER INSERT ON `imprimante`
FOR EACH ROW
BEGIN
  INSERT INTO `historique` (`imprimante_id`, `date_historique`, `description`)
  VALUES (NEW.id, CURDATE(), CONCAT('Imprimante ', NEW.nom , ' ajoutée.'));
END;


CREATE TRIGGER `after_update_imprimante`
AFTER UPDATE ON `imprimante`
FOR EACH ROW
BEGIN
  INSERT INTO `historique` (`imprimante_id`, `date_historique`, `description`)
  VALUES (NEW.id, CURDATE(), CONCAT('Imprimante ', NEW.nom , ' mise à jour.'));
END;  

CREATE TRIGGER `after_delete_imprimante`
AFTER DELETE ON `imprimante`
FOR EACH ROW
BEGIN
  INSERT INTO `historique` (`imprimante_id`, `date_historique`, `description`)
  VALUES (OLD.id, CURDATE(), CONCAT('Imprimante ', OLD.nom , ' supprimée.'));
END; 

CREATE TRIGGER `after_insert_maintenance`
AFTER INSERT ON `maintenance`
FOR EACH ROW
BEGIN
  INSERT INTO `historique` (`imprimante_id`, `date_historique`, `description`)
  VALUES (
    NEW.imprimante_id,
    CURDATE(),
    CONCAT(
      'Maintenance ajoutée par ',
      IFNULL(NEW.nom_technicien, 'technicien inconnu'),
      ' (type: ',
      IFNULL(NEW.type_maintenance, 'non spécifié'),
      '). Description: ',
      NEW.description
    )
  );
END;

CREATE TRIGGER `after_update_maintenance`
AFTER UPDATE ON `maintenance`
FOR EACH ROW
BEGIN
  INSERT INTO `historique` (`imprimante_id`, `date_historique`, `description`)
  VALUES (
    NEW.imprimante_id,
    CURDATE(),
    CONCAT(
      'Maintenance mise à jour par ',
      IFNULL(NEW.nom_technicien, 'technicien inconnu'),
      ' (type: ',
      IFNULL(NEW.type_maintenance, 'non spécifié'),
      '). Description: ',
      NEW.description
    )
  );
END;

CREATE TRIGGER `after_delete_maintenance`
AFTER DELETE ON `maintenance`
FOR EACH ROW
BEGIN
  INSERT INTO `historique` (`imprimante_id`, `date_historique`, `description`)
  VALUES (
    OLD.imprimante_id,
    CURDATE(),
    CONCAT(
      'Maintenance supprimée par ',
      IFNULL(OLD.nom_technicien, 'technicien inconnu'),
      ' (type: ',
      IFNULL(OLD.type_maintenance, 'non spécifié'),
      '). Description: ',
      OLD.description
    )
  );
END;