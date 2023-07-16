-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 15-07-2023 a las 23:41:42
-- Versión del servidor: 5.7.36
-- Versión de PHP: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tecseg`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `business_name` varchar(150) DEFAULT NULL,
  `cuit` bigint(11) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `comments` varchar(1000) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `domicilio_id` int(11) DEFAULT NULL,
  `cond_fiscal_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cliente_nombre_apellido` (`nombre`,`apellido`),
  KEY `domicilio_id` (`domicilio_id`),
  KEY `user_id` (`user_id`),
  KEY `client_cf` (`cond_fiscal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `client`
--

INSERT INTO `client` (`id`, `nombre`, `apellido`, `business_name`, `cuit`, `telefono`, `email`, `comments`, `user_id`, `domicilio_id`, `cond_fiscal_id`) VALUES
(1, 'Canal 13', 'San Luis', 'Canal 13 televisión', NULL, '42432432', '', 'Director Nasim', 1, 1, 1),
(2, 'Héctor', 'Bonarrico', 'Jesus Te Ama', NULL, '261 618 8088', '', 'ANYDESK: 255 433 310\r\npass: ?\r\n\r\nEnlace 11G\r\n\r\nTecnico Luis Fernandez (externo) - 261 558 6978\r\nTecnico Juan Silva (interno) - 261 618 8088', 4, 2, 1),
(3, 'Juan Antonio', 'Acompanies', 'REMAR', 34243243242, '954-424687', 'jaaco@remar.com.ar', 'Exportador a Paraguay', 4, 3, 1),
(4, 'Pedro', 'Almirón', 'Radio Total FM', 20432432421, '2147483647', 'palmiron@yahoo.com', 'teléfono del técnico\r\nFernandez: 2996-1235432\r\n10-14hs solamente', 4, 4, 3),
(6, 'Mariangeles', 'Gonzalez', 'MARIAN S.A.', 20432432421, '2147483647', NULL, 'persona ficticia', 1, 5, 1),
(16, 'Oscar', 'de la Fuente', 'De la Hoya S.R.L.', 20432432421, '42432432', NULL, 'cliente preferencial', 4, 7, 1),
(17, 'Favio', 'Brandan', 'FIVE TV', NULL, '1155637121', '', 'anydesk= 129445228\r\npass= universal14070', 10, 8, 1),
(18, 'Ana', 'Lupe', 'RF Argentina S.A.', NULL, '432654764', 'analupe@rfsa.com.ar', '', 10, 9, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cond_fiscal`
--

DROP TABLE IF EXISTS `cond_fiscal`;
CREATE TABLE IF NOT EXISTS `cond_fiscal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cond_fiscal`
--

INSERT INTO `cond_fiscal` (`id`, `nombre`) VALUES
(0, 'Sin especificar'),
(1, 'IVA Responsable Inscripto'),
(2, 'IVA Sujeto Exento'),
(3, 'Consumidor final'),
(4, 'Responsable Monotributo'),
(5, 'Sujeto No Categorizado'),
(6, 'Proveedor del Exterior'),
(7, 'Cliente del Exterior'),
(8, 'IVA Liberado - Ley Nº 19.640'),
(9, 'Monotributista  Social'),
(10, 'IVA No Alcanzado'),
(11, 'Monotributista Trabajador Independiente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_reparacion`
--

DROP TABLE IF EXISTS `detalle_reparacion`;
CREATE TABLE IF NOT EXISTS `detalle_reparacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(1000) NOT NULL,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) NOT NULL,
  `reparacion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_detalle` (`user_id`),
  KEY `orden_detalle` (`reparacion_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `detalle_reparacion`
--

INSERT INTO `detalle_reparacion` (`id`, `content`, `date_created`, `date_modified`, `user_id`, `reparacion_id`) VALUES
(1, 'Primer comentario', '2023-07-15 19:56:10', '2023-07-15 19:56:10', 10, 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `domicilio`
--

DROP TABLE IF EXISTS `domicilio`;
CREATE TABLE IF NOT EXISTS `domicilio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direccion` varchar(150) DEFAULT NULL,
  `localidad_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `localidad_id` (`localidad_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `domicilio`
--

INSERT INTO `domicilio` (`id`, `direccion`, `localidad_id`) VALUES
(1, 'Los cajones 2162', 870),
(2, 'Lavalle 327', 974),
(3, 'San Martin 514', 3),
(4, 'Urquiza 534', 754),
(5, 'Belgrano 519', 33),
(7, 'Mariano Moreno 678', 33),
(8, 'Calle Dominico 276', 973),
(9, 'Litoral 432', 766),
(10, 'calle 54', 184);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipment`
--

DROP TABLE IF EXISTS `equipment`;
CREATE TABLE IF NOT EXISTS `equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numSerie` varchar(20) NOT NULL,
  `anio` varchar(4) DEFAULT NULL,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(1000) DEFAULT NULL,
  `etiqueta_file` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `modelo_id` int(11) NOT NULL,
  `frecuencia_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `eq_numSerie` (`numSerie`),
  KEY `client_id` (`client_id`),
  KEY `user_id` (`user_id`),
  KEY `equipment_modelo` (`modelo_id`),
  KEY `equipment_canal_frecuencia` (`frecuencia_id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `equipment`
--

INSERT INTO `equipment` (`id`, `numSerie`, `anio`, `date_created`, `date_modified`, `content`, `etiqueta_file`, `user_id`, `client_id`, `modelo_id`, `frecuencia_id`) VALUES
(1, '121116-2/1221', '2012', '2022-05-21 04:37:49', '2023-07-13 21:58:02', 'IP: 192.168.0.100', '121116-2_1221.pdf', 1, 1, 13, 27),
(2, '193454-2/0719', '2012', '2022-05-21 04:39:05', '2023-06-28 16:45:44', 'IP: 192.168.0.101', NULL, 5, 1, 2, 159),
(3, '213454-2/0222', '2013', '2022-05-21 04:57:38', '2023-06-28 16:46:50', '', NULL, 5, 1, 3, 155),
(4, '227455-2/0123', '2014', '2022-05-21 04:59:10', '2023-06-28 16:47:11', 'IP: 192.168.0.101', NULL, 5, 1, 1, 163),
(5, '243454-2/0722', '2014', '2022-05-21 05:01:19', '2022-05-21 05:01:19', 'IP: 192.168.0.101', NULL, 1, 2, 2, 160),
(6, '223154-3/0722', '2018', '2022-05-21 05:01:34', '2023-06-28 13:26:50', '', NULL, 1, 1, 4, 163),
(7, '223454-4/0722', '2019', '2022-05-21 05:10:24', '2023-07-03 13:46:09', '', NULL, 1, 1, 19, 22),
(8, '223464-5/0722', '2019', '2022-05-21 14:43:33', '2023-04-20 23:33:17', NULL, NULL, 1, 1, 19, 19),
(9, '223354-6/0722', '2022', '2022-05-21 14:44:12', '2023-06-28 17:27:11', '', NULL, 1, 1, 4, 156),
(10, '223454-7/0722', '2020', '2022-05-21 14:45:55', '2023-04-20 23:32:56', NULL, NULL, 1, 1, 5, 167),
(11, '213454-2/0722', '2020', '2022-05-24 02:20:00', '2023-04-20 23:32:04', NULL, NULL, 1, 3, 11, 19),
(12, '223554-2/0722', '2020', '2022-05-25 14:58:24', '2023-04-20 23:31:54', NULL, NULL, 1, 6, 11, 25),
(13, '223454-11/0722', '2021', '2022-05-30 02:41:13', '2023-04-20 23:31:42', NULL, NULL, 1, 3, 23, 17),
(15, '223454-2/0724', '2021', '2022-06-13 03:21:29', '2023-06-24 19:33:04', '\r\n', NULL, 1, 3, 15, 19),
(16, '12345432/8765', '2022', '2022-06-13 03:22:03', '2023-06-24 19:35:36', '', NULL, 10, 6, 19, 31),
(17, '213454-3/0522', '2022', '2022-06-13 03:30:03', '2023-06-17 15:12:17', NULL, NULL, 1, 4, 1, 189),
(18, '190722-1/1219', '2019', '2022-06-13 20:56:51', '2023-06-24 13:58:46', '', NULL, 1, 4, 22, 16),
(19, '190722-2/1219', '2012', '2022-06-13 21:26:02', '2023-06-28 17:35:02', '', NULL, 1, 1, 1, 167),
(20, '190722-3/1219', '2012', '2022-06-22 21:32:29', '2023-04-20 23:30:59', 'Rack: 6 modulos \narmado: completo\nfirmado: Oscar\ntel tecnico: 0345-2321387\nmanual: DMTRUD1200-22.pdf', NULL, 1, 18, 26, 18),
(21, '020823-1/0423', '2023', '2022-06-23 01:15:03', '2023-06-28 13:45:09', '', NULL, 10, 1, 25, 124),
(22, '220223-1/0422', '2016', '2022-06-22 22:16:56', '2023-06-17 15:10:29', NULL, NULL, 1, 4, 46, 7),
(23, '223494-2/0722', '2022', '2022-06-22 22:19:54', '2023-06-17 15:08:41', NULL, NULL, 10, 4, 25, 30),
(33, '230504-1/8765', '2023', '2023-04-20 23:24:06', '2023-06-14 13:45:31', 'Encoder LP211_IP: 192.168.1.30\r\nMultiplexor DMUX1000_IP: 192.168.1.40\r\nModulador 3542_IP: 192.168.1.90', NULL, 10, 16, 38, 1),
(34, '190122-1/1219', '2023', '2023-05-20 14:39:38', '2023-06-17 16:48:53', 'IP: 192.168.0.90\r\nNuevo multiplexor de videoswitch', NULL, 1, 2, 37, 31),
(37, '190322-1/1219', '2015', '2023-05-20 14:57:38', '2023-06-17 16:48:09', 'IP: 192.168.1.90\r\nmodulador chino, 13 segmentos capa A', NULL, 1, 18, 1, 1),
(59, '220722-1/1223', '2020', '2023-06-05 19:33:17', '2023-07-04 10:28:08', '(ex canal: 14)', NULL, 10, 3, 37, 13),
(68, '190522-2/1220', '2023', '2023-06-14 13:07:56', '2023-06-29 13:37:10', '', NULL, 10, 1, 46, 5),
(71, '123456-1/0423', '2024', '2023-06-28 13:35:42', '2023-07-03 19:33:05', '', NULL, 10, 1, 5, 152),
(72, '230617-3/0723', 'N/D', '2023-07-03 23:53:09', '2023-07-04 00:39:12', '', NULL, 10, 1, 3, 111),
(85, '230617-2/0723', 'N/D', '2023-07-04 00:23:41', '2023-07-04 00:23:41', '', NULL, 10, 1, 1, 2),
(87, '230617-1/0723', '2023', '2023-07-04 21:36:14', '2023-07-06 10:23:31', '', NULL, 10, 6, 1, 161),
(90, '190516-1/0819', '2019', '2023-07-06 12:07:16', '2023-07-13 21:56:19', '', '190516-1_0819.pdf', 10, 6, 46, 5),
(92, '220101-1/0222', '2022', '2023-07-07 11:44:41', '2023-07-12 11:57:16', '16QAM modo3 convolución 5/6 IG: 1/16\r\n#1 señal 9 MBps \"FIVE TV\"\r\n#2 señal 3,5 MBps \"TV Channel\"', NULL, 10, 17, 37, 16),
(93, '220101-2/0122', '2022', '2023-07-07 11:44:41', '2023-07-07 11:44:41', '', '220101-2_0122.pdf', 10, 17, 13, 16);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_or`
--

DROP TABLE IF EXISTS `estado_or`;
CREATE TABLE IF NOT EXISTS `estado_or` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `estado_or`
--

INSERT INTO `estado_or` (`id`, `descripcion`) VALUES
(1, 'Creada'),
(2, 'Asignada'),
(3, 'Anulada'),
(4, 'Finalizada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `frecuencia`
--

DROP TABLE IF EXISTS `frecuencia`;
CREATE TABLE IF NOT EXISTS `frecuencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `canal` varchar(50) NOT NULL,
  `unidad_id` int(11) NOT NULL DEFAULT '6',
  PRIMARY KEY (`id`),
  KEY `frec_unidad` (`unidad_id`)
) ENGINE=InnoDB AUTO_INCREMENT=318 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `frecuencia`
--

INSERT INTO `frecuencia` (`id`, `canal`, `unidad_id`) VALUES
(0, 'N/D', 6),
(1, '1', 4),
(2, '2', 4),
(3, '3', 4),
(4, '4', 4),
(5, '5', 4),
(6, '6', 4),
(7, '7', 4),
(8, '8', 4),
(9, '9', 4),
(10, '10', 4),
(11, '11', 4),
(12, '12', 4),
(13, '13', 4),
(14, '14', 5),
(15, '15', 5),
(16, '16', 5),
(17, '17', 5),
(18, '18', 5),
(19, '19', 5),
(20, '20', 5),
(21, '21', 5),
(22, '22', 5),
(23, '23', 5),
(24, '24', 5),
(25, '25', 5),
(26, '26', 5),
(27, '27', 5),
(28, '28', 5),
(29, '29', 5),
(30, '30', 5),
(31, '31', 5),
(32, '32', 5),
(33, '33', 5),
(34, '34', 5),
(35, '35', 5),
(36, '36', 5),
(37, '37', 5),
(38, '38', 5),
(39, '39', 5),
(40, '40', 5),
(41, '41', 5),
(42, '42', 5),
(43, '43', 5),
(44, '44', 5),
(45, '45', 5),
(46, '46', 5),
(47, '47', 5),
(48, '48', 5),
(49, '49', 5),
(50, '50', 5),
(51, '51', 5),
(52, '52', 5),
(53, '53', 5),
(54, '54', 5),
(55, '55', 5),
(56, '56', 5),
(57, '57', 5),
(58, '58', 5),
(59, '59', 5),
(60, '60', 5),
(61, '61', 5),
(62, '62', 5),
(63, '63', 5),
(64, '64', 5),
(65, '65', 5),
(66, '66', 5),
(67, '67', 5),
(68, '68', 5),
(69, '69', 5),
(70, '70', 5),
(71, '71', 5),
(72, '72', 5),
(73, '73', 5),
(74, '74', 5),
(75, '75', 5),
(76, '76', 5),
(77, '77', 5),
(78, '78', 5),
(79, '79', 5),
(80, '80', 5),
(81, '81', 5),
(82, '82', 5),
(83, '83', 5),
(84, '84', 5),
(85, '85', 5),
(86, '86', 5),
(87, '87', 5),
(88, '88', 5),
(89, '89', 5),
(90, '90', 5),
(91, '91', 5),
(92, '92', 5),
(93, '93', 5),
(94, '94', 5),
(95, '95', 5),
(96, '96', 5),
(97, '97', 5),
(98, '98', 5),
(99, '99', 5),
(100, '87.9', 2),
(101, '88.1', 2),
(102, '88.3', 2),
(103, '88.5', 2),
(104, '88.7', 2),
(105, '88.9', 2),
(106, '89.1', 2),
(107, '89.3', 2),
(108, '89.5', 2),
(109, '89.7', 2),
(110, '89.9', 2),
(111, '90.1', 2),
(112, '90.3', 2),
(113, '90.5', 2),
(114, '90.7', 2),
(115, '90.9', 2),
(116, '91.1', 2),
(117, '91.3', 2),
(118, '91.5', 2),
(119, '91.7', 2),
(120, '91.9', 2),
(121, '92.1', 2),
(122, '92.3', 2),
(123, '92.5', 2),
(124, '92.7', 2),
(125, '92.9', 2),
(126, '93.1', 2),
(127, '93.3', 2),
(128, '93.5', 2),
(129, '93.7', 2),
(130, '93.9', 2),
(131, '94.1', 2),
(132, '94.3', 2),
(133, '94.5', 2),
(134, '94.7', 2),
(135, '94.9', 2),
(136, '95.1', 2),
(137, '95.3', 2),
(138, '95.5', 2),
(139, '95.7', 2),
(140, '95.9', 2),
(141, '96.1', 2),
(142, '96.3', 2),
(143, '96.5', 2),
(144, '96.7', 2),
(145, '96.9', 2),
(146, '97.1', 2),
(147, '97.3', 2),
(148, '97.5', 2),
(149, '97.7', 2),
(150, '97.9', 2),
(151, '98.1', 2),
(152, '98.3', 2),
(153, '98.5', 2),
(154, '98.7', 2),
(155, '98.9', 2),
(156, '99.1', 2),
(157, '99.3', 2),
(158, '99.5', 2),
(159, '99.7', 2),
(160, '99.9', 2),
(161, '100.1', 2),
(162, '100.3', 2),
(163, '100.5', 2),
(164, '100.7', 2),
(165, '100.9', 2),
(166, '101.1', 2),
(167, '101.3', 2),
(168, '101.5', 2),
(169, '101.7', 2),
(170, '101.9', 2),
(171, '102.1', 2),
(172, '102.3', 2),
(173, '102.5', 2),
(174, '102.7', 2),
(175, '102.9', 2),
(176, '103.1', 2),
(177, '103.3', 2),
(178, '103.5', 2),
(179, '103.7', 2),
(180, '103.9', 2),
(181, '104.1', 2),
(182, '104.3', 2),
(183, '104.5', 2),
(184, '104.7', 2),
(185, '104.9', 2),
(186, '105.1', 2),
(187, '105.3', 2),
(188, '105.5', 2),
(189, '105.7', 2),
(190, '105.9', 2),
(191, '106.1', 2),
(192, '106.3', 2),
(193, '106.5', 2),
(194, '106.7', 2),
(195, '106.9', 2),
(196, '107.1', 2),
(197, '107.3', 2),
(198, '107.5', 2),
(199, '107.7', 2),
(200, '107.9', 2),
(201, '540', 1),
(202, '550', 1),
(203, '560', 1),
(204, '570', 1),
(205, '580', 1),
(206, '590', 1),
(207, '600', 1),
(208, '610', 1),
(209, '620', 1),
(210, '630', 1),
(211, '640', 1),
(212, '650', 1),
(213, '660', 1),
(214, '670', 1),
(215, '680', 1),
(216, '690', 1),
(217, '700', 1),
(218, '710', 1),
(219, '720', 1),
(220, '730', 1),
(221, '740', 1),
(222, '750', 1),
(223, '760', 1),
(224, '770', 1),
(225, '780', 1),
(226, '790', 1),
(227, '800', 1),
(228, '810', 1),
(229, '820', 1),
(230, '830', 1),
(231, '840', 1),
(232, '850', 1),
(233, '860', 1),
(234, '870', 1),
(235, '880', 1),
(236, '890', 1),
(237, '900', 1),
(238, '910', 1),
(239, '920', 1),
(240, '930', 1),
(241, '940', 1),
(242, '950', 1),
(243, '960', 1),
(244, '970', 1),
(245, '980', 1),
(246, '990', 1),
(247, '1000', 1),
(248, '1010', 1),
(249, '1020', 1),
(250, '1030', 1),
(251, '1040', 1),
(252, '1050', 1),
(253, '1060', 1),
(254, '1070', 1),
(255, '1080', 1),
(256, '1090', 1),
(257, '1100', 1),
(258, '1110', 1),
(259, '1120', 1),
(260, '1130', 1),
(261, '1140', 1),
(262, '1150', 1),
(263, '1160', 1),
(264, '1170', 1),
(265, '1180', 1),
(266, '1190', 1),
(267, '1200', 1),
(268, '1210', 1),
(269, '1220', 1),
(270, '1230', 1),
(271, '1240', 1),
(272, '1250', 1),
(273, '1260', 1),
(274, '1270', 1),
(275, '1280', 1),
(276, '1290', 1),
(277, '1300', 1),
(278, '1310', 1),
(279, '1320', 1),
(280, '1330', 1),
(281, '1340', 1),
(282, '1350', 1),
(283, '1360', 1),
(284, '1370', 1),
(285, '1380', 1),
(286, '1390', 1),
(287, '1400', 1),
(288, '1410', 1),
(289, '1420', 1),
(290, '1430', 1),
(291, '1440', 1),
(292, '1450', 1),
(293, '1460', 1),
(294, '1470', 1),
(295, '1480', 1),
(296, '1490', 1),
(297, '1500', 1),
(298, '1510', 1),
(299, '1520', 1),
(300, '1530', 1),
(301, '1540', 1),
(302, '1550', 1),
(303, '1560', 1),
(304, '1570', 1),
(305, '1580', 1),
(306, '1590', 1),
(307, '1600', 1),
(308, '1610', 1),
(309, '1620', 1),
(310, '1630', 1),
(311, '1640', 1),
(312, '1650', 1),
(313, '1660', 1),
(314, '1670', 1),
(315, '1680', 1),
(316, '1690', 1),
(317, '1700', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historia`
--

DROP TABLE IF EXISTS `historia`;
CREATE TABLE IF NOT EXISTS `historia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(1000) DEFAULT NULL,
  `tipologia_id` int(11) NOT NULL,
  `equipo_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `equipment_id` (`equipo_id`),
  KEY `historia_tipo` (`tipologia_id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `historia`
--

INSERT INTO `historia` (`id`, `title`, `date_created`, `date_modified`, `content`, `tipologia_id`, `equipo_id`, `user_id`) VALUES
(1, 'Reparacion ventiladores', '2023-06-04 12:16:37', '2023-06-04 12:16:37', 'Se desarmo el equipo y se constato que los ventiladores no funcionaban por lo que se procedió a cambiarlos y eso resolvió el problema', 2, 21, 10),
(5, 'Cambio de IP', '2023-06-05 16:02:19', '2023-06-05 16:02:19', '192.168.1.101', 3, 33, 10),
(15, 'Linealidad', '2023-06-05 19:33:17', '2023-06-05 19:33:17', 'equipo ex TRU400, se linealizo para uso digital, y se hizo uso extremo de la potencia para mantener la pot nominal RMS', 1, 1, 10),
(16, 'retraso en entrega', '2023-06-13 11:08:00', '2023-06-13 11:08:00', 'la entrega se realizo dos semana después de lo pactado', 1, 59, 10),
(17, 'verificacion por pedido del cliente', '2023-06-14 13:34:50', '2023-06-14 13:34:50', 'se reviso a fondo!', 2, 33, 10),
(18, 'ventiladores', '2023-06-15 15:40:48', '2023-06-15 15:40:48', 'se cambiaron los ventiladores del equipo', 2, 1, 1),
(23, 'envio de equipo', '2023-06-16 15:56:55', '2023-06-16 15:56:55', 'Se programó un envío para el 25/08/22. Se aguarda confirmación', 1, 23, 10),
(24, 'linealidad', '2023-06-16 15:56:55', '2023-06-16 15:56:55', 'consultó por modificar la linealidad del amplificador para ser usado para TV digital', 3, 23, 10),
(25, 'cambio IP', '2023-06-16 20:27:27', '2023-06-16 20:27:27', 'IP: 10.0.0.97', 1, 23, 1),
(26, 'fotos', '2023-06-16 20:27:27', '2023-06-16 20:27:27', 'se sacaron fotos del frente y fondo', 1, 23, 1),
(27, 'manual', '2023-06-17 15:03:51', '2023-06-17 15:03:51', 'Manual enviado via mail', 1, 21, 10),
(28, 'actualización', '2023-06-17 15:03:51', '2023-06-17 15:03:51', 'equipo reacondicionado y actualizado a versión \'22', 3, 17, 10),
(29, 'Modelo equipo', '2023-06-17 15:21:08', '2023-06-17 15:21:08', 'modelo original TRU250', 1, 18, 10),
(31, 'modelo', '2023-06-17 16:29:37', '2023-06-17 16:29:37', 'Este equipo es modelo 2023\r\nTomado de un modelo 2016', 3, 68, 1),
(32, 'cambio fuente', '2023-06-24 19:08:21', '2023-06-24 19:08:21', 'una descarga quemó la fuente del sumador', 2, 15, 10),
(33, 'cambio ventiladores', '2023-06-24 19:08:21', '2023-06-24 19:08:21', 'se repararon 2 ventiladores forzadores de aire del control general', 2, 15, 10),
(34, 'nueva señal', '2023-06-24 19:08:21', '2023-06-24 19:08:21', 'se agregó una señal de tv digital al Mux\r\n', 3, 15, 10),
(35, 'cambio frec', '2023-06-24 19:33:39', '2023-06-24 19:33:39', 'Se cambió la frecuencia del modulador a CH:13', 3, 16, 10),
(36, 'modulos quemados', '2023-06-24 19:33:39', '2023-06-24 19:33:39', 'Reparación de dos módulos de potencia (Atilio)', 2, 19, 10),
(39, 'cambio IP', '2023-06-28 16:45:23', '2023-06-28 16:45:23', '192.168.0.136', 1, 9, 10),
(40, 'IP', '2023-06-29 11:11:55', '2023-06-29 11:11:55', 'IP192.168.1.12', 1, 71, 10),
(41, 'IP', '2023-07-05 09:51:15', '2023-07-05 09:51:15', 'IP: 192.168.1.136', 3, 87, 10),
(42, 'IP', '2023-07-07 10:12:24', '2023-07-07 11:23:31', '192.168.1.100', 3, 90, 10),
(43, 'Cambio ventiladores', '2023-07-07 10:12:24', '2023-07-07 10:12:24', 'Se reemplazaron los ventiladores de 220 por unos de 48V', 2, 90, 10),
(44, 'IP', '2023-07-07 11:44:41', '2023-07-07 11:44:41', '192.168.1.136', 1, 92, 10),
(45, 'Codec audio', '2023-07-07 11:44:41', '2023-07-07 11:44:41', 'MPEG2- mejor recepción de clientes', 1, 92, 10),
(46, 'Ficha alimentación', '2023-07-07 11:44:41', '2023-07-10 16:34:07', 'falla en la ficha de alimentación del mod, se asistió por teléfono para encontrar la falla.', 2, 93, 10),
(47, 'Señal #2', '2023-07-07 11:44:41', '2023-07-07 11:44:41', 'se agregó la señal 16.2', 3, 93, 10),
(48, 'charla con cliente', '2023-07-07 13:45:43', '2023-07-07 13:45:43', 'todo OK', 1, 22, 10),
(49, 'IP', '2023-07-07 13:45:43', '2023-07-07 13:45:43', '192.168.1.100', 3, 22, 10),
(50, 'Fuente', '2023-07-07 20:51:42', '2023-07-07 20:51:42', 'cambio de la fuente switching 200W', 2, 90, 10),
(53, 'IP', '2023-07-10 18:00:27', '2023-07-10 18:00:27', '192.168.1.100', 1, 72, 5),
(54, '230712', '2023-07-12 09:29:31', '2023-07-12 09:29:31', 'Se constató que había una falla en el conector de salida de RF lo que producía la falla de >>ROE. Al cambiar el conector el equipo quedó funcionando bien.', 2, 20, 14),
(56, 'cambio de \"ENT RF\"', '2023-07-15 00:03:03', '2023-07-15 00:04:11', 'se cambió el conector \"F\" por un \"BNC\"', 3, 1, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `homologacion`
--

DROP TABLE IF EXISTS `homologacion`;
CREATE TABLE IF NOT EXISTS `homologacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(15) NOT NULL,
  `modelo` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_homologacion_codigo` (`codigo`),
  UNIQUE KEY `uq_homologacion_modelo` (`modelo`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `homologacion`
--

INSERT INTO `homologacion` (`id`, `codigo`, `modelo`) VALUES
(1, 'H-16503', 'FM50'),
(2, 'H-16505', 'FM100'),
(3, '32-522', 'FM250'),
(4, '32-407', 'FM500'),
(5, 'H-23104', 'FM1000'),
(6, 'H-23105', 'FM2000'),
(7, 'H-22011', 'FM5000'),
(8, 'C-22679', 'FM10.000'),
(9, 'C-15701', 'TRUD250'),
(10, 'C-15697', 'TRUD500'),
(11, 'C-12130', 'TRUD1200'),
(12, '40-155', 'TRV100');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `localidad`
--

DROP TABLE IF EXISTS `localidad`;
CREATE TABLE IF NOT EXISTS `localidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cp` int(4) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `provincia_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ciudad_prov` (`provincia_id`)
) ENGINE=InnoDB AUTO_INCREMENT=975 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `localidad`
--

INSERT INTO `localidad` (`id`, `cp`, `nombre`, `provincia_id`) VALUES
(3, 6300, 'Santa Rosa', 11),
(4, 6360, 'General Pico', 11),
(5, 6301, 'Toay', 11),
(6, 6338, '25 de Mayo', 11),
(7, 6383, 'Quemú Quemú', 11),
(8, 6380, 'Realicó', 11),
(9, 6305, 'Victorica', 11),
(10, 6313, 'Macachín', 11),
(11, 6385, 'Eduardo Castex', 11),
(12, 6360, 'General Acha', 11),
(13, 6361, 'Trenel', 11),
(14, 6382, 'Intendente Alvear', 11),
(15, 6367, 'Ingeniero Luiggi', 11),
(16, 6334, 'General Campos', 11),
(17, 6336, 'Miguel Riglos', 11),
(18, 6363, 'Colonia Barón', 11),
(19, 6365, 'Dorila', 11),
(20, 6369, 'Rancul', 11),
(21, 6307, 'Anguil', 11),
(22, 6348, 'Alta Italia', 11),
(23, 6342, 'Bernardo Larroudé', 11),
(24, 6344, 'Caleufú', 11),
(25, 6319, 'Parera', 11),
(26, 6362, 'Rolón', 11),
(27, 6364, 'Colonia Santa María', 11),
(28, 6340, 'Arata', 11),
(29, 6303, 'Ataliva Roca', 11),
(30, 6366, 'Embajador Martini', 11),
(31, 6368, 'La Maruja', 11),
(32, 6305, 'La Adela', 11),
(33, 5000, 'Córdoba', 6),
(34, 5012, 'Villa Revol', 6),
(35, 5014, 'Villa El Libertador', 6),
(36, 5016, 'Villa Belgrano', 6),
(37, 5018, 'Villa Urquiza', 6),
(38, 5020, 'Alta Córdoba', 6),
(39, 5022, 'General Bustos', 6),
(40, 5024, 'Centro América', 6),
(41, 5026, 'Barrio San Vicente', 6),
(42, 5028, 'General Paz', 6),
(43, 5030, 'Nueva Córdoba', 6),
(44, 5032, 'Cofico', 6),
(45, 5034, 'Barrio Jardín', 6),
(46, 5036, 'Barrio Juniors', 6),
(47, 5038, 'Barrio Residencial San Roque', 6),
(48, 5040, 'Barrio San Martín', 6),
(49, 5042, 'Barrio Observatorio', 6),
(50, 5044, 'Barrio Talleres', 6),
(51, 5046, 'Barrio Alberdi', 6),
(52, 5048, 'Barrio San Ignacio', 6),
(53, 5050, 'Barrio General Bustos', 6),
(54, 5052, 'Barrio Parque Capital', 6),
(55, 5054, 'Barrio Crisol', 6),
(56, 5056, 'Barrio Jardín Espinosa', 6),
(57, 5058, 'Barrio Marqués de Sobremonte', 6),
(58, 5060, 'Barrio Nuestro Hogar III', 6),
(59, 5062, 'Barrio Ampliación San Pablo', 6),
(60, 5064, 'Barrio La France', 6),
(61, 5066, 'Barrio Yofre Sud', 6),
(62, 5068, 'Barrio Parque Atlántica', 6),
(63, 5070, 'Barrio Altamira', 6),
(64, 5072, 'Barrio Maipú', 6),
(65, 5074, 'Barrio Mariano Fragueiro', 6),
(66, 5076, 'Barrio Maldonado', 6),
(67, 5078, 'Barrio Los Paraísos', 6),
(68, 5080, 'Barrio Ampliación Los Plátanos', 6),
(69, 5082, 'Barrio Parque Atlántica Oeste', 6),
(70, 5084, 'Barrio Residencial Santa Ana', 6),
(71, 5086, 'Barrio San Felipe', 6),
(72, 5088, 'Barrio General Bustos', 6),
(73, 5090, 'Barrio Residencial San Antonio', 6),
(74, 5092, 'Barrio Comercial', 6),
(75, 5094, 'Barrio Residencial América', 6),
(76, 5096, 'Barrio Jardín Espinosa', 6),
(77, 5098, 'Barrio Villa La Tela', 6),
(78, 5100, 'Barrio General Deheza', 6),
(79, 5101, 'Unquillo', 6),
(80, 5103, 'Río Ceballos', 6),
(81, 5105, 'Salsipuedes', 6),
(82, 5107, 'Agua de Oro', 6),
(83, 5109, 'Colonia Caroya', 6),
(84, 5111, 'Villa Allende', 6),
(85, 5113, 'Mendiolaza', 6),
(86, 5115, 'Villa Los Llanos', 6),
(87, 5117, 'La Calera', 6),
(88, 5119, 'Malagueño', 6),
(89, 5121, 'Cosquín', 6),
(90, 5123, 'Santa María de Punilla', 6),
(91, 5125, 'La Falda', 6),
(92, 5127, 'Huerta Grande', 6),
(93, 5129, 'Villa Giardino', 6),
(94, 5132, 'Carlos Paz', 6),
(95, 5133, 'Tanti', 6),
(96, 5135, 'Villa Carlos Paz', 6),
(97, 5137, 'Los Cocos', 6),
(98, 5139, 'San Antonio de Arredondo', 6),
(99, 5141, 'Villa del Lago', 6),
(100, 5143, 'Bialet Massé', 6),
(101, 5145, 'San Roque', 6),
(102, 5147, 'Villa Parque Síquiman', 6),
(103, 5149, 'Estancia Vieja', 6),
(104, 5152, 'Unquillo', 6),
(105, 5153, 'Colonia Caroya', 6),
(106, 5155, 'Río Ceballos', 6),
(107, 5157, 'Salsipuedes', 6),
(108, 5159, 'Agua de Oro', 6),
(109, 5161, 'Villa Allende', 6),
(110, 5163, 'Mendiolaza', 6),
(111, 5165, 'Villa Los Llanos', 6),
(112, 5167, 'La Calera', 6),
(113, 5169, 'Malagueño', 6),
(114, 5171, 'Cosquín', 6),
(115, 5173, 'Santa María de Punilla', 6),
(116, 5174, 'La Falda', 6),
(117, 5175, 'Huerta Grande', 6),
(118, 5176, 'Villa Giardino', 6),
(119, 5178, 'Carlos Paz', 6),
(120, 5180, 'Tanti', 6),
(121, 5182, 'Villa Carlos Paz', 6),
(122, 5184, 'Los Cocos', 6),
(123, 5186, 'San Antonio de Arredondo', 6),
(124, 5187, 'Villa del Lago', 6),
(125, 5189, 'Bialet Massé', 6),
(126, 5191, 'San Roque', 6),
(127, 5193, 'Villa Parque Síquiman', 6),
(128, 5195, 'Estancia Vieja', 6),
(129, 5200, 'Villa Dolores', 6),
(130, 5201, 'San Javier', 6),
(131, 5203, 'Merlo', 6),
(132, 5205, 'Mina Clavero', 6),
(133, 5207, 'Los Cocos', 6),
(134, 5209, 'Villa General Belgrano', 6),
(135, 5210, 'La Cumbrecita', 6),
(136, 5211, 'Santa Rosa de Calamuchita', 6),
(137, 5212, 'Embalse', 6),
(138, 5213, 'Villa Rumipal', 6),
(139, 5214, 'Yacanto', 6),
(140, 5216, 'Río de los Sauces', 6),
(141, 5218, 'Villa de Las Rosas', 6),
(142, 5220, 'San Agustín', 6),
(143, 5221, 'San Francisco', 6),
(144, 5223, 'Villa Santa Cruz del Lago', 6),
(145, 5225, 'Casa Grande', 6),
(146, 5227, 'Villa del Dique', 6),
(147, 5229, 'Amboy', 6),
(148, 5231, 'Santa Rosa', 6),
(149, 5233, 'Embalse', 6),
(150, 5235, 'Villa Quillinzo', 6),
(151, 5237, 'La Cruz', 6),
(152, 5239, 'Los Molinos', 6),
(153, 5241, 'Dique Los Molinos', 6),
(154, 5243, 'Los Reartes', 6),
(155, 5245, 'Alta Gracia', 6),
(156, 5246, 'Anisacate', 6),
(157, 5248, 'La Paisanita', 6),
(158, 5250, 'Despeñaderos', 6),
(159, 5252, 'Villa Los Aromos', 6),
(160, 5254, 'Los Cedros', 6),
(161, 5256, 'Los Aromos', 6),
(162, 5258, 'San Ignacio', 6),
(163, 5260, 'Villa Santa Cruz', 6),
(164, 5262, 'Potrero de Garay', 6),
(165, 5264, 'Villa Ciudad de América', 6),
(166, 5266, 'Alpa Corral', 6),
(167, 5268, 'Los Hornillos', 6),
(168, 5270, 'La Falda', 6),
(169, 5271, 'La Cumbre', 6),
(170, 5273, 'Valle Hermoso', 6),
(171, 5275, 'Huerta Grande', 6),
(172, 5277, 'Capilla del Monte', 6),
(173, 5279, 'San Marcos Sierras', 6),
(174, 5280, 'Villa de Soto', 6),
(175, 5282, 'Villa Dolores', 6),
(176, 5284, 'Mina Clavero', 6),
(177, 5286, 'Nono', 6),
(178, 5288, 'Villa Cura Brochero', 6),
(179, 5291, 'Villa Berna', 6),
(180, 5293, 'Las Rabonas', 6),
(181, 5295, 'Villa El Chacay', 6),
(182, 5297, 'Villa Las Rosas', 6),
(183, 5299, 'Villa de Las Rosas', 6),
(184, 4600, 'San Salvador de Jujuy', 10),
(185, 4601, 'Barrio Belgrano', 10),
(186, 4602, 'Palpalá', 10),
(187, 4603, 'San Pedro', 10),
(188, 4604, 'Barrio Gorriti', 10),
(189, 4605, 'Barrio Los Perales', 10),
(190, 4606, 'San Antonio', 10),
(191, 4607, 'Monterrico', 10),
(192, 4608, 'Yala', 10),
(193, 4609, 'Libertador General San Martín', 10),
(194, 4610, 'Barrio Los Huaicos', 10),
(195, 4611, 'Tilcara', 10),
(196, 4612, 'Barrio Ciudad de Nieva', 10),
(197, 4613, 'Purmamarca', 10),
(198, 4614, 'Maimará', 10),
(199, 4615, 'Volcán', 10),
(200, 4616, 'Uquía', 10),
(201, 4617, 'Humahuaca', 10),
(202, 4618, 'El Carmen', 10),
(203, 4619, 'La Quiaca', 10),
(204, 1000, 'La Plata', 1),
(205, 1001, 'Barrio Norte', 1),
(206, 1002, 'Monserrat', 1),
(207, 1003, 'San Telmo', 1),
(208, 1004, 'Retiro', 1),
(209, 1005, 'San Nicolás', 1),
(210, 1006, 'Balvanera', 1),
(211, 1007, 'San Cristóbal', 1),
(212, 1008, 'Puerto Madero', 1),
(213, 1009, 'Montserrat', 1),
(214, 1010, 'Recoleta', 1),
(215, 1011, 'Barrio Parque', 1),
(216, 1012, 'Palermo', 1),
(217, 1013, 'Belgrano', 1),
(218, 1014, 'Nuñez', 1),
(219, 1015, 'Saavedra', 1),
(220, 1016, 'Villa Urquiza', 1),
(221, 1017, 'Colegiales', 1),
(222, 1018, 'Chacarita', 1),
(223, 1019, 'Villa Crespo', 1),
(224, 1020, 'Almagro', 1),
(225, 1021, 'Caballito', 1),
(226, 1022, 'Boedo', 1),
(227, 1023, 'Flores', 1),
(228, 1024, 'Parque Chacabuco', 1),
(229, 1025, 'Parque Avellaneda', 1),
(230, 1026, 'Mataderos', 1),
(231, 1027, 'Villa Lugano', 1),
(232, 1028, 'Villa Riachuelo', 1),
(233, 1029, 'Villa Soldati', 1),
(234, 1030, 'Villa Luro', 1),
(235, 1031, 'Vélez Sársfield', 1),
(236, 1032, 'Floresta', 1),
(237, 1033, 'Monte Castro', 1),
(238, 1034, 'Villa Real', 1),
(239, 1035, 'Versalles', 1),
(240, 1036, 'Villa Devoto', 1),
(241, 1037, 'Villa del Parque', 1),
(242, 1038, 'Villa Santa Rita', 1),
(243, 1039, 'Agronomía', 1),
(244, 1040, 'Parque Centenario', 1),
(245, 1041, 'Paternal', 1),
(246, 1042, 'Villa General Mitre', 1),
(247, 1043, 'Villa Pueyrredón', 1),
(248, 1044, 'Coghlan', 1),
(249, 1045, 'Saenz Peña', 1),
(250, 1046, 'Villa Ortúzar', 1),
(251, 1047, 'Villa del Parque', 1),
(252, 1048, 'Villa Riachuelo', 1),
(253, 1049, 'Villa Lugano', 1),
(254, 1050, 'Villa Soldati', 1),
(255, 1051, 'Villa Luro', 1),
(256, 1052, 'Vélez Sársfield', 1),
(257, 1053, 'Floresta', 1),
(258, 1054, 'Monte Castro', 1),
(259, 1055, 'Villa Real', 1),
(260, 1056, 'Versalles', 1),
(261, 1057, 'Villa Devoto', 1),
(262, 1058, 'Villa del Parque', 1),
(263, 1059, 'Villa Santa Rita', 1),
(264, 1060, 'Agronomía', 1),
(265, 1061, 'Parque Centenario', 1),
(266, 1062, 'Paternal', 1),
(267, 1063, 'Villa General Mitre', 1),
(268, 1064, 'Villa Pueyrredón', 1),
(269, 1065, 'Coghlan', 1),
(270, 1066, 'Saenz Peña', 1),
(271, 1067, 'Villa Ortúzar', 1),
(272, 1068, 'Villa del Parque', 1),
(273, 1069, 'Villa Riachuelo', 1),
(274, 1070, 'Villa Lugano', 1),
(275, 1071, 'Villa Soldati', 1),
(276, 1072, 'Villa Luro', 1),
(277, 1073, 'Vélez Sársfield', 1),
(278, 1074, 'Floresta', 1),
(279, 1075, 'Monte Castro', 1),
(280, 1076, 'Villa Real', 1),
(281, 1077, 'Versalles', 1),
(282, 1078, 'Villa Devoto', 1),
(283, 1079, 'Villa del Parque', 1),
(284, 1080, 'Villa Santa Rita', 1),
(285, 1081, 'Agronomía', 1),
(286, 1082, 'Parque Centenario', 1),
(287, 1083, 'Paternal', 1),
(288, 1084, 'Villa General Mitre', 1),
(289, 1085, 'Villa Pueyrredón', 1),
(290, 1086, 'Coghlan', 1),
(291, 1087, 'Saenz Peña', 1),
(292, 1088, 'Villa Ortúzar', 1),
(293, 1089, 'Villa del Parque', 1),
(294, 1090, 'Villa Riachuelo', 1),
(295, 1091, 'Villa Lugano', 1),
(296, 1092, 'Villa Soldati', 1),
(297, 1093, 'Villa Luro', 1),
(298, 1094, 'Vélez Sársfield', 1),
(299, 1095, 'Floresta', 1),
(300, 1096, 'Monte Castro', 1),
(301, 1097, 'Villa Real', 1),
(302, 1098, 'Versalles', 1),
(303, 1099, 'Villa Devoto', 1),
(304, 1100, 'Villa del Parque', 1),
(305, 1000, 'Microcentro', 2),
(306, 1001, 'San Nicolás', 2),
(307, 1002, 'Montserrat', 2),
(308, 1003, 'San Telmo', 2),
(309, 1004, 'Retiro', 2),
(310, 1005, 'Puerto Madero', 2),
(311, 1006, 'San Cristóbal', 2),
(312, 1007, 'Balvanera', 2),
(313, 1008, 'Congreso', 2),
(314, 1009, 'Tribunales', 2),
(315, 1010, 'Recoleta', 2),
(316, 1011, 'Barrio Norte', 2),
(317, 1012, 'Palermo', 2),
(318, 1013, 'Belgrano', 2),
(319, 1014, 'Núñez', 2),
(320, 1015, 'Saavedra', 2),
(321, 1016, 'Coghlan', 2),
(322, 1017, 'Villa Urquiza', 2),
(323, 1018, 'Parque Chas', 2),
(324, 1019, 'Agronomía', 2),
(325, 1020, 'Villa Ortúzar', 2),
(326, 1021, 'Colegiales', 2),
(327, 1022, 'Chacarita', 2),
(328, 1023, 'Villa Crespo', 2),
(329, 1024, 'Almagro', 2),
(330, 1025, 'Boedo', 2),
(331, 1026, 'San Cristóbal', 2),
(332, 1027, 'Balvanera', 2),
(333, 1028, 'San Cristóbal', 2),
(334, 1029, 'Balvanera', 2),
(335, 1030, 'San Telmo', 2),
(336, 1031, 'San Telmo', 2),
(337, 1032, 'San Telmo', 2),
(338, 1033, 'San Telmo', 2),
(339, 1034, 'San Telmo', 2),
(340, 1035, 'Monserrat', 2),
(341, 1036, 'Monserrat', 2),
(342, 1037, 'Monserrat', 2),
(343, 1038, 'Monserrat', 2),
(344, 1039, 'Monserrat', 2),
(345, 1040, 'Retiro', 2),
(346, 1041, 'Retiro', 2),
(347, 1042, 'Retiro', 2),
(348, 1043, 'Retiro', 2),
(349, 1044, 'Retiro', 2),
(350, 1045, 'Puerto Madero', 2),
(351, 1046, 'Puerto Madero', 2),
(352, 1047, 'Puerto Madero', 2),
(353, 1048, 'Puerto Madero', 2),
(354, 1049, 'Puerto Madero', 2),
(355, 1050, 'Recoleta', 2),
(356, 1051, 'Recoleta', 2),
(357, 1052, 'Recoleta', 2),
(358, 1053, 'Recoleta', 2),
(359, 1054, 'Recoleta', 2),
(360, 1055, 'Barrio Norte', 2),
(361, 1056, 'Barrio Norte', 2),
(362, 1057, 'Barrio Norte', 2),
(363, 1058, 'Barrio Norte', 2),
(364, 1059, 'Barrio Norte', 2),
(365, 1060, 'Palermo', 2),
(366, 1061, 'Palermo', 2),
(367, 1062, 'Palermo', 2),
(368, 1063, 'Palermo', 2),
(369, 1064, 'Palermo', 2),
(370, 1065, 'Belgrano', 2),
(371, 1066, 'Belgrano', 2),
(372, 1067, 'Belgrano', 2),
(373, 1068, 'Belgrano', 2),
(374, 1069, 'Belgrano', 2),
(375, 1070, 'Núñez', 2),
(376, 1071, 'Núñez', 2),
(377, 1072, 'Núñez', 2),
(378, 1073, 'Núñez', 2),
(379, 1074, 'Núñez', 2),
(380, 1075, 'Saavedra', 2),
(381, 1076, 'Saavedra', 2),
(382, 1077, 'Saavedra', 2),
(383, 1078, 'Saavedra', 2),
(384, 1079, 'Saavedra', 2),
(385, 1080, 'Coghlan', 2),
(386, 1081, 'Coghlan', 2),
(387, 1082, 'Coghlan', 2),
(388, 1083, 'Coghlan', 2),
(389, 1084, 'Coghlan', 2),
(390, 1085, 'Villa Urquiza', 2),
(391, 1086, 'Villa Urquiza', 2),
(392, 1087, 'Villa Urquiza', 2),
(393, 1088, 'Villa Urquiza', 2),
(394, 1089, 'Villa Urquiza', 2),
(395, 1090, 'Parque Chas', 2),
(396, 1091, 'Parque Chas', 2),
(397, 1092, 'Parque Chas', 2),
(398, 1093, 'Parque Chas', 2),
(399, 1094, 'Parque Chas', 2),
(400, 1095, 'Agronomía', 2),
(401, 1096, 'Agronomía', 2),
(402, 1097, 'Agronomía', 2),
(403, 1098, 'Agronomía', 2),
(404, 1099, 'Agronomía', 2),
(405, 1100, 'Villa Ortúzar', 2),
(406, 5000, 'Córdoba', 6),
(407, 5001, 'Córdoba', 6),
(408, 5002, 'Córdoba', 6),
(409, 5003, 'Córdoba', 6),
(410, 5004, 'Córdoba', 6),
(411, 5005, 'Córdoba', 6),
(412, 5006, 'Córdoba', 6),
(413, 5007, 'Córdoba', 6),
(414, 5008, 'Córdoba', 6),
(415, 5009, 'Córdoba', 6),
(416, 5010, 'Córdoba', 6),
(417, 5011, 'Córdoba', 6),
(418, 5012, 'Córdoba', 6),
(419, 5003, 'Villa Carlos Paz', 6),
(420, 5152, 'Villa Allende', 6),
(421, 5147, 'Río Ceballos', 6),
(422, 5180, 'Cosquín', 6),
(423, 5107, 'La Calera', 6),
(424, 5194, 'Villa General Belgrano', 6),
(425, 5158, 'Unquillo', 6),
(426, 5196, 'Embalse', 6),
(427, 5101, 'Alta Gracia', 6),
(428, 5137, 'Río Segundo', 6),
(429, 5199, 'Santa Rosa de Calamuchita', 6),
(430, 5186, 'Capilla del Monte', 6),
(431, 5153, 'Colonia Caroya', 6),
(432, 5182, 'Villa Giardino', 6),
(433, 5184, 'Huerta Grande', 6),
(434, 5105, 'Jesús María', 6),
(435, 5166, 'Mendiolaza', 6),
(436, 5149, 'Salsipuedes', 6),
(437, 5176, 'Tanti', 6),
(438, 5172, 'Malagueño', 6),
(439, 5191, 'Villa del Dique', 6),
(440, 5189, 'La Falda', 6),
(441, 5188, 'Los Cocos', 6),
(442, 5143, 'Monte Cristo', 6),
(443, 5145, 'Arroyito', 6),
(444, 5109, 'Villa María', 6),
(445, 5168, 'Saldán', 6),
(446, 5190, 'Villa Rumipal', 6),
(447, 5157, 'Río Tercero', 6),
(448, 5103, 'Villa Dolores', 6),
(449, 5141, 'Pilar', 6),
(450, 5164, 'Mina Clavero', 6),
(451, 5160, 'Río Cuarto', 6),
(452, 5170, 'Cosquín', 6),
(453, 5106, 'Deán Funes', 6),
(454, 5178, 'Villa Carlos Paz', 6),
(455, 5174, 'Capilla del Monte', 6),
(456, 5147, 'Oliva', 6),
(457, 5162, 'Villa María', 6),
(458, 5149, 'Bell Ville', 6),
(459, 5168, 'Villa Nueva', 6),
(460, 5141, 'Laboulaye', 6),
(461, 5164, 'Alta Gracia', 6),
(462, 5160, 'Río Tercero', 6),
(463, 5170, 'Morteros', 6),
(464, 5106, 'San Francisco', 6),
(465, 5178, 'Marcos Juárez', 6),
(466, 5174, 'Cruz del Eje', 6),
(467, 5147, 'Las Varillas', 6),
(468, 5162, 'San Marcos Sierras', 6),
(469, 5149, 'San Francisco del Chañar', 6),
(470, 5168, 'Río Ceballos', 6),
(471, 5141, 'Santa Rosa de Río Primero', 6),
(472, 5164, 'Las Varas', 6),
(473, 5160, 'Salsacate', 6),
(474, 5170, 'Colonia Tirolesa', 6),
(475, 5106, 'San Agustín', 6),
(476, 5178, 'Villa Quilino', 6),
(477, 5174, 'Villa de Soto', 6),
(478, 5147, 'San Esteban', 6),
(479, 5162, 'La Cumbre', 6),
(480, 5149, 'La Falda', 6),
(481, 5168, 'Cabalango', 6),
(482, 5141, 'Valle Hermoso', 6),
(483, 5164, 'Los Hornillos', 6),
(484, 5160, 'Villa Serranita', 6),
(485, 5170, 'Villa Tulumba', 6),
(486, 5106, 'Capilla del Monte', 6),
(487, 5178, 'Santa Rosa de Río Primero', 6),
(488, 5174, 'Las Calles', 6),
(489, 5147, 'Villa Ciudad de América', 6),
(490, 5162, 'Los Reartes', 6),
(491, 5149, 'Mina Clavero', 6),
(492, 5168, 'Villa Santa Cruz del Lago', 6),
(493, 5141, 'San Marcos Sud', 6),
(494, 5164, 'Villa Santa Rosa', 6),
(495, 5160, 'Villa del Rosario', 6),
(496, 5170, 'Villa Yacanto de Calamuchita', 6),
(497, 5106, 'Agua de Oro', 6),
(498, 5178, 'La Granja', 6),
(499, 5174, 'Villa de María', 6),
(500, 5147, 'San José de la Dormida', 6),
(501, 5162, 'La Paisanita', 6),
(502, 5149, 'Los Cóndores', 6),
(503, 5168, 'La Rancherita', 6),
(504, 5141, 'La Para', 6),
(505, 5164, 'Santa Mónica', 6),
(506, 5160, 'Despeñaderos', 6),
(507, 5170, 'La Serranita', 6),
(508, 5106, 'Colonia Vicente Agüero', 6),
(509, 5178, 'La Serranita', 6),
(510, 5174, 'La Paisanita', 6),
(511, 5147, 'Santa Rosa de Calamuchita', 6),
(512, 5162, 'Tanti Nuevo', 6),
(513, 5149, 'Villa Los Aromos', 6),
(514, 5168, 'Los Cedros', 6),
(515, 5141, 'Anisacate', 6),
(516, 5164, 'San Agustín', 6),
(517, 5160, 'Villa Anizacate', 6),
(518, 5170, 'Villa Parque Siquiman', 6),
(519, 5106, 'La Cumbrecita', 6),
(520, 5178, 'Colonia Tirolesa', 6),
(521, 5174, 'Villa de María', 6),
(522, 5147, 'Bialet Massé', 6),
(523, 5162, 'Salsipuedes', 6),
(524, 5149, 'La Cumbre', 6),
(525, 5168, 'Villa Berna', 6),
(526, 5141, 'Colonia Caroya', 6),
(527, 5164, 'Los Molinos', 6),
(528, 5160, 'La Cautiva', 6),
(529, 5170, 'Villa Los Molinos', 6),
(530, 5106, 'Villa General Belgrano', 6),
(531, 5178, 'El Durazno', 6),
(532, 5174, 'Las Rabonas', 6),
(533, 5147, 'Malagueño', 6),
(534, 5162, 'Villa del Totoral', 6),
(535, 5149, 'Villa del Dique', 6),
(536, 5168, 'Villa Cerro Azul', 6),
(537, 5141, 'Río Segundo', 6),
(538, 5164, 'Villa Tulumba', 6),
(539, 5160, 'Yacanto', 6),
(540, 5170, 'Villa del Prado', 6),
(541, 5106, 'La Falda', 6),
(542, 5178, 'Villa Huidobro', 6),
(543, 5174, 'La Para', 6),
(544, 5147, 'La Puerta', 6),
(545, 5162, 'Río Cuarto', 6),
(546, 5149, 'Villa de Pocho', 6),
(547, 5168, 'Villa de Las Rosas', 6),
(548, 5141, 'Pilar', 6),
(549, 5164, 'Almafuerte', 6),
(550, 5160, 'Tancacha', 6),
(551, 5170, 'Villa Parque Santa Ana', 6),
(552, 5106, 'Villa Santa Rosa', 6),
(553, 5178, 'Los Zorros', 6),
(554, 5174, 'Las Varas', 6),
(555, 5147, 'San Marcos Sud', 6),
(556, 5162, 'La Playa', 6),
(557, 5149, 'Las Acequias', 6),
(558, 5168, 'Capilla de Sitón', 6),
(559, 5141, 'Monte Leña', 6),
(560, 5164, 'Pascanas', 6),
(561, 5160, 'Los Cerrillos', 6),
(562, 5170, 'La Bolsa', 6),
(563, 5106, 'Los Condores', 6),
(564, 5178, 'Ticino', 6),
(565, 5174, 'El Manzano', 6),
(566, 5147, 'Colonia Lola', 6),
(567, 5162, 'San Antonio de Litín', 6),
(568, 5149, 'San José de la Esquina', 6),
(569, 5168, 'Aldea Santa María', 6),
(570, 5141, 'Monte Buey', 6),
(571, 5164, 'Leones', 6),
(572, 5160, 'Villa Ascasubi', 6),
(573, 5170, 'General Cabrera', 6),
(574, 5106, 'Alejo Ledesma', 6),
(575, 5178, 'Etruria', 6),
(576, 5174, 'Pasco', 6),
(577, 5147, 'General Deheza', 6),
(578, 5162, 'Ausonia', 6),
(579, 5149, 'Morrison', 6),
(580, 5168, 'General Levalle', 6),
(581, 5141, 'La Carlota', 6),
(582, 5164, 'San Basilio', 6),
(583, 5160, 'La Playosa', 6),
(584, 5170, 'Berrotarán', 6),
(585, 5106, 'Santa Rosa de Río Primero', 6),
(586, 5178, 'Santa Eufemia', 6),
(587, 5174, 'Obispo Trejo', 6),
(588, 5147, 'Del Campillo', 6),
(589, 5162, 'General Baldissera', 6),
(590, 5149, 'Colonia Marina', 6),
(591, 5168, 'Tío Pujio', 6),
(592, 5141, 'Adelia María', 6),
(593, 5164, 'General Roca', 6),
(594, 5160, 'Los Surgentes', 6),
(595, 5170, 'Villa Amancay', 6),
(596, 5106, 'Río Tercero', 6),
(597, 5178, 'Monte Maíz', 6),
(598, 5174, 'Monte de los Gauchos', 6),
(599, 5147, 'Villa Huidobro', 6),
(600, 5162, 'Arias', 6),
(601, 5149, 'Carnerillo', 6),
(602, 5168, 'Chilibroste', 6),
(603, 5141, 'Huinca Renancó', 6),
(604, 5164, 'Elena', 6),
(605, 5160, 'General Fotheringham', 6),
(606, 5170, 'Buchardo', 6),
(607, 5106, 'Berrotarán', 6),
(608, 5178, 'Melo', 6),
(609, 5174, 'Ucacha', 6),
(610, 5147, 'Mattaldi', 6),
(611, 5162, 'Pueblo Italiano', 6),
(612, 5149, 'Villa Valeria', 6),
(613, 5168, 'Bengolea', 6),
(614, 5141, 'Villa Reducción', 6),
(615, 5164, 'La Cesira', 6),
(616, 5160, 'General Deheza', 6),
(617, 5170, 'Villa Elisa', 6),
(618, 5106, 'General Cabrera', 6),
(619, 5178, 'Los Cisnes', 6),
(620, 5174, 'Corral de Bustos', 6),
(621, 5147, 'Colonia Almada', 6),
(622, 5162, 'La Palestina', 6),
(623, 5149, 'La Carolina', 6),
(624, 5168, 'Elena', 6),
(625, 5141, 'General Levalle', 6),
(626, 5164, 'Los Condores', 6),
(627, 5160, 'Chazón', 6),
(628, 5170, 'Cavanagh', 6),
(629, 5106, 'Pasco', 6),
(630, 5178, 'Catalina', 6),
(631, 5174, 'San Marcos Sud', 6),
(632, 5147, 'La Laguna', 6),
(633, 5162, 'Viamonte', 6),
(634, 5149, 'Los Zorros', 6),
(635, 5168, 'Monte Buey', 6),
(636, 5141, 'Los Condores', 6),
(637, 5164, 'Camilo Aldao', 6),
(638, 5160, 'La Palestina', 6),
(639, 5170, 'Corral de Bustos', 6),
(640, 5106, 'Alejo Ledesma', 6),
(641, 5178, 'Reducción', 6),
(642, 5174, 'La Laguna', 6),
(643, 5147, 'La Playosa', 6),
(644, 5162, 'Washington', 6),
(645, 5149, 'Villa Rossi', 6),
(646, 5168, 'San Basilio', 6),
(647, 5141, 'Bouwer', 6),
(648, 5164, 'Los Surgentes', 6),
(649, 5160, 'Villa María', 6),
(650, 5170, 'Colonia San Bartolomé', 6),
(651, 5106, 'Villa Valeria', 6),
(652, 5178, 'Wenceslao Escalante', 6),
(653, 5174, 'Villa Ascasubi', 6),
(654, 5147, 'Chilibroste', 6),
(655, 5162, 'Villa Los Patos', 6),
(656, 5149, 'Calmayo', 6),
(657, 5168, 'Monte de los Gauchos', 6),
(658, 5141, 'Pueblo Santa María', 6),
(659, 5164, 'Monte Ralo', 6),
(660, 5160, 'Aldea Santa María', 6),
(661, 5170, 'General Roca', 6),
(662, 5106, 'Monte de los Gauchos', 6),
(663, 5178, 'Villa Reducción', 6),
(664, 5174, 'Santa Eufemia', 6),
(665, 5147, 'La Carolina', 6),
(666, 5162, 'Carnerillo', 6),
(667, 5149, 'La Cesira', 6),
(668, 5168, 'General Deheza', 6),
(669, 5141, 'Tosquita', 6),
(670, 5164, 'Bengolea', 6),
(671, 5160, 'General Fotheringham', 6),
(672, 5170, 'Elena', 6),
(673, 5106, 'Villa Huidobro', 6),
(674, 5178, 'La Playa', 6),
(675, 5174, 'La Cañada', 6),
(676, 5147, 'La Puerta', 6),
(677, 5162, 'Monte Leña', 6),
(678, 5149, 'General Deheza', 6),
(679, 5168, 'Washington', 6),
(680, 5141, 'Río Tercero', 6),
(681, 5164, 'Ausonia', 6),
(682, 5160, 'General Roca', 6),
(683, 5170, 'Huinca Renancó', 6),
(684, 5106, 'General Levalle', 6),
(685, 5178, 'General Fotheringham', 6),
(686, 5174, 'Colonia Caroya', 6),
(687, 5147, 'La Cumbrecita', 6),
(688, 5162, 'Las Perdices', 6),
(689, 5149, 'Aldea Santa María', 6),
(690, 5168, 'General Baldissera', 6),
(691, 5141, 'Santa Eufemia', 6),
(692, 5164, 'La Carlota', 6),
(693, 5160, 'Etruria', 6),
(694, 5170, 'Monte Leña', 6),
(695, 5106, 'Corralito', 6),
(696, 5178, 'La Laguna', 6),
(697, 5174, 'Monte Maíz', 6),
(698, 5147, 'Las Junturas', 6),
(699, 5162, 'Río Cuarto', 6),
(700, 5149, 'Villa Huidobro', 6),
(701, 5168, 'Colonia Caroya', 6),
(702, 5141, 'Monte Cristo', 6),
(703, 5164, 'Colonia San Bartolomé', 6),
(704, 5160, 'Los Zorros', 6),
(705, 5170, 'San Antonio de Litín', 6),
(706, 5106, 'Monte Buey', 6),
(707, 5178, 'San Marcos Sud', 6),
(708, 5174, 'Río Segundo', 6),
(709, 5147, 'Santa Rosa de Calamuchita', 6),
(710, 5162, 'Monte Maíz', 6),
(711, 5149, 'Despeñaderos', 6),
(712, 5168, 'Corralito', 6),
(713, 5141, 'La Bolsa', 6),
(714, 5164, 'Ucacha', 6),
(715, 5160, 'General Deheza', 6),
(716, 5170, 'Reducción', 6),
(717, 5106, 'La Carolina', 6),
(718, 5178, 'Wenceslao Escalante', 6),
(719, 5174, 'General Levalle', 6),
(720, 5147, 'Berrotarán', 6),
(721, 5162, 'La Cumbrecita', 6),
(722, 5149, 'Villa Rumipal', 6),
(723, 5168, 'Villa María', 6),
(724, 5141, 'Colonia San Bartolomé', 6),
(725, 5164, 'San Agustín', 6),
(726, 5160, 'Charras', 6),
(727, 5170, 'Almafuerte', 6),
(728, 5106, 'Santa Rosa de Calamuchita', 6),
(729, 5178, 'Chilibroste', 6),
(730, 5174, 'Ausonia', 6),
(731, 5147, 'La Laguna', 6),
(732, 5162, 'Alcira Gigena', 6),
(733, 5149, 'Santa Eufemia', 6),
(734, 5168, 'Río Tercero', 6),
(735, 5141, 'Bialet Massé', 6),
(736, 5164, 'Tancacha', 6),
(737, 5160, 'Pampayasta Sud', 6),
(738, 5170, 'Monte Cristo', 6),
(739, 5106, 'Monte Cristo', 6),
(740, 5178, 'La Francia', 6),
(741, 5174, 'Pueblo Santa María', 6),
(742, 5147, 'Morrison', 6),
(743, 5162, 'La Laguna', 6),
(744, 5149, 'Chilibroste', 6),
(745, 5168, 'Monte Cristo', 6),
(746, 5141, 'Villa del Dique', 6),
(747, 5164, 'Chilibroste', 6),
(748, 5160, 'Despeñaderos', 6),
(749, 5170, 'Aldea Santa María', 6),
(750, 5106, 'Huinca Renancó', 6),
(751, 5178, 'Colonia Vicente Agüero', 6),
(752, 5174, 'Santa Rosa de Calamuchita', 6),
(753, 3100, 'Paraná', 9),
(754, 3200, 'Concordia', 9),
(755, 3150, 'Gualeguaychú', 9),
(756, 3260, 'La Paz', 9),
(757, 2820, 'Colón', 9),
(758, 3190, 'Victoria', 9),
(759, 2828, 'San José', 9),
(760, 3105, 'Diamante', 9),
(761, 3280, 'Villaguay', 9),
(762, 3265, 'Federación', 9),
(763, 2822, 'Pueblo Belgrano', 9),
(764, 3193, 'Rosario del Tala', 9),
(765, 3116, 'Crespo', 9),
(766, 3240, 'Chajarí', 9),
(767, 2824, 'Villa Elisa', 9),
(768, 3218, 'Nogoyá', 9),
(769, 3170, 'Basavilbaso', 9),
(770, 2826, 'Ubajay', 9),
(771, 3203, 'Santa Elena', 9),
(772, 3196, 'Maciá', 9),
(773, 2828, 'Concepción del Uruguay', 9),
(774, 3197, 'Federal', 9),
(775, 2828, 'Villa Paranacito', 9),
(776, 3180, 'Hasenkamp', 9),
(777, 2824, 'San Salvador', 9),
(778, 2822, 'Gualeguay', 9),
(779, 3194, 'Oro Verde', 9),
(780, 2820, 'Santa Ana', 9),
(781, 3201, 'San Benito', 9),
(782, 2824, 'Villa Mantero', 9),
(783, 2826, 'General Ramírez', 9),
(784, 3206, 'Hernandarias', 9),
(785, 2826, 'Paraje Las Tunas', 9),
(786, 2824, 'Colonia Elía', 9),
(787, 2822, 'Aldea San Antonio', 9),
(788, 2820, 'Tabossi', 9),
(789, 2822, 'Conscripto Bernardi', 9),
(790, 3177, 'Villa Clara', 9),
(791, 2822, 'Concordia', 9),
(792, 3195, 'Aldea Brasilera', 9),
(793, 2828, 'Conscripto Bernardi', 9),
(794, 3198, 'Aldea Protestante', 9),
(795, 2824, 'Aldea San Antonio', 9),
(796, 3114, 'General Campos', 9),
(797, 2820, 'Villa Elisa', 9),
(798, 2828, 'Colonia Elía', 9),
(799, 2822, 'Villa Clara', 9),
(800, 2826, 'El Brillante', 9),
(801, 2824, 'San Marcial', 9),
(802, 2822, 'Estación Yeruá', 9),
(803, 2820, 'Villa San Marcial', 9),
(804, 2828, 'Colonia Crespo', 9),
(805, 2824, 'Concepción del Uruguay', 9),
(806, 2822, 'Sauce de Luna', 9),
(807, 2826, 'Pueblo General Belgrano', 9),
(808, 2822, 'Piedras Blancas', 9),
(809, 2820, 'Colonia General Roca', 9),
(810, 2824, 'General Ramírez', 9),
(811, 2826, 'Colonia Hughes', 9),
(812, 2820, 'Bovril', 9),
(813, 2828, 'San Justo', 9),
(814, 2822, 'Arroyo Barú', 9),
(815, 2824, 'Villa Domínguez', 9),
(816, 2826, 'Santa Anita', 9),
(817, 2820, 'Villa San Justo', 9),
(818, 2828, 'Cerrito', 9),
(819, 2822, 'Paraje Las Moscas', 9),
(820, 2824, 'La Criolla', 9),
(821, 2826, 'Sauce Montrull', 9),
(822, 2820, 'General Galarza', 9),
(823, 2828, 'Strobel', 9),
(824, 2822, 'Villa Clara', 9),
(825, 2824, 'Villa Mantero', 9),
(826, 2826, 'Pueblo Brugo', 9),
(827, 2820, 'Villa Elisa', 9),
(828, 2828, 'La Clarita', 9),
(829, 2822, 'Paraje La Esmeralda', 9),
(830, 2824, 'Estación Sosa', 9),
(831, 2826, 'Gobernador Etchevehere', 9),
(832, 2820, 'San Miguel', 9),
(833, 2828, 'El Cimarrón', 9),
(834, 2822, 'Arroyo Cle', 9),
(835, 2824, 'Paraje El Brillante', 9),
(836, 2826, 'Paraje Ñancay', 9),
(837, 2820, 'Paraje Sauce de Luna', 9),
(838, 2828, 'Paraje Aldea Santa Rosa', 9),
(839, 2822, 'Los Charrúas', 9),
(840, 2824, 'Arroyo del Medio', 9),
(841, 2826, 'Sauce Pinto', 9),
(842, 2820, 'Paraje Talitas', 9),
(843, 2828, 'Paraje Calabacillas', 9),
(844, 2822, 'Villa Domínguez', 9),
(845, 2824, 'Villa Mantero', 9),
(846, 2826, 'Mojones Norte', 9),
(847, 2820, 'Estación Camps', 9),
(848, 2828, 'Colonia Avellaneda', 9),
(849, 2822, 'Costa Grande', 9),
(850, 2824, 'Las Tunas', 9),
(851, 2826, 'Herrera', 9),
(852, 2820, 'Pueblo Bellocq', 9),
(853, 2828, 'Villa Alarcón', 9),
(854, 2822, 'Las Tunas', 9),
(855, 2824, 'Estación Raíces', 9),
(856, 2826, 'Costa Grande', 9),
(857, 2820, 'Estación Lazo', 9),
(858, 2828, 'Villa Urquiza', 9),
(859, 2822, 'Estación Escriña', 9),
(860, 2824, 'San Anselmo', 9),
(861, 2826, 'San Marcial', 9),
(862, 2820, 'Aldea San Rafael', 9),
(863, 2828, 'Estación Racedo', 9),
(864, 2822, 'Piedras Blancas', 9),
(865, 2824, 'Paraje Talitas', 9),
(866, 2826, 'La Querencia', 9),
(867, 2820, 'Colonia Ensayo', 9),
(868, 2828, 'Colonia Hocker', 9),
(869, 2822, 'Estación Yeruá', 9),
(870, 5700, 'San Luis', 19),
(871, 5730, 'Villa Mercedes', 19),
(872, 5881, 'Merlo', 19),
(873, 5711, 'La Punta', 19),
(874, 5701, 'Juana Koslay', 19),
(875, 5885, 'Quines', 19),
(876, 5883, 'Candelaria', 19),
(877, 5887, 'La Toma', 19),
(878, 5889, 'Tilisarao', 19),
(879, 5887, 'Nueva Galia', 19),
(880, 5700, 'Justo Daract', 19),
(881, 5701, 'Santa Rosa del Conlara', 19),
(882, 5885, 'Concarán', 19),
(883, 5887, 'Carpintería', 19),
(884, 5700, 'Luján', 19),
(885, 5881, 'San Francisco del Monte de Oro', 19),
(886, 5701, 'Unión', 19),
(887, 5700, 'El Volcán', 19),
(888, 5881, 'Villa de Merlo', 19),
(889, 5701, 'Potrero de los Funes', 19),
(890, 5883, 'El Trapiche', 19),
(891, 5881, 'Balde', 19),
(892, 5701, 'La Carolina', 19),
(893, 5883, 'Cortaderas', 19),
(894, 5881, 'Zanjitas', 19),
(895, 5889, 'Naschel', 19),
(896, 5887, 'Los Molles', 19),
(897, 5701, 'San Martín', 19),
(898, 5887, 'Buena Esperanza', 19),
(899, 5885, 'Villa Larca', 19),
(900, 5881, 'Renca', 19),
(901, 5887, 'La Calera', 19),
(902, 5700, 'Desaguadero', 19),
(903, 5885, 'Lafinur', 19),
(904, 5700, 'El Durazno', 19),
(905, 5883, 'Los Cajones', 19),
(906, 5889, 'San Pablo', 19),
(907, 5881, 'El Rincón', 19),
(908, 5887, 'Villa del Carmen', 19),
(909, 5883, 'San Jerónimo', 19),
(910, 5885, 'Las Chacras', 19),
(911, 5889, 'Navia', 19),
(912, 5701, 'Cruz de Caña', 19),
(913, 5887, 'La Botija', 19),
(914, 5883, 'Las Barranquitas', 19),
(915, 5700, 'La Florida', 19),
(916, 5889, 'Los Molles', 19),
(917, 5881, 'La Ramada', 19),
(918, 5885, 'Las Palomas', 19),
(919, 5887, 'Las Aguadas', 19),
(920, 2000, 'Rosario', 21),
(921, 3000, 'Santa Fe', 21),
(922, 2132, 'Villa Gobernador Gálvez', 21),
(923, 3001, 'Reconquista', 21),
(924, 2001, 'San Lorenzo', 21),
(925, 2100, 'Venado Tuerto', 21),
(926, 2132, 'Granadero Baigorria', 21),
(927, 3000, 'Rafaela', 21),
(928, 2132, 'Funes', 21),
(929, 2132, 'Santo Tomé', 21),
(930, 2132, 'Esperanza', 21),
(931, 2132, 'Rosario Norte', 21),
(932, 2132, 'San Justo', 21),
(933, 2000, 'Capitán Bermúdez', 21),
(934, 2132, 'Villa Constitución', 21),
(935, 2132, 'Casilda', 21),
(936, 3001, 'Arroyo Seco', 21),
(937, 2001, 'Gálvez', 21),
(938, 2100, 'Pérez', 21),
(939, 2132, 'Roldán', 21),
(940, 2132, 'San Jorge', 21),
(941, 2132, 'Santa Fe Norte', 21),
(942, 3000, 'Firmat', 21),
(943, 2132, 'Carcarana', 21),
(944, 2132, 'Acebal', 21),
(945, 2000, 'Villa Constitución', 21),
(946, 2132, 'San Carlos Centro', 21),
(947, 2132, 'Coronda', 21),
(948, 2132, 'Las Parejas', 21),
(949, 2001, 'Villa Ocampo', 21),
(950, 2100, 'Casilda', 21),
(951, 2132, 'Las Rosas', 21),
(952, 2132, 'San Lorenzo Norte', 21),
(953, 2132, 'Fighiera', 21),
(954, 2000, 'Esperanza', 21),
(955, 2132, 'Gálvez', 21),
(956, 2132, 'Sunchales', 21),
(957, 3001, 'Villa Eloísa', 21),
(958, 2001, 'Villa Gobernador Gálvez', 21),
(959, 2100, 'San Jorge', 21),
(960, 2132, 'Fray Luis Beltrán', 21),
(961, 2132, 'San Javier', 21),
(962, 2132, 'Sunchales', 21),
(963, 2132, 'Las Toscas', 21),
(964, 3000, 'Santa Fe Sur', 21),
(965, 2132, 'Villa Cañás', 21),
(966, 2132, 'Humboldt', 21),
(967, 2132, 'San Cristóbal', 21),
(968, 2001, 'San Justo', 21),
(969, 2100, 'Esperanza', 21),
(970, 2132, 'Fighiera', 21),
(971, 2132, 'San José del Rincón', 21),
(972, 2132, 'Santa Fe Oeste', 21),
(973, 1757, 'Gregorio de Laferrere', 1),
(974, 5500, 'Mendoza', 13);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

DROP TABLE IF EXISTS `marca`;
CREATE TABLE IF NOT EXISTS `marca` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_marca_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `marca`
--

INSERT INTO `marca` (`id`, `nombre`) VALUES
(4, 'Dexin'),
(6, 'Hewlett Packard'),
(2, 'IA Electrónica'),
(1, 'Liecom'),
(0, 'N/D'),
(7, 'TeamCast'),
(5, 'Ubiquiti'),
(3, 'VideoSwitch');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

DROP TABLE IF EXISTS `modelo`;
CREATE TABLE IF NOT EXISTS `modelo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marca_id` int(11) DEFAULT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(250) DEFAULT NULL,
  `image_file` varchar(50) NOT NULL DEFAULT 'default_eq.png',
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `anio` varchar(4) DEFAULT NULL,
  `homologacion_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_modelo_nombre_anio` (`nombre`,`anio`),
  KEY `modelo_homologacion` (`homologacion_id`),
  KEY `modelo_marca` (`marca_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `modelo`
--

INSERT INTO `modelo` (`id`, `marca_id`, `nombre`, `descripcion`, `image_file`, `date_created`, `date_modified`, `anio`, `homologacion_id`) VALUES
(0, 0, 'N/D', 'Modelo no específico', 'default_eq.png', '2023-07-06 10:45:57', '2023-07-06 10:45:57', 'N/D', NULL),
(1, 2, 'FM100', 'STM', '9b0a1133e8efc0ad-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-09 12:55:38', '\'17', 2),
(2, 2, 'FM250', 'STM', '00a0d44c7702e1a5-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'16', 3),
(3, 1, 'FM500', 'STM', 'd54af0ea5584e2ef-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'19', 4),
(4, 1, 'FM1000', 'CTM', '4d36499baa010264-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-07 10:54:26', '\'23', 5),
(5, 1, 'FM2000', 'STM', 'b67f8b1f6f96a97e-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'23', 6),
(6, 1, 'FM3000', 'CTM', 'b3de7d3f5614eda7-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'23', NULL),
(8, 1, 'FM7000', 'refrigeración Agua', 'a40c30b94d9b1ee9-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'14', NULL),
(10, 1, 'FM5000', 'rack CTM', '4883a88e4aa7c4ef-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'23', 7),
(11, 1, 'TRUD70', 'STM', '0d0fb90ce98ad382-removebg-preview.png', '2023-06-30 10:17:39', '2023-06-30 10:17:39', '\'20', NULL),
(13, 1, 'TRUD250', 'STM', 'a865c54b13d4b420-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-10 16:36:01', '\'20', 9),
(15, 1, 'TRUD500', 'CTM', 'ac25db2c48c2802b-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-04 10:47:31', '\'21', 10),
(19, 1, 'TRUD1200', 'CTM', 'b551d0cb2c616c88-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-04 10:55:33', '\'10', 11),
(20, 1, 'TRUD1800', 'CTM', 'e7f3f00e4feb84d3-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-04 10:56:48', '\'22', NULL),
(22, 1, 'TRV5000', 'CTM', 'ac43080af69e7ac5.JPG', '2023-06-30 10:17:39', '2023-07-04 11:22:04', '\'10', NULL),
(23, 1, 'TRU250', 'CTM', 'b826b5271375f5bb.jpg', '2023-06-30 10:17:39', '2023-07-04 11:14:24', '\'06', NULL),
(25, 1, 'TRU400', 'CTM', '2b82d39020339dce-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-04 11:11:20', '\'08', NULL),
(26, 1, 'TRU500', 'CTM', 'a42b1c7599f290cf-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-04 11:12:53', '\'19', NULL),
(30, 1, 'TRM2650', 'CTM', '7c7c38654f7e1563.jpg', '2023-06-30 10:17:39', '2023-07-04 10:23:40', '\'23', NULL),
(31, 1, 'TRM26100', 'CTM', '6a75e05653aa3660-removebg-preview.png', '2023-06-30 10:17:39', '2023-07-04 10:22:48', '\'16', NULL),
(32, 4, 'NDS3542', 'HDMI', 'b7da03f8bccd689d.png', '2023-06-30 10:17:39', '2023-07-04 10:38:38', '\'16', NULL),
(33, 4, 'NDS3542A', 'SDI', '47c3e06c73d0fbd7.png', '2023-06-30 10:17:39', '2023-07-04 10:38:13', '\'17', NULL),
(34, 3, 'DMOD-1000', '', '983d6e0b7a8cf0e9.png', '2023-06-30 10:17:39', '2023-07-12 12:14:28', '\'20', NULL),
(36, 3, 'DMUX-500i', '', '64261f290660c662.png', '2023-06-30 10:17:39', '2023-07-09 12:18:29', '\'19', NULL),
(37, 3, 'DMUX-3100', '', 'c62ba952cffab5c6.png', '2023-06-30 10:17:39', '2023-07-09 12:18:18', '\'20', NULL),
(38, 4, 'LP211', 'CTM', 'a3bd839633bbd039.png', '2023-06-30 10:17:39', '2023-07-04 10:28:56', '\'18', NULL),
(40, 2, 'FM100', 'enc. posterior', '2e02a8e0c60f655d-removebg-preview.png', '2023-06-30 12:39:07', '2023-07-09 12:18:53', '\'23', 2),
(46, 1, 'TRV100', 'STM', '73ca8466b7df3f00-removebg-preview.png', '2023-07-04 10:22:36', '2023-07-04 10:22:36', '\'08', 12),
(47, 2, 'FM50', '', 'default_eq.png', '2023-07-04 13:21:30', '2023-07-04 13:21:30', '\'22', 1),
(48, 0, 'Router', '', '7a1a80f2c44bcceb.png', '2023-07-07 12:16:00', '2023-07-07 12:16:00', 'N/D', NULL),
(49, 0, 'Switch', '', 'a1c2e38a214e88e7.png', '2023-07-07 12:16:19', '2023-07-07 12:16:19', 'N/D', NULL),
(50, 0, 'Enlace', 'banda 5GHz', '5410c5fdf8749071.png', '2023-07-07 12:16:19', '2023-07-07 12:16:19', 'N/D', NULL),
(51, 1, 'FM10.000', '', '612c081fc0fc7d85.jpg', '2023-07-10 11:01:51', '2023-07-10 11:03:13', '\'18', 8),
(52, 2, 'FM250', '', '3481b256c88d0518.jpg', '2023-07-14 15:35:14', '2023-07-14 15:35:14', '\'23', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden_reparacion`
--

DROP TABLE IF EXISTS `orden_reparacion`;
CREATE TABLE IF NOT EXISTS `orden_reparacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codigo` varchar(50) NOT NULL,
  `content` varchar(250) NOT NULL,
  `tecnico_id` int(11) DEFAULT NULL,
  `equipo_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `estado_id` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `user_id` (`user_id`),
  KEY `equipment_id` (`equipo_id`),
  KEY `or_estado` (`estado_id`),
  KEY `or_tecnico` (`tecnico_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `orden_reparacion`
--

INSERT INTO `orden_reparacion` (`id`, `date_created`, `date_modified`, `codigo`, `content`, `tecnico_id`, `equipo_id`, `user_id`, `estado_id`) VALUES
(2, '2023-06-13 12:20:25', '2023-07-13 23:18:56', '230327', 'Reparar ventiladores', 14, 10, 10, 2),
(6, '2023-06-13 12:41:08', '2023-07-13 23:17:04', '210615', 'Revisar el equipo, presenta falla RF.', 14, 3, 10, 2),
(9, '2023-06-14 11:59:34', '2023-07-13 23:20:05', '220516', 'Se envió el módulo de potencia porque no enciende', 5, 13, 10, 2),
(12, '2023-06-14 12:28:20', '2023-07-13 23:20:18', '230314', 'Pedido de reparación por falla de temperatura', 14, 1, 10, 2),
(13, '2023-06-16 11:48:15', '2023-06-16 13:24:56', '230422', 'Cambiar de frecuencia a 107,1MHz', 14, 17, 10, 3),
(14, '2023-06-16 12:14:01', '2023-07-07 11:07:21', '230516', 'cambiar base de tiempo a GPS integrado', 5, 34, 10, 2),
(15, '2023-06-16 12:33:40', '2023-07-13 23:17:42', '230315', 'revisar configuracion', 6, 34, 10, 2),
(17, '2023-06-17 16:02:08', '2023-06-17 16:20:02', '193454', 'cambiar de frec a 98,5MHz', 1, 2, 10, 4),
(18, '2023-06-17 16:02:08', '2023-07-13 23:19:14', '213454', 'problemas entrada 220V', 1, 3, 10, 2),
(19, '2023-06-17 16:02:08', '2023-07-13 23:18:15', '230504', 'cambiar modulacion: \r\nIG: 1/32\r\nContelacion=64QAM', 5, 33, 10, 2),
(20, '2023-07-11 12:22:42', '2023-07-11 13:25:39', '230711', 'revisar alimentación', 6, 92, 10, 2),
(21, '2023-07-12 09:29:31', '2023-07-12 09:39:22', '230712', 'Falla >>ROE revisar', 14, 20, 12, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pais`
--

DROP TABLE IF EXISTS `pais`;
CREATE TABLE IF NOT EXISTS `pais` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `pais`
--

INSERT INTO `pais` (`id`, `nombre`) VALUES
(1, 'Argentina'),
(2, 'Bolivia'),
(3, 'Brasil'),
(4, 'Chile'),
(5, 'Colombia'),
(6, 'Costa Rica'),
(7, 'Cuba'),
(8, 'Ecuador'),
(9, 'El Salvador'),
(10, 'Guatemala'),
(11, 'Honduras'),
(12, 'México'),
(13, 'Nicaragua'),
(14, 'Panamá'),
(15, 'Paraguay'),
(16, 'Perú'),
(17, 'Puerto Rico'),
(18, 'República Dominicana'),
(19, 'Uruguay'),
(20, 'Venezuela'),
(21, 'Otro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `provincia`
--

DROP TABLE IF EXISTS `provincia`;
CREATE TABLE IF NOT EXISTS `provincia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `pais_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prov_pais` (`pais_id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `provincia`
--

INSERT INTO `provincia` (`id`, `nombre`, `pais_id`) VALUES
(1, 'Buenos Aires', 1),
(2, 'CABA', 1),
(3, 'Catamarca', 1),
(4, 'Chaco', 1),
(5, 'Chubut', 1),
(6, 'Córdoba', 1),
(7, 'Corrientes', 1),
(8, 'Formosa', 1),
(9, 'Entre Ríos', 1),
(10, 'Jujuy', 1),
(11, 'La Pampa', 1),
(12, 'La Rioja', 1),
(13, 'Mendoza', 1),
(14, 'Misiones', 1),
(15, 'Neuquén', 1),
(16, 'Río Negro', 1),
(17, 'Salta', 1),
(18, 'San Juan', 1),
(19, 'San Luis', 1),
(20, 'Santa Cruz', 1),
(21, 'Santa Fe', 1),
(22, 'Santiago del Estero', 1),
(23, 'Tierra del Fuego', 1),
(24, 'Tucumán', 1),
(25, 'Artigas', 19),
(26, 'Canelones', 19),
(27, 'Cerro Largo', 19),
(28, 'Colonia', 19),
(29, 'Durazno', 19),
(30, 'Flores', 19),
(31, 'Florida', 19),
(32, 'Lavalleja', 19),
(33, 'Maldonado', 19),
(34, 'Montevideo', 19),
(35, 'Paysandú', 19),
(36, 'Río Negro', 19),
(37, 'Rivera', 19),
(38, 'Rocha', 19),
(39, 'Salto', 19),
(40, 'San José', 19),
(41, 'Soriano', 19),
(42, 'Tacuarembó', 19),
(43, 'Treinta y Tres', 19),
(44, 'Chuquisaca', 2),
(45, 'La Paz', 2),
(46, 'Cochabamba', 2),
(47, 'Oruro', 2),
(48, 'Potosí', 2),
(49, 'Tarija', 2),
(50, 'Santa Cruz', 2),
(51, 'Beni', 2),
(52, 'Pando', 2),
(53, 'Acre', 3),
(54, 'Alagoas', 3),
(55, 'Amapá', 3),
(56, 'Amazonas', 3),
(57, 'Bahía', 3),
(58, 'Ceará', 3),
(59, 'Distrito Federal', 3),
(60, 'Espírito Santo', 3),
(61, 'Goiás', 3),
(62, 'Maranhão', 3),
(63, 'Mato Grosso', 3),
(64, 'Mato Grosso do Sul', 3),
(65, 'Minas Gerais', 3),
(66, 'Pará', 3),
(67, 'Paraíba', 3),
(68, 'Paraná', 3),
(69, 'Pernambuco', 3),
(70, 'Piauí', 3),
(71, 'Rio de Janeiro', 3),
(72, 'Rio Grande do Norte', 3),
(73, 'Rio Grande do Sul', 3),
(74, 'Rondônia', 3),
(75, 'Roraima', 3),
(76, 'Santa Catarina', 3),
(77, 'São Paulo', 3),
(78, 'Sergipe', 3),
(79, 'Tocantins', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `id` int(11) NOT NULL,
  `role_name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `role`
--

INSERT INTO `role` (`id`, `role_name`) VALUES
(1, 'Admin'),
(2, 'Invitado'),
(3, 'Técnico'),
(4, 'ServicioCliente'),
(5, 'Comercial');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipologia`
--

DROP TABLE IF EXISTS `tipologia`;
CREATE TABLE IF NOT EXISTS `tipologia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tipo` (`tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `tipologia`
--

INSERT INTO `tipologia` (`id`, `tipo`) VALUES
(1, 'Mensaje'),
(3, 'Modificación'),
(2, 'Reparación');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unidad`
--

DROP TABLE IF EXISTS `unidad`;
CREATE TABLE IF NOT EXISTS `unidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `unidad`
--

INSERT INTO `unidad` (`id`, `nombre`) VALUES
(3, 'GHz'),
(1, 'KHz'),
(2, 'MHz'),
(5, 'Uhf'),
(6, 'Un.'),
(4, 'Vhf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `image_file` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL DEFAULT '2',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `password` (`password`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `image_file`, `password`, `role_id`) VALUES
(1, 'Turko', 'arnaizagustin@gmail.com', '18789144792542e0.jpg', '$2b$12$2aL8KrZk6zd4NTk0Hr0UneVLOcQHuZBSLYrRORuElTZOklrI6kw9a', 3),
(4, 'Alejandro', 'toparuiz@mail.com', '51a1e8e115f3c97c.jpg', '$2b$12$VrhQjceSifK79HNg0smr2uidZRnklPL3tFbI54TevRvg2LJ8DkMWu', 1),
(5, 'Atilio', 'atilioavanzini@mail.com', 'f830c0210df9532a.png', '$2b$12$.9g0xMzY6Ov8CEmsuvG5secn12KAfy/JPpffzeYddw81tE.KBg3sy', 3),
(6, 'Oscar', 'oscar@mail.com', '78fcd03e420ea343.jpg', '$2b$12$2BYblyKU0bxi7P4SVglbVe6UamACecyb5nfsmsa5nEzNvtNlIteIK', 3),
(10, 'admin', 'admin@tecseg.com', 'ba7f10cd2f0cb49a.jpg', '$2b$12$dIxpjyQ/uTr8Z7owkfrZKuNoQ5oF4moJHeJgBwjO2X65gmCW.YEWO', 1),
(11, 'Tomas', 'tomas@tecseg.com', 'c1ed20648c2746a0.jpg', '$2b$12$nFwkmd5n6bdgmyroTvpjlehN15JEavOoNpEP/R1DXpAx09GjTJNc6', 5),
(12, 'Juan', 'juan@tecseg.com', 'ee259c124c31059d.jpg', '$2b$12$K2jwJpDeVQyYm0P5iQlGougGR5wG7E.XUb5GadmJEt3PlvijZXRM.', 4),
(14, 'Jorge', 'jorge@tecseg.com', '0cf2ffbae3b4a383.jpg', '$2b$12$8fFUwOfpjV.eHRy11awAjexyJ/kFyryGpGNCL2Eg82xZxNSpeRW3e', 3),
(16, 'Salvador', 'salvi@tecseg.com', '547deb8a3e4608eb.jpg', '$2b$12$JtiK1H.DH4Wnk.hFcn8RseHdBpmNko46NvvwtA/ell9x6BDD9oAkG', 2);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `client_domicilio` FOREIGN KEY (`domicilio_id`) REFERENCES `domicilio` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `client_fiscal` FOREIGN KEY (`cond_fiscal_id`) REFERENCES `cond_fiscal` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `client_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalle_reparacion`
--
ALTER TABLE `detalle_reparacion`
  ADD CONSTRAINT `orden_detalle` FOREIGN KEY (`reparacion_id`) REFERENCES `orden_reparacion` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_detalle` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `domicilio`
--
ALTER TABLE `domicilio`
  ADD CONSTRAINT `domicilio_localidad` FOREIGN KEY (`localidad_id`) REFERENCES `localidad` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `equipment`
--
ALTER TABLE `equipment`
  ADD CONSTRAINT `eq_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `eq_frec` FOREIGN KEY (`frecuencia_id`) REFERENCES `frecuencia` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `eq_modelo` FOREIGN KEY (`modelo_id`) REFERENCES `modelo` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `eq_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `frecuencia`
--
ALTER TABLE `frecuencia`
  ADD CONSTRAINT `frec_unidad` FOREIGN KEY (`unidad_id`) REFERENCES `unidad` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `historia`
--
ALTER TABLE `historia`
  ADD CONSTRAINT `historia_equipo` FOREIGN KEY (`equipo_id`) REFERENCES `equipment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `historia_tipo` FOREIGN KEY (`tipologia_id`) REFERENCES `tipologia` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `historia_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `localidad`
--
ALTER TABLE `localidad`
  ADD CONSTRAINT `localidad_prov` FOREIGN KEY (`provincia_id`) REFERENCES `provincia` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `modelo_homologacion` FOREIGN KEY (`homologacion_id`) REFERENCES `homologacion` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `modelo_marca` FOREIGN KEY (`marca_id`) REFERENCES `marca` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `orden_reparacion`
--
ALTER TABLE `orden_reparacion`
  ADD CONSTRAINT `or_equipo` FOREIGN KEY (`equipo_id`) REFERENCES `equipment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `or_estado` FOREIGN KEY (`estado_id`) REFERENCES `estado_or` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `or_tecnico` FOREIGN KEY (`tecnico_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `or_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `provincia`
--
ALTER TABLE `provincia`
  ADD CONSTRAINT `prov_pais` FOREIGN KEY (`pais_id`) REFERENCES `pais` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
