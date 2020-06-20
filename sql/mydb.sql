-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 19, 2020 at 12:56 PM
-- Server version: 5.7.30-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mydb`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `accumulated`
-- (See below for the actual view)
--
CREATE TABLE `accumulated` (
`email` varchar(255)
,`score` double
,`duration` double
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `accumulated_rank`
-- (See below for the actual view)
--
CREATE TABLE `accumulated_rank` (
`score` double
,`email` varchar(255)
,`score_rank` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `ranks`
-- (See below for the actual view)
--
CREATE TABLE `ranks` (
`email` varchar(255)
,`username` varchar(255)
,`score` double
,`duration` double
,`week_score` double
,`week_duration` double
,`score_rank` bigint(21)
);

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE `scores` (
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `duration` double NOT NULL,
  `dscore` double NOT NULL,
  `id` int(11) NOT NULL,
  `receive_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `sensor_data` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `week_accumulated`
-- (See below for the actual view)
--
CREATE TABLE `week_accumulated` (
`email` varchar(255)
,`score` double
,`duration` double
);

-- --------------------------------------------------------

--
-- Structure for view `accumulated`
--
DROP TABLE IF EXISTS `accumulated`;

CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` SQL SECURITY DEFINER VIEW `accumulated`  AS  select `users`.`email` AS `email`,coalesce(sum(`scores`.`dscore`),0) AS `score`,coalesce(sum(`scores`.`duration`),0) AS `duration` from (`users` left join `scores` on((`users`.`email` = `scores`.`email`))) group by `users`.`email` ;

-- --------------------------------------------------------

--
-- Structure for view `accumulated_rank`
--
DROP TABLE IF EXISTS `accumulated_rank`;

CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` SQL SECURITY DEFINER VIEW `accumulated_rank`  AS  select `a`.`score` AS `score`,`a`.`email` AS `email`,(select count(`b`.`email`) from `accumulated` `b` where (`b`.`score` >= `a`.`score`)) AS `score_rank` from `accumulated` `a` order by `a`.`score` desc ;

-- --------------------------------------------------------

--
-- Structure for view `ranks`
--
DROP TABLE IF EXISTS `ranks`;

CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` SQL SECURITY DEFINER VIEW `ranks`  AS  select `a`.`email` AS `email`,`d`.`username` AS `username`,`a`.`score` AS `score`,`a`.`duration` AS `duration`,`c`.`score` AS `week_score`,`c`.`duration` AS `week_duration`,`b`.`score_rank` AS `score_rank` from (((`accumulated` `a` join `accumulated_rank` `b` on((`a`.`email` = `b`.`email`))) join `week_accumulated` `c` on((`a`.`email` = `c`.`email`))) join `users` `d` on((`a`.`email` = `d`.`email`))) ;

-- --------------------------------------------------------

--
-- Structure for view `week_accumulated`
--
DROP TABLE IF EXISTS `week_accumulated`;

CREATE ALGORITHM=UNDEFINED DEFINER=`admin`@`localhost` SQL SECURITY DEFINER VIEW `week_accumulated`  AS  select `users`.`email` AS `email`,coalesce(sum(`scores`.`dscore`),0) AS `score`,coalesce(sum(`scores`.`duration`),0) AS `duration` from (`users` left join (select `scores`.`email` AS `email`,`scores`.`duration` AS `duration`,`scores`.`dscore` AS `dscore`,`scores`.`id` AS `id`,`scores`.`receive_time` AS `receive_time` from `scores` where (`scores`.`receive_time` between (now() - interval 1 week) and now())) `scores` on((`users`.`email` = `scores`.`email`))) group by `users`.`email` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`id`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `scores`
--
ALTER TABLE `scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `fk` FOREIGN KEY (`email`) REFERENCES `users` (`email`) ON DELETE NO ACTION ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
