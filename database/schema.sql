CREATE DATABASE IF NOT EXISTS `financetracker`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE `financetracker`;

--
-- Table: users
--
CREATE TABLE IF NOT EXISTS `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `createdat` datetime DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table: categories
--
CREATE TABLE IF NOT EXISTS `categories` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `CategoryName` varchar(50) DEFAULT NULL,
  `CategoryType` enum('income','expense') DEFAULT NULL,
  PRIMARY KEY (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table: transactions
--
CREATE TABLE IF NOT EXISTS `transactions` (
  `TxnID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `CategoryID` int DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `txnType` enum('income','expense') DEFAULT NULL,
  `txnDate` date DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `createdat` datetime DEFAULT NULL,
  PRIMARY KEY (`TxnID`),
  KEY `CategoryID` (`CategoryID`),
  KEY `transactions_ibfk_1` (`UserID`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`CategoryID`) REFERENCES `categories` (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;