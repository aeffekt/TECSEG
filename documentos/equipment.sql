-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 21-11-2023 a las 19:38:49
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
-- Estructura de tabla para la tabla `equipment`
--

DROP TABLE IF EXISTS `equipment`;
CREATE TABLE IF NOT EXISTS `equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numSerie` varchar(11) DEFAULT NULL,
  `anio` varchar(4) DEFAULT NULL,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(1000) DEFAULT NULL,
  `caratula_file` varchar(50) DEFAULT NULL,
  `etiqueta_file` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `modelo_id` int(11) NOT NULL,
  `frecuencia_id` int(11) DEFAULT NULL,
  `detalle_trabajo_id` int(11) NOT NULL,
  `sistema` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `equipment_modelo` (`modelo_id`),
  KEY `equipment_canal_frecuencia` (`frecuencia_id`),
  KEY `eq_detalle` (`detalle_trabajo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `equipment`
--

INSERT INTO `equipment` (`id`, `numSerie`, `anio`, `date_created`, `date_modified`, `content`, `caratula_file`, `etiqueta_file`, `user_id`, `modelo_id`, `frecuencia_id`, `detalle_trabajo_id`, `sistema`) VALUES
(95, '3/1122', '2023', '2023-10-20 19:08:32', '2023-11-21 12:58:05', 'IP: 10.0.0.85 ', NULL, NULL, 1, 10, NULL, 14, 'Paraná'),
(96, NULL, '2022', '2023-10-20 22:51:31', '2023-11-21 12:48:32', 'IP: 10.0.0.96', NULL, NULL, 1, 34, NULL, 13, 'Paraná'),
(99, NULL, '2022', '2023-10-20 22:51:31', '2023-11-21 12:47:20', 'IP: 10.0.0.95', NULL, NULL, 1, 69, NULL, 10, 'Paraná'),
(100, NULL, '2022', '2023-10-20 22:51:31', '2023-11-21 12:47:47', 'IP: 10.0.0.94', NULL, NULL, 1, 69, NULL, 10, 'Crespo'),
(101, NULL, '2022', '2023-10-20 22:51:31', '2023-11-21 12:52:21', 'IP: 10.0.0.90\r\nsalida IP\r\nMultiplex vs entrada IP: 224.2.2.2 port 2234. IP : 10.0.0.88', NULL, NULL, 1, 37, 18, 9, 'Crespo'),
(102, NULL, '2020', '2023-10-20 22:51:31', '2023-11-21 12:49:42', '(solo #1 a 9Mb + 2 FM 1M5 c/u) \r\nIP: 10.0.0.89', NULL, NULL, 1, 58, NULL, 8, 'Estudios'),
(106, '4/1122', '2022', '2023-10-21 00:19:20', '2023-11-21 12:48:10', 'IP: 192.168.1.90(?) or 192.168.1.210', NULL, NULL, 1, 56, 18, 11, 'Crespo'),
(108, '1/1221', '2021', '2023-10-22 11:33:10', '2023-10-23 10:39:19', 'Potencia de salida RMS 150W', NULL, NULL, 1, 13, 29, 16, NULL),
(109, NULL, '2020', '2023-10-22 11:33:10', '2023-10-23 10:39:43', 'tiene 2 señales 7,5Mb.. quiere agregar 3er señal\r\nla señal viaja via fibra SDI 4 pelos convierte a HDMI', NULL, NULL, 1, 58, 29, 17, NULL),
(110, '3/1221', '2021', '2023-10-22 14:53:12', '2023-10-26 11:58:07', 'TRUD1000 CTM instalada\r\nIP: 10.6.0.205', NULL, NULL, 1, 19, 21, 24, NULL),
(111, NULL, '2020', '2023-10-22 14:53:12', '2023-10-26 11:58:26', '10.6.0.201	NIT= 21.1 	BTS-MFN', NULL, NULL, 1, 61, 21, 23, NULL),
(112, NULL, '2022', '2023-10-22 14:53:12', '2023-10-26 11:58:47', 'IP: 10.6.0.202	\r\ncapa A 13 seg\r\n64QAM \r\n5/6 \r\n1/16\r\ningresa IP multicast 224.2.2.2 puerto 12000', NULL, NULL, 1, 36, 21, 22, NULL),
(113, NULL, '2020', '2023-10-22 14:53:12', '2023-10-27 11:54:42', 'MASTER 	\r\n192.168.0.20 \r\nuser:ubnt \r\npass:ubnt	\r\nnombre de link: JTA24G \r\npassword: jesusteama', NULL, NULL, 1, 59, NULL, 21, NULL),
(114, NULL, '2020', '2023-10-22 14:53:12', '2023-10-27 12:04:30', 'SLAVE	\r\n192.168.0.21 \r\nuser: ubnt \r\npass: ubnt	\r\nnombre de link: JTA24G \r\npassword: jesusteama', NULL, NULL, 1, 59, NULL, 21, NULL),
(115, NULL, '2020', '2023-10-22 14:53:12', '2023-10-22 15:42:31', 'ARUBA 1930\r\nIP 192.168.1.1', NULL, NULL, 1, 49, NULL, 20, NULL),
(116, NULL, '2020', '2023-10-22 14:53:12', '2023-10-22 15:42:06', 'ARUBA 1930', NULL, NULL, 1, 49, NULL, 20, NULL),
(117, NULL, '2021', '2023-10-22 14:53:12', '2023-11-19 12:46:34', 'IP: 172.20.3.130\r\n8 entradas HDMI\r\n#1 8MBps \"JTA TV\" high profile 1920x1080\r\n#3 8MBps \"JTA DEPORTES\" high profile 1920x1080\r\nSalida IP 224.2.2.2 12000 hasta 12008', NULL, NULL, 1, 60, NULL, 19, NULL),
(118, NULL, '2021', '2023-10-22 15:40:14', '2023-11-21 00:33:08', '192.168.0.30 	nombre=\"JTA TV\" \r\nbitrate= 8M ENtrada HDMI \r\nIP OUT 224.2.2.2 puerto 12.000', NULL, NULL, 1, 38, NULL, 18, NULL),
(119, '2/1122', '2020', '2023-10-23 10:21:21', '2023-11-21 13:01:52', '10.0.0.86\r\ninstalado en CRESPO. \r\nEn primer lugar fue a préstamo un TRUD500', '220516-2_1122_caratula.pdf', '220516-2_1122.pdf', 1, 20, 18, 12, 'Crespo'),
(121, '2/1218', '2018', '2023-10-23 11:39:42', '2023-11-13 18:05:35', '', NULL, NULL, 1, 55, 31, 29, NULL),
(122, NULL, '2018', '2023-10-23 11:39:42', '2023-10-23 11:39:42', '192.168.0.40', NULL, NULL, 1, 37, 31, 28, NULL),
(123, NULL, '2018', '2023-10-23 11:39:42', '2023-10-26 12:00:27', ' 192.168.0.136\r\nusa conversor hdmi, no funciona SDI\r\nLo usa de BACKUP', NULL, NULL, 1, 58, 31, 27, NULL),
(124, '1/1218', '2018', '2023-10-23 11:39:42', '2023-10-26 15:32:01', '', NULL, NULL, 1, 13, 31, 25, NULL),
(125, NULL, '2018', '2023-10-23 11:39:42', '2023-10-23 11:39:42', 'HDMI sin webbrower usar SNMP 192.168.0.30', NULL, NULL, 1, 38, NULL, 26, NULL),
(126, '1/1023', '2023', '2023-10-25 12:53:33', '2023-10-25 12:53:33', 'sin pre corrección', NULL, NULL, 1, 15, 19, 33, NULL),
(127, NULL, '2023', '2023-10-25 12:53:33', '2023-10-25 12:53:33', 'IP 192.168.1.136\r\nchannel #1 GUANACO PLAY 9M\r\nchannel #3 CHINGUI CHINGUI 4M5\r\nchannel #4 DYNAMIS TV 4M5\r\n\r\nRF OUT -5dBm 64qam 1/32 7/8', NULL, NULL, 1, 58, 19, 32, NULL),
(128, '1/0322', '2022', '2023-10-25 13:05:56', '2023-10-25 13:16:08', '', NULL, NULL, 1, 13, 16, 35, NULL),
(129, NULL, '2022', '2023-10-25 13:05:56', '2023-10-26 09:09:09', 'IP: 192.168.1.136\r\n16QAM modo3 conv 5/6 IG: 1/16\r\n#1 señal 9 MBps \"FIVE TV\"\r\n#2 señal 3,5 MBps \"TV Channel\"\r\nMPEG2 audio, para mejor recepción a pedido del cliente', NULL, NULL, 1, 58, 16, 34, NULL),
(130, '1/1223', '2023', '2023-10-26 14:14:40', '2023-10-26 15:09:05', '192.168.1.100', NULL, NULL, 1, 67, NULL, 42, NULL),
(131, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', '192.168.1.101  S/N:01-0102-5522', NULL, NULL, 1, 34, NULL, 41, NULL),
(132, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', '192.168.1.102 S/N:01-0102-6184', NULL, NULL, 1, 69, NULL, 40, NULL),
(133, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', '192.168.1.106 S/N:01-0102-6183', NULL, NULL, 1, 69, NULL, 40, NULL),
(134, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', 'Aruba', NULL, NULL, 1, 49, NULL, 39, NULL),
(135, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', 'Aruba', NULL, NULL, 1, 49, NULL, 39, NULL),
(136, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', '192.168.1.103 S/N:01-0102-6182', NULL, NULL, 1, 54, NULL, 38, NULL),
(137, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', 'HDMI 192.168.1.104 one-seg y HD 9Mb S/N:01-0102-6142\r\n', NULL, NULL, 1, 70, NULL, 37, NULL),
(138, NULL, '2023', '2023-10-26 15:03:10', '2023-10-26 15:03:10', 'HDMI 192.168.1.105 (idem repuesto) S/N:01-0102-6181\r\n', NULL, NULL, 1, 70, NULL, 37, NULL),
(140, NULL, '2018', '2023-11-03 10:17:34', '2023-11-03 10:17:34', '#1 \r\nNDS3542\r\n172.30.9.8 \r\n20.1 	7 Mbps Municipalidad de Concordia 1\r\n20.2	        3 Mbps Municipalidad de Concordia 2\r\n64QAM 1/16 3/4 RF -14,5dBm', NULL, NULL, 1, 58, 20, 44, NULL),
(141, NULL, '2018', '2023-11-03 10:17:34', '2023-11-03 10:17:34', '#2 \r\nNDS3542 (usa solo encoder, replicado el modulador)\r\n172.30.9.9 \r\n20.3	   3 Mbps Direccion Electrotécnica y comunicaciones 1\r\n20.4    3 Mbps Direccion Electrotécnica y comunicaciones 2', NULL, NULL, 1, 58, 20, 44, NULL),
(142, '1/0218', '2018', '2023-11-08 13:27:23', '2023-11-08 16:36:59', 'ex TRU400 linealizado', '180102-1_0218_caratula.pdf', '180102-1_0218.pdf', 1, 13, 20, 43, NULL),
(143, '2/0219', '2019', '2023-11-09 11:34:53', '2023-11-09 11:34:53', '192.168.1.90', NULL, NULL, 1, 55, 16, 50, NULL),
(144, NULL, '2019', '2023-11-09 11:34:53', '2023-11-09 11:34:53', '192.168.1.40', NULL, NULL, 1, 37, 16, 49, NULL),
(145, NULL, '2019', '2023-11-09 11:34:53', '2023-11-09 11:34:53', '192.168.1.30', NULL, NULL, 1, 58, NULL, 48, NULL),
(146, '1/0219', '2019', '2023-11-09 11:34:53', '2023-11-09 11:34:53', '192.168.1.100', NULL, NULL, 1, 15, 16, 47, NULL),
(154, '1/1122', '2022', '2023-11-10 15:55:00', '2023-11-21 12:45:38', '10.0.0.92 instalado en PARANA', '220516-1_1122_caratula.pdf', '220516-1_1122.pdf', 1, 20, 18, 12, 'Paraná'),
(155, NULL, '2017', '2023-11-17 10:42:48', '2023-11-21 13:18:33', '4-1 SNMP	\r\n192.168.1.30\r\nsalidas IP 224.2.2.2 12001/3\r\n1 - MULTIVISIÓN HD 8M\r\n2 - SIN NOMBRE SD 3M\r\n3 - SIN NOMBRE/SIN SEÑAL SD 3M', NULL, NULL, 10, 72, NULL, 51, 'Estudios'),
(156, NULL, '2017', '2023-11-17 10:42:48', '2023-11-21 13:10:39', 'HP.192.168.1.2  admin :: blank\r\n! Port 1: VLAN 1+5 (Enlace Fibra)\r\n! Port 2: VLAN 1 (NMS Encoder)\r\n! Port 3: VLAN 1\r\n! Port 4: VLAN 1 (PC Control)\r\n! Port 5: VLAN 5 (DATA Encoder, video MPTS)\r\n! Port 6: VLAN 5 ()\r\n! Port 7: VLAN 1\r\n! Port 8: VLAN 1 (Notebook Control)', NULL, NULL, 10, 49, NULL, 52, 'Estudios'),
(157, NULL, '2017', '2023-11-17 10:42:48', '2023-11-21 11:09:23', 'Switch Planta Transmisora (IP 192.168.1.1):\r\n! Port 1: VLAN 1+5 (Enlace Fibra)\r\n! Port 2: VLAN 1 (Control Mux)\r\n! Port 3: VLAN 1\r\n! Port 4: VLAN 1 (Control Modulador)\r\n! Port 5: VLAN 5 (GbE1 Mux)\r\n! Port 6: VLAN 1 (Control TRUD500)\r\n! Port 7: VLAN 1 (Control equipo analógico)\r\n! Port 8: VLAN 1', NULL, NULL, 10, 49, NULL, 52, 'Cerro'),
(158, '1/0117', '2017', '2023-11-17 11:58:28', '2023-11-21 13:21:24', '192.168.1.100', NULL, NULL, 10, 15, 35, 56, 'Cerro'),
(159, NULL, '2017', '2023-11-17 11:59:56', '2023-11-21 13:20:46', '192.168.1.40\r\nSe usa la salida \"BTS MONITOR\" la salida ASI parece no andar\r\nModo 3 - IG=1/8\r\nLA=1 QPSK\r\nLB=12 64QAM', NULL, NULL, 10, 74, 35, 53, 'Cerro'),
(160, NULL, '2017', '2023-11-17 12:09:29', '2023-11-21 11:07:50', '', NULL, NULL, 10, 73, 35, 57, 'Cerro'),
(161, '2/0117', '2017', '2023-11-17 12:19:28', '2023-11-21 13:21:57', '64QAM 1/16\r\n192.168.1.90\r\n', NULL, NULL, 10, 55, 35, 55, 'Cerro'),
(162, NULL, '2017', '2023-11-17 12:20:46', '2023-11-21 11:08:42', 'Modo 3 - IG=1/8\r\nLA=1 QPSK\r\nLB=12 64QAM\r\n192.168.1.40', NULL, NULL, 10, 36, 35, 54, 'Cerro'),
(163, NULL, '2017', '2023-11-17 12:26:27', '2023-11-18 12:10:52', '192.168.0.30\r\nSDI HD\r\nSDI SD\r\nSDI SD\r\nSDI SD', NULL, NULL, 10, 72, NULL, 51, 'Salta'),
(164, NULL, '2017', '2023-11-17 12:26:27', '2023-11-18 12:10:39', '', NULL, NULL, 10, 49, NULL, 52, 'Salta'),
(165, '3/0117', '2017', '2023-11-17 12:26:27', '2023-11-18 12:06:19', '192.168.0.100', NULL, NULL, 10, 13, 35, 58, 'Salta'),
(166, NULL, '2017', '2023-11-17 12:26:27', '2023-11-18 01:49:37', '', NULL, NULL, 10, 73, 35, 57, 'Salta'),
(167, '4/0117', '2017', '2023-11-17 12:26:27', '2023-11-18 01:49:45', 'IP: 192.168.0.90', NULL, NULL, 10, 55, 35, 55, 'Salta'),
(168, NULL, '2017', '2023-11-17 12:26:27', '2023-11-18 01:49:53', 'Modo 3 - IG=1/8\r\nLA=1 QPSK\r\nLB=12 64QAM\r\n192.168.0.40', NULL, NULL, 10, 74, 35, 53, 'Salta'),
(169, '1/1123', '2023', '2023-11-21 13:45:40', '2023-11-21 13:45:40', '', '231006-1_1123_caratula.pdf', '231006-1_1123.pdf', 10, 10, NULL, 60, NULL),
(170, '2/1123', '2023', '2023-11-21 13:45:40', '2023-11-21 15:09:26', 'Frec: 101,3MHz,  105,1MHz,  106,3MHz,  107,9MHz', NULL, NULL, 10, 75, NULL, 59, NULL);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `equipment`
--
ALTER TABLE `equipment`
  ADD CONSTRAINT `eq_detalle` FOREIGN KEY (`detalle_trabajo_id`) REFERENCES `detalle_trabajo` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `eq_frec` FOREIGN KEY (`frecuencia_id`) REFERENCES `frecuencia` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `eq_modelo` FOREIGN KEY (`modelo_id`) REFERENCES `modelo` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `eq_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
