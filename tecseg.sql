-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 18-06-2023 a las 01:25:01
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
CREATE DATABASE IF NOT EXISTS `tecseg` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `tecseg`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciudad`
--

DROP TABLE IF EXISTS `ciudad`;
CREATE TABLE IF NOT EXISTS `ciudad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cp` varchar(15) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `provincia_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `ciudad`
--

INSERT INTO `ciudad` (`id`, `cp`, `nombre`, `provincia_id`) VALUES
(1, '5000', 'Córdoba', 6),
(2, '6300', 'Santa Rosa', 11),
(7, 'codPostal', 'ciud', 85),
(8, 'codPostal', 'ciud', 86),
(9, ' ', ' ', 87),
(10, '', '', 88);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_name` varchar(150) NOT NULL,
  `business_name` varchar(150) DEFAULT NULL,
  `contact` varchar(250) DEFAULT NULL,
  `comments` varchar(1000) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `domicilio_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `domicilio_id` (`domicilio_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `client`
--

INSERT INTO `client` (`id`, `client_name`, `business_name`, `contact`, `comments`, `user_id`, `domicilio_id`) VALUES
(0, 'Luis Ponzonetta', 'TV Broadcast', '42432432', 'radicado en Uruguay', 1, 9),
(1, 'Canal 13 san luis', 'Canal 13 televisión', '42432432', 'Director Nasim', 1, 9),
(2, 'Bonarrico', 'Jesus Te Ama', '02954-4303248', 'o contactarlo por mail: bonarrico@jta.com\r\n\r\n', 2, 9),
(3, 'Juan Antonio Acompanies', 'REMAR', '123123123', 'Exportador a Paraguay', 3, 9),
(4, 'Pedro Almirón', 'Radio Total FM', '2147483647', 'teléfono del técnico\r\nFernandez: 2996-1235432\r\n10-14hs solamente', 1, 9),
(6, 'Mariangeles Gonzalez', 'MARIAN S.A.', '2147483647', 'persona ficticia', 1, 9),
(11, 'Marcelo Gomez', 'Digital Content S.R.L.', '2147483647', 'Datos del cliente', 1, 9),
(16, 'Oscar de la Fuente', 'De la Hoya S.R.L.', '42432432', 'cliente preferencial', 1, 9),
(17, 'Fabio Brandan', 'JTA S.A.', '1111333222', 'Suele modificar configuraciones sin preguntar antes', 10, 9),
(18, 'Ana Lupe', 'RF Argentina S.A.', '432654765', '', 10, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `domicilio`
--

DROP TABLE IF EXISTS `domicilio`;
CREATE TABLE IF NOT EXISTS `domicilio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direccion` varchar(150) DEFAULT NULL,
  `ciudad_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_ciudad` (`ciudad_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `domicilio`
--

INSERT INTO `domicilio` (`id`, `direccion`, `ciudad_id`) VALUES
(1, 'San Martin 514', 2),
(2, 'Belgrano 519', 1),
(7, 'domicilio', 7),
(8, 'domicilio', 8),
(9, ' ', 9),
(10, '', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipment`
--

DROP TABLE IF EXISTS `equipment`;
CREATE TABLE IF NOT EXISTS `equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `numSerie` varchar(20) DEFAULT NULL,
  `anio` varchar(20) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  `date_modified` datetime DEFAULT NULL,
  `content` varchar(1000) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `equipment`
--

INSERT INTO `equipment` (`id`, `title`, `numSerie`, `anio`, `date_created`, `date_modified`, `content`, `user_id`, `client_id`) VALUES
(1, 'TRUD400', '223454-2/0322', '2012', '2022-05-21 04:37:49', '2022-05-21 04:37:49', 'num ser: 1111111111\r\n\r\nCH: 21\r\n\r\nIP: 192.168.0.100', 1, 1),
(2, 'FM250', '193454-2/0719', '2012', '2022-05-21 04:39:05', '2022-05-21 04:39:05', 'num ser: 22222222\r\n\r\nFREC: 103,1MHz\r\n\r\nIP: 192.168.0.101', 3, 1),
(3, 'MFM4', '213454-2/0222', '2013', '2022-05-21 04:57:38', '2022-05-21 04:57:38', 'num ser: 3333333333', 3, 2),
(4, 'FM1K', '227455-2/0123', '2014', '2022-05-21 04:59:10', '2022-05-21 04:59:10', 'num ser: 444444444\r\n\r\nFREC: 95,3MHz\r\n\r\nIP: 192.168.0.101', 3, 2),
(5, 'TRUD1200', '223454-2/0722', '2014', '2022-05-21 05:01:19', '2022-05-21 05:01:19', 'num ser: 55555555555\r\n\r\nCH: 14\r\n\r\nIP: 192.168.0.101', 1, 2),
(6, 'AGCV2000', '223454-2/0722', '2018', '2022-05-21 05:01:34', '2023-04-20 23:32:25', 'N serie: 223982-1/0422', 1, 11),
(7, 'TRV200', '223454-2/0722', '2019', '2022-05-21 05:10:24', '2022-05-21 05:10:24', 'num ser: 377777777\r\n\r\nCH: 7', 1, 2),
(8, 'FM100', '223454-2/0722', '2019', '2022-05-21 14:43:33', '2023-04-20 23:33:17', 'N serie: 233232-3/0423', 1, 1),
(9, 'FM100', '223454-2/0722', '2022', '2022-05-21 14:44:12', '2023-04-20 23:33:07', 'N serie: 233232-2/0423', 1, 1),
(10, 'FM100', '223454-2/0722', '2020', '2022-05-21 14:45:55', '2023-04-20 23:32:56', 'N serie: 233232-1/0423', 1, 1),
(11, 'FM200', '223454-2/0722', '2020', '2022-05-24 02:20:00', '2023-04-20 23:32:04', 'N serie: 213982-4/0422', 1, 3),
(12, 'FM2000', '223454-2/0722', '2020', '2022-05-25 14:58:24', '2023-04-20 23:31:54', 'N serie: 213982-3/0422', 1, 3),
(13, 'FM250', '223454-2/0722', '2021', '2022-05-30 02:41:13', '2023-04-20 23:31:42', 'N serie: 213982-2/0422', 1, 3),
(14, 'TRUD1300', '223454-2/0722', '2021', '2022-06-05 04:03:02', '2023-04-20 23:31:31', 'N serie: 213982-1/0422', 1, 3),
(15, 'TRUD400', '223454-2/0722', '2021', '2022-06-13 03:21:29', '2023-04-20 23:26:03', '12/08/19\r\n\r\nse agregó una señal de tv digital al Mux\r\n\r\n\r\n\r\n12/08/20\r\n\r\nse repararon 2 ventiladores forzadores de aire del control general\r\n\r\n\r\n\r\n12/08/22\r\n\r\nuna descarga quemó la fuente del sumador', 1, 6),
(16, 'TRU400', '12345432/8765', '2022', '2022-06-13 03:22:03', '2023-06-14 19:14:47', '03/02/22\r\n\r\nSe cambió la frecuencia del modulador a CH:13', 10, 6),
(17, 'FM250', '223454-3/0522', '2022', '2022-06-13 03:30:03', '2023-06-17 15:12:17', 'frec: 91,9MHz', 1, 4),
(18, 'TRU200', '', '2022', '2022-06-13 20:56:51', '2023-06-17 15:22:36', 'CH: 15', 1, 4),
(19, 'TRV100', NULL, '2022', '2022-06-13 21:26:02', '2023-04-20 23:23:41', '13/04/20\r\n\r\nReparación de dos módulos de potencia (Atilio)', 1, 6),
(20, 'TRUD1200', NULL, NULL, '2022-06-22 21:32:29', '2023-04-20 23:30:59', 'Rack: 6 modulos \r\n\r\nnum de serie: 220422-1/0224\r\n\r\narmado: completo\r\n\r\nfirmado: Oscar\r\n\r\n\r\n\r\nfecha: 20/03/22\r\n\r\ntel tecnico: 0345-2321387\r\n\r\nmanual: DMTRUD1200-22.pdf', 1, 0),
(21, 'FM100', '020823-1/0423', '2023', '2022-06-23 01:15:03', '2023-06-17 15:09:06', 'frec: 101,3MHz', 10, 4),
(22, 'FM100', '220223-1/0422', '2016', '2022-06-22 22:16:56', '2023-06-17 15:10:29', 'frec: 97,5MHz', 1, 4),
(23, 'TRV250', '223454-2/0722', '2022', '2022-06-22 22:19:54', '2023-06-17 15:08:41', 'Canal: 7', 10, 4),
(33, 'Sistema TV Digital', '230504-1/8765', '2023', '2023-04-20 23:24:06', '2023-06-14 13:45:31', 'Encoder LP211_IP: 192.168.1.30\r\nMultiplexor DMUX1000_IP: 192.168.1.40\r\nModulador 3542_IP: 192.168.1.90', 10, 16),
(34, 'DMUX1000', '', '2023', '2023-05-20 14:39:38', '2023-06-17 16:48:53', 'IP: 192.168.0.90\r\nNuevo multiplexor de videoswitch', 1, 2),
(37, 'NDS3542', '', '2015', '2023-05-20 14:57:38', '2023-06-17 16:48:09', 'IP: 192.168.1.90\r\nmodulador chino, 13 segmentos capa A', 1, 0),
(59, 'TRU400', NULL, '2015', '2023-06-05 19:33:17', '2023-06-13 15:41:00', 'canal:13\r\n(ex canal: 14)', 10, 3),
(68, 'FM100', '190522-2/1220', '2023', '2023-06-14 13:07:56', '2023-06-17 16:31:12', 'Frec: 98,3MHz', 10, 11),
(69, 'TRM26100', '230306-1/0723', '2023', '2023-06-14 13:34:50', '2023-06-17 01:26:07', '6 canales', 1, 17),
(70, 'DMUX-1000', '230617-1/0723', 'N/D', '2023-06-17 16:02:08', '2023-06-17 16:29:49', 'IP: 192.168.1.136', 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eq_detail`
--

DROP TABLE IF EXISTS `eq_detail`;
CREATE TABLE IF NOT EXISTS `eq_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `content` varchar(1000) DEFAULT NULL,
  `tipologia_id` int(11) NOT NULL,
  `equipment_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `equipment_id` (`equipment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `eq_detail`
--

INSERT INTO `eq_detail` (`id`, `title`, `date_created`, `date_modified`, `content`, `tipologia_id`, `equipment_id`, `user_id`) VALUES
(1, 'Reparacion ventiladores', '2023-06-04 12:16:37', '2023-06-04 12:16:37', 'Se desarmo el equipo y se constato que los ventiladores no funcionaban por lo que se procedió a cambiarlos y eso resolvió el problema', 2, NULL, 10),
(5, 'Cambio de IP', '2023-06-05 16:02:19', '2023-06-05 16:02:19', '192.168.1.101', 3, NULL, 10),
(15, 'Linealidad', '2023-06-05 19:33:17', '2023-06-05 19:33:17', 'equipo ex TRU400, se linealizo para uso digital, y se hizo uso extremo de la potencia para mantener la pot nominal RMS', 1, 1, 10),
(16, 'retraso en entrega', '2023-06-13 11:08:00', '2023-06-13 11:08:00', 'la entrega se realizo dos semana después de lo pactado', 1, 59, 10),
(17, 'verificacion por pedido del cliente', '2023-06-14 13:34:50', '2023-06-14 13:34:50', 'se reviso a fondo!', 2, 33, 10),
(18, 'ventiladores', '2023-06-15 15:40:48', '2023-06-15 15:40:48', 'se cambiaron los ventiladores del equipo', 2, NULL, 1),
(19, 'Entregado', '2023-06-15 15:45:42', '2023-06-15 15:45:42', 'se entregó con retardo de dos semanas', 1, 69, 1),
(20, 'Fuente', '2023-06-15 15:59:36', '2023-06-15 15:59:36', 'falla en la fuente auxiliar, se cambió por fuente meanwell', 2, 69, 1),
(21, 'IP', '2023-06-16 14:54:54', '2023-06-16 14:54:54', 'se cambio la IP a : 192.168.1.14', 3, 69, 10),
(22, 'Revisión', '2023-06-16 15:56:55', '2023-06-17 15:56:14', 'se revisó el equipo y funciona correctamente.', 1, 69, 10),
(23, 'envio de equipo', '2023-06-16 15:56:55', '2023-06-16 15:56:55', 'Se programó un envío para el 25/08/22. Se aguarda confirmación', 1, 23, 10),
(24, 'linealidad', '2023-06-16 15:56:55', '2023-06-16 15:56:55', 'consultó por modificar la linealidad del amplificador para ser usado para TV digital', 3, 23, 10),
(25, 'cambio IP', '2023-06-16 20:27:27', '2023-06-16 20:27:27', 'IP: 10.0.0.97', 1, 23, 1),
(26, 'fotos', '2023-06-16 20:27:27', '2023-06-16 20:27:27', 'se sacaron fotos del frente y fondo', 1, 23, 1),
(27, 'manual', '2023-06-17 15:03:51', '2023-06-17 15:03:51', 'Manual enviado via mail', 1, 21, 10),
(28, 'actualización', '2023-06-17 15:03:51', '2023-06-17 15:03:51', 'equipo reacondicionado y actualizado a versión \'22', 3, 17, 10),
(29, 'Modelo equipo', '2023-06-17 15:21:08', '2023-06-17 15:21:08', 'modelo original TRU250', 1, 18, 10),
(30, '432', '2023-06-17 16:02:08', '2023-06-17 16:02:08', 'dsa', 1, 69, 10),
(31, 'modelo', '2023-06-17 16:29:37', '2023-06-17 16:29:37', 'Este equipo es modelo 2023\r\nTomado de un modelo 2016', 3, 68, 1);

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
-- Estructura de tabla para la tabla `orden_reparacion`
--

DROP TABLE IF EXISTS `orden_reparacion`;
CREATE TABLE IF NOT EXISTS `orden_reparacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime NOT NULL,
  `date_modified` datetime DEFAULT NULL,
  `codigo` varchar(50) NOT NULL,
  `content` varchar(250) DEFAULT NULL,
  `tecnico_id` int(11) DEFAULT NULL,
  `equipo_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `estado_id` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `equipment_id` (`equipo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `orden_reparacion`
--

INSERT INTO `orden_reparacion` (`id`, `date_created`, `date_modified`, `codigo`, `content`, `tecnico_id`, `equipo_id`, `user_id`, `estado_id`) VALUES
(2, '2023-06-13 12:20:25', '2023-06-16 11:11:02', '230327-1/0423', 'Reparar ventiladores', 6, 10, 10, 4),
(6, '2023-06-13 12:41:08', '2023-06-16 23:48:01', '210615-1/0621', 'Revisar el equipo, presenta falla RF', 5, 3, 10, 2),
(9, '2023-06-14 11:59:34', '2023-06-16 23:18:45', '220516-1/1122', 'Se envió el módulo de potencia porque no enciende', 6, 13, 10, 2),
(12, '2023-06-14 12:28:20', '2023-06-17 16:08:38', '230313-6/0920', 'Pedido de reparación por falla de temperatura', NULL, 1, 10, 1),
(13, '2023-06-16 11:48:15', '2023-06-16 13:24:56', '230422-1/0322', 'Cambiar de frecuencia a 107,1MHz', 14, 17, 10, 3),
(14, '2023-06-16 12:14:01', '2023-06-16 12:20:52', '230516-1/170523', 'cambiar base de tiempo a GPS integrado', 5, 34, 10, 2),
(15, '2023-06-16 12:33:40', '2023-06-16 23:45:27', '230313-6/0920', 'revisar configuracion', NULL, 34, 10, 1),
(16, '2023-06-17 16:02:08', '2023-06-17 16:02:08', '223454', 'ver conexión TIBBO por problemas', 1, 14, 10, 2),
(17, '2023-06-17 16:02:08', '2023-06-17 16:20:02', '193454', 'cambiar de frec a 98,5MHz', 1, 2, 10, 4),
(18, '2023-06-17 16:02:08', '2023-06-17 16:02:08', '213454', 'problemas entrada 220V', 1, 3, 10, 2),
(19, '2023-06-17 16:02:08', '2023-06-17 16:20:10', '230504', 'cambiar modulacion: \r\nIG: 1/32\r\nContelacion=64QAM', 1, 33, 10, 3);

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;

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
(8, 'Entre Ríos', 1),
(9, 'Formosa', 1),
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
(79, 'Tocantins', 3),
(86, 'prov', 21),
(87, ' ', 1),
(88, '', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `id` int(11) NOT NULL,
  `role_name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `role`
--

INSERT INTO `role` (`id`, `role_name`) VALUES
(1, 'Admin'),
(2, 'Invitado'),
(3, 'Técnico'),
(4, 'ServicioCliente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipologia`
--

DROP TABLE IF EXISTS `tipologia`;
CREATE TABLE IF NOT EXISTS `tipologia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `tipologia`
--

INSERT INTO `tipologia` (`id`, `tipo`) VALUES
(1, 'Mensaje'),
(2, 'Reparación'),
(3, 'Modificación');

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
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `password` (`password`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `image_file`, `password`, `role_id`) VALUES
(1, 'Turko', 'arnaizagustin@gmail.com', '18789144792542e0.jpg', '$2b$12$2aL8KrZk6zd4NTk0Hr0UneVLOcQHuZBSLYrRORuElTZOklrI6kw9a', 3),
(4, 'Alejandro Ruiz', 'toparuiz@mail.com', '51a1e8e115f3c97c.jpg', '$2b$12$VrhQjceSifK79HNg0smr2uidZRnklPL3tFbI54TevRvg2LJ8DkMWu', 1),
(5, 'Atilio', 'atilio@mail.com', 'f830c0210df9532a.png', '$2b$12$.9g0xMzY6Ov8CEmsuvG5secn12KAfy/JPpffzeYddw81tE.KBg3sy', 3),
(6, 'Oscar', 'oscar@mail.com', '78fcd03e420ea343.jpg', '$2b$12$2BYblyKU0bxi7P4SVglbVe6UamACecyb5nfsmsa5nEzNvtNlIteIK', 3),
(10, 'admin', 'admin@tecseg.com', '61103f056de4ab95.jpg', '$2b$12$dIxpjyQ/uTr8Z7owkfrZKuNoQ5oF4moJHeJgBwjO2X65gmCW.YEWO', 1),
(11, 'Tomas', 'tomas@tecseg.com', 'c1ed20648c2746a0.jpg', '$2b$12$nFwkmd5n6bdgmyroTvpjlehN15JEavOoNpEP/R1DXpAx09GjTJNc6', 4),
(12, 'Juan', 'juan@tecseg.com', '708207d226459aaa.jpg', '$2b$12$K2jwJpDeVQyYm0P5iQlGougGR5wG7E.XUb5GadmJEt3PlvijZXRM.', 4),
(14, 'Jorge', 'jorge@tecseg.com', 'default.jpg', '$2b$12$8fFUwOfpjV.eHRy11awAjexyJ/kFyryGpGNCL2Eg82xZxNSpeRW3e', 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
