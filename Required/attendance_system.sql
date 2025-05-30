-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3308
-- Generation Time: May 30, 2025 at 05:26 PM
-- Server version: 8.3.0
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `attendance_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance_attendancerecord`
--

DROP TABLE IF EXISTS `attendance_attendancerecord`;
CREATE TABLE IF NOT EXISTS `attendance_attendancerecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(10) NOT NULL,
  `time_in` datetime(6) DEFAULT NULL,
  `time_out` datetime(6) DEFAULT NULL,
  `marked_with` varchar(20) NOT NULL,
  `comments` longtext,
  `marked_by_id` bigint DEFAULT NULL,
  `student_id` bigint NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `attendance_attendancerecord_student_id_session_id_7a9b92cf_uniq` (`student_id`,`session_id`),
  KEY `attendance_attendancerecord_marked_by_id_c49b69c9` (`marked_by_id`),
  KEY `attendance_attendancerecord_student_id_d242c468` (`student_id`),
  KEY `attendance_attendancerecord_session_id_ddf44875` (`session_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `attendance_attendancerecord`
--

INSERT INTO `attendance_attendancerecord` (`id`, `status`, `time_in`, `time_out`, `marked_with`, `comments`, `marked_by_id`, `student_id`, `session_id`) VALUES
(9, 'PRESENT', '2025-05-14 17:37:13.888022', NULL, 'FACE', NULL, 7, 2, 4),
(10, 'PRESENT', '2025-05-14 17:41:12.378609', NULL, 'FACE', NULL, 7, 11, 4),
(11, 'PRESENT', '2025-05-26 07:21:05.559570', NULL, 'FACE', NULL, 7, 2, 3),
(12, 'ABSENT', NULL, NULL, 'MANUAL', NULL, 12, 2, 5),
(13, 'ABSENT', NULL, NULL, 'MANUAL', NULL, 12, 17, 5),
(14, 'PRESENT', '2025-05-26 07:27:10.644797', NULL, 'FACE', NULL, 12, 18, 5);

-- --------------------------------------------------------

--
-- Table structure for table `attendance_session`
--

DROP TABLE IF EXISTS `attendance_session`;
CREATE TABLE IF NOT EXISTS `attendance_session` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `attendance_session_course_id_date_start_time_957df254_uniq` (`course_id`,`date`,`start_time`),
  KEY `attendance_session_course_id_dbd973da` (`course_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `attendance_session`
--

INSERT INTO `attendance_session` (`id`, `date`, `start_time`, `end_time`, `description`, `is_active`, `course_id`) VALUES
(3, '2025-05-08', '09:00:00.000000', '10:00:00.000000', '1st class', 1, 2),
(4, '2025-05-08', '10:00:00.000000', '11:00:00.000000', '2nd Period', 1, 6),
(5, '2025-05-26', '12:15:00.000000', '13:15:00.000000', NULL, 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add course', 6, 'add_course'),
(22, 'Can change course', 6, 'change_course'),
(23, 'Can delete course', 6, 'delete_course'),
(24, 'Can view course', 6, 'view_course'),
(25, 'Can add department', 7, 'add_department'),
(26, 'Can change department', 7, 'change_department'),
(27, 'Can delete department', 7, 'delete_department'),
(28, 'Can view department', 7, 'view_department'),
(29, 'Can add custom user', 8, 'add_customuser'),
(30, 'Can change custom user', 8, 'change_customuser'),
(31, 'Can delete custom user', 8, 'delete_customuser'),
(32, 'Can view custom user', 8, 'view_customuser'),
(33, 'Can view attendance records', 8, 'can_view_attendance'),
(34, 'Can mark attendance', 8, 'can_mark_attendance'),
(35, 'Can manage users', 8, 'can_manage_users'),
(36, 'Can add attendance record', 9, 'add_attendancerecord'),
(37, 'Can change attendance record', 9, 'change_attendancerecord'),
(38, 'Can delete attendance record', 9, 'delete_attendancerecord'),
(39, 'Can view attendance record', 9, 'view_attendancerecord'),
(40, 'Can add session', 10, 'add_session'),
(41, 'Can change session', 10, 'change_session'),
(42, 'Can delete session', 10, 'delete_session'),
(43, 'Can view session', 10, 'view_session');

-- --------------------------------------------------------

--
-- Table structure for table `core_course`
--

DROP TABLE IF EXISTS `core_course`;
CREATE TABLE IF NOT EXISTS `core_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `description` longtext,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `teacher_id` bigint DEFAULT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `slug` (`slug`),
  KEY `core_course_teacher_id_c5fe8e73` (`teacher_id`),
  KEY `core_course_department_id_2e55d724` (`department_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `core_course`
--

INSERT INTO `core_course` (`id`, `name`, `code`, `slug`, `description`, `start_date`, `end_date`, `teacher_id`, `department_id`) VALUES
(2, 'Discrete Mathematics', '24BCA201', 'discrete-mathematics', '', '2025-02-17', '2025-07-04', 9, 2),
(3, 'Programming in Python', '24BCA202', 'programming-in-python', '', '2025-02-17', '2025-07-04', 8, 2),
(4, 'Data Structure using C', '24BCA203', 'data-structure-using-c', 'Good Course', '2025-02-17', '2025-07-04', 12, 2),
(5, 'Database Management System', '24BCA204', 'database-management-system', 'GOOD COURSE', '2025-02-17', '2025-07-04', 13, 2),
(6, 'Operating Systems with Unix', '24BCA005', 'operating-systems-with-unix', '', '2025-02-17', '2025-07-04', 14, 2),
(7, 'Quantitiative Aptitude and Logical Reasoning', '24BCA006', 'quantitiative-aptitude-and-logical-reasoning', 'Good', '2025-02-17', '2025-07-03', 15, 2),
(8, 'Indian Constitution', '24BCA207', 'indian-constitution', 'Good Course', '2025-02-17', '2025-07-02', 16, 2);

-- --------------------------------------------------------

--
-- Table structure for table `core_course_students`
--

DROP TABLE IF EXISTS `core_course_students`;
CREATE TABLE IF NOT EXISTS `core_course_students` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `course_id` bigint NOT NULL,
  `customuser_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_course_students_course_id_customuser_id_7e8e7edc_uniq` (`course_id`,`customuser_id`),
  KEY `core_course_students_course_id_f401f754` (`course_id`),
  KEY `core_course_students_customuser_id_29719860` (`customuser_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `core_course_students`
--

INSERT INTO `core_course_students` (`id`, `course_id`, `customuser_id`) VALUES
(2, 2, 2),
(3, 3, 2),
(4, 4, 2),
(5, 5, 2),
(13, 4, 17),
(9, 7, 2),
(10, 8, 2),
(12, 6, 11),
(14, 4, 18);

-- --------------------------------------------------------

--
-- Table structure for table `core_department`
--

DROP TABLE IF EXISTS `core_department`;
CREATE TABLE IF NOT EXISTS `core_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `description` longtext,
  `head_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_department_head_id_7e6d49b3` (`head_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `core_department`
--

INSERT INTO `core_department` (`id`, `name`, `code`, `description`, `head_id`) VALUES
(2, 'Bachelor in computer application', 'BCA', 'Bachelor in computer application in cloud computing and cyber security is good course', 10);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(3, '2025-05-04 17:58:59.856343', '2', 'aakash (Student)', 2, '[]', 8, 2),
(4, '2025-05-04 18:01:30.947629', '1', 'root (Student)', 3, '', 8, 2),
(5, '2025-05-04 18:01:39.941614', '2', 'aakash (Student)', 2, '[]', 8, 2),
(6, '2025-05-04 18:01:56.633006', '2', 'aakash (Student)', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Phone number\"]}}]', 8, 2),
(7, '2025-05-04 18:03:08.456764', '3', 'admin (Student)', 3, '', 8, 2);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'core', 'course'),
(7, 'core', 'department'),
(8, 'users', 'customuser'),
(9, 'attendance', 'attendancerecord'),
(10, 'attendance', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-05-04 16:53:25.836258'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-05-04 16:53:25.914488'),
(3, 'auth', '0001_initial', '2025-05-04 16:53:26.219147'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-05-04 16:53:26.287103'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-05-04 16:53:26.294607'),
(6, 'auth', '0004_alter_user_username_opts', '2025-05-04 16:53:26.325611'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-05-04 16:53:26.336520'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-05-04 16:53:26.337529'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-05-04 16:53:26.343587'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-05-04 16:53:26.349585'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-05-04 16:53:26.355935'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-05-04 16:53:26.386326'),
(13, 'auth', '0011_update_proxy_permissions', '2025-05-04 16:53:26.394327'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-05-04 16:53:26.400864'),
(15, 'users', '0001_initial', '2025-05-04 16:53:26.717979'),
(16, 'admin', '0001_initial', '2025-05-04 16:53:27.021737'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-05-04 16:53:27.037772'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-04 16:53:27.046209'),
(19, 'core', '0001_initial', '2025-05-04 16:53:27.063291'),
(20, 'attendance', '0001_initial', '2025-05-04 16:53:27.090304'),
(21, 'attendance', '0002_initial', '2025-05-04 16:53:27.543980'),
(22, 'core', '0002_initial', '2025-05-04 16:53:28.043260'),
(23, 'sessions', '0001_initial', '2025-05-04 16:53:28.095732');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('bk2bezmozejio4k17twbid8mbht0oivv', '.eJxVjEEOwiAQRe_C2hDJ0A64dO8ZyMAMUjWQlHbVeHdt0oVu_3vvbyrQupSwdpnDxOqiUJ1-t0jpKXUH_KB6bzq1usxT1LuiD9r1rbG8rof7d1Col29tmcBjRDFCgObMIEM21qAHJIAsIzG56D24MQ2M6JCQWaLkaEFEvT_tQjiv:1uJY7d:stb8cIQ874sGfvVQi_V0REJMawxODi6J5R_BhCknL_w', '2025-06-09 13:44:09.907053');

-- --------------------------------------------------------

--
-- Table structure for table `users_customuser`
--

DROP TABLE IF EXISTS `users_customuser`;
CREATE TABLE IF NOT EXISTS `users_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `barcode_id` varchar(50) DEFAULT NULL,
  `face_encoding` longblob,
  `profile_pic` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `barcode_id` (`barcode_id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users_customuser`
--

INSERT INTO `users_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `barcode_id`, `face_encoding`, `profile_pic`, `phone_number`) VALUES
(10, 'pbkdf2_sha256$1000000$RW9rzXbJt3KTUjb47n3WxB$vtYgqhZlGC8p0Rn/3kQfiJwxu25gJQiYfbA6mkAqifU=', NULL, 0, 'Jagannathsir', 'Jagannath', 'Director Sir', 'jagannath@gmail.com', 0, 1, '2025-05-04 19:09:58.630444', 'TEACHER', '24BCADR000', NULL, '', NULL),
(2, 'pbkdf2_sha256$1000000$7mNEEdN03qne4T0wSZtDky$Z4U9CHfqK2LlIHldtyV3cpMyBpWT2+Rzrht99JJq02Y=', '2025-05-04 18:53:04.250734', 1, 'aakashsapkotaa', 'Aakash', 'Sapkota', 'sapkotaswikar123@gmail.com', 1, 1, '2025-05-04 17:01:41.000000', 'STUDENT', '24SUUBCACS001', NULL, 'profile_pics/pp_I3JZ8Km.jpg', '6361752052'),
(7, 'pbkdf2_sha256$720000$qO3tMeVRo6MUQ2kNJtmq02$w7kn0zyYz2RmGnNR6FZxAAt/LLURUagoNPK+rEbZWmo=', '2025-05-26 13:44:09.905055', 1, 'superadmin', 'Super', 'Admin', 'admin@admin.com', 1, 1, '2025-05-04 18:57:49.774537', 'ADMIN', 'SNPSU', 0x8004958c040000000000008c166e756d70792e5f636f72652e6d756c74696172726179948c0c5f7265636f6e7374727563749493948c056e756d7079948c076e6461727261799493944b0085944301629487945294284b014b80859468038c0564747970659493948c02663894898887945294284b038c013c944e4e4e4affffffff4affffffff4b00749462894200040000d5242c2d826fec3f443cf08dcc45c13f00b1c35d34f7d43fcae6c1b7d083ed3ff5d8093ecefeec3f5fa95f0827d1e83fcaf6d1a38581db3f466d35cdc180e73fc162a78090aaee3f1cc56cf4cc98e73fc4c9182d398ced3f640a71b793cee73ff80a853a550ecf3f78d95999d8a1b13f56823b90ded3ee3fd091d0c62cdfa73f7e88e5bd88daea3f3cbaebaf9b7fea3fe901d09ecc97ec3fee5929b006d4e93f0da817d1ef7ce33f5c9cd0a62d06d33f61d1d98940cee93f3093b0ef927eab3f9750897f2aa7e43fa07706083fefd33fc613f9c5b7c1d73ff5425cfbedd3e43faef89ee75a86e83f30a09f19646bac3fa2625948161bdf3f0367f7127d57ee3ff8e2701f5838c03ffc2f215d5aaad03f8e1933113ea3e63f6f2ad1e8bc50e53fe6acc4947af4d03f98e9dd067a75d33f78ece96ca1bcc03f190f53c6c069ed3f480eecfdbe77b23fbabc7f01d211d13fff150d14bbecee3f89a9795c5149e63f901aa5dccc92cd3f30bb054f4dcfed3fc043cbb7dbb4e43f5830e9862cfcd73f207bead404b09b3f38ef1ece196ae03f6d9c7ef3340ce63fef78a92ea2ace13f58b90ff15430c13f2b946a82a159ef3f96f35f22e3b7df3fbdf7a5346c91e23fdd702a3e286ded3f68e56e51d2cdbd3f6e531861cd97de3fdcb8960f6004d43faeb69a8edea4d73f21ea7842fc7aec3f976af42c67bce43f77610dc5e4bbe73fa10e50a6984be03f1f3e5b9df4a7eb3ff89b48388f1cd83fc564da78169be13f789f20474f89de3f4845e6fe93ccd03fd82638475149d23f92b89f74b479e43f5c3f7608fce3df3fd930d76707b9e93f2634fa5d16a2db3ff0d4cbd894b5cd3f680ffa2583e8b53fe09d37431cb0ed3f40e12ee7eb9ae33f1c8da53d6adfd13f2c3315aa1256c13f8abd6e6eff4bda3fb680fa6c3db6e53f3853394877cfc33f920d8a6ebd48db3f1a96d75abfafe83f08b6f982e74bcc3faeae0dd4fe4cd83fe1bb71965dfbe83f0c3b8ac70729ea3f590abadb1cb9e73fc8c9f6b1998ac03fbf4e9e65ec10e13f7aa56ed45a82e03f98c6a9e83d3ad63f1ea9834f566cd43fec368dbee4a7e83f85196f235828ee3f46b2c94f1b19e73fe6efecca7de2eb3fbee59dcfb7d9dd3f8e92a3617282dc3fadf191410cbfe03ffdd673777535e33f84cff63bb375da3ff3724d28561be13f40054db02c93803f4276bc3d26dedd3fcc9ba2b72b00c03f5882b2787c16d83f8138045377a2e63f15863db31af3e23f7a47e51f64bdeb3f8672374cdcd7e43f0d97b758167eeb3f4cb16cdf1494dd3f80205fd6d2f2803f09a02af15502e63f414e01f60960eb3f54d71bfdbfc9c13f6a04e8a0daf5d33fa13a87978430e83f18589b271fe6e03f5c512df5584fc83f9b9e90f11923ee3f562cd459c478e13fe63312482f8ed33f7042316bde59d83f947494622e, '', '505152'),
(8, 'pbkdf2_sha256$1000000$xOnasTn0nVavBJCiqEcJQb$HZpmlWb8uK6qHIIp/6gSuWgih4YUf1Nj4lZ19jIfwmI=', NULL, 0, 'Sushmamam', 'Sushma', 'Mam', 'sushma@gmail.com', 0, 1, '2025-05-04 19:04:10.877315', 'TEACHER', '24SUUPY202', NULL, '', NULL),
(9, 'pbkdf2_sha256$1000000$o517JgQM66RAnnwBZs2Sxz$S0OCy/nc9eWIuJtfoRyOQGtUD8ODu2gzm214ibTyTIE=', NULL, 0, 'Shrawanimam', 'Shrawani', 'Mam', 'shrawani@gmail.com', 0, 1, '2025-05-04 19:06:46.931996', 'TEACHER', '24SUUDM001', NULL, '', NULL),
(11, 'pbkdf2_sha256$1000000$1lHZ3dG6cYTI20mFQmFNRb$3wnBvMMdWwI5PX7f14O1lU2BYJkiS6iVfnMA6lBa0Ew=', '2025-05-07 22:50:16.529021', 0, 'amarlobalob', 'amar', 'grg', 'amar@gmail.com', 0, 1, '2025-05-06 17:30:17.722544', 'STUDENT', '24SUUBCS010', 0x8004958c040000000000008c166e756d70792e5f636f72652e6d756c74696172726179948c0c5f7265636f6e7374727563749493948c056e756d7079948c076e6461727261799493944b0085944301629487945294284b014b80859468038c0564747970659493948c02663894898887945294284b038c013c944e4e4e4affffffff4affffffff4b00749462894200040000400d1ad647838d3f2815559741e9be3ffeb531098c8bdf3f3a72468666dbd93f30c6e046c387b73fc9cb2c8bd91ded3f1a6ec97948b3e63fb13aac3404ffe53f38f04a93d883b03f280521539c29d73f004b558534ce863fd830a83c9189df3f4038dc246f6fd83fd4d99da7b435ed3f98c0a88a1d9cc83f909b5a33cd3ad33f00fc16861ecbba3f1637420d5d22d53fdb92969ca6fce93f7844b51f827ebb3fe43c65c540a9ef3f2485e4f76f69e83fe0601286b785c73f367904d28f9cee3fe78c1653dfe3e83f10b2cdbbe5abb13fb0a027b0fc6ad33fe9e058ec580fe53f3423034e8944cd3f2abcf44a0e4ddc3ff964c5fe77d4e93f902eb6769ad6ce3f0fa074ecca94ec3fc09d53900607bf3f0cb6067c2601c83fb433c0a1fac7e23fc81dd928fa46b93f0ee64ffb9db5ef3f209d6e71185cc33f08a2a1fdcf5bc03fa82bff752f99e83ff8925c7fec7fb93fd99f9e56360ee43f2c3ecb6e0a70df3fd956b51d5854e43f4cb88f9491d7e83fe8c56fdcc677de3f8603982c2d1de53ff239337b3f47d03f903a3943e97dbb3ff8972643802cda3f20533b513690a83fb3ec16e1f819ef3fa88982c7f7d6ea3fe32ee0ac4c9be03f2032aeb0b21dba3fc4bd5eba3b25d03fdccc816fd771ca3f8b2dd6b8df35e73f0f92874214a2e63f60a825581b82b63f0f8096d07231e33f5bc133a04fd6e63f2c7c06c0c8d4e83f2731be6bff50e73fb029bfe16030bf3fc80e5fc882d7e83fa6f1589cb223de3f1fad6cfe2679eb3f4db7c080337ce73f70405b2a2a10ec3f30999a721c6ede3f2859001ce3a9b83fa0fb3523798fb43ff275e926b494eb3fb4ef22589db6e03f483e551a4dcbc63f5cd05980f8d2ca3f2d108214ad24e23f7c2447d5f8dccc3fc64e4542e7dfeb3f1604a39e9800e43f1ddfceb8dceceb3ff0c2a7d6ce2cd63f05ae3b836305e03f00d0b45f0da9383f98508dafaf38ce3f90cfd3446009a83f6836fd65a95ec93f983022a2ea9bbc3fb4c09dec6d25e73f8adc15e08bc7e23f7e50f2276a45dc3f04c5e8eced5cd73f3ad1913a68acd53fb6f9c5e28285ee3f0016b8370f14853fdd72b13a5846ee3f88690c5d2f4bca3f405ac150fe54e83f300aaea4e6aed03f9c78615aa075c53f009432018559e73f48ab2027e570dd3ff072e087d831eb3fd8903a31a938ec3f3fbd979329ffed3f813e5ffa32c2e83fed35f8d7d435e03fa467c26c771aea3f1c3dceba5c84c13fe403407f4c82df3f600d865d7901d03f5e475d457660d93f8abfc57600cde43faebbbc8b5e92e93f70a023fc3aaaba3f505125fe4036e83fa07f01af6b6bc93fcc972ab234a2e33f2e6796bbf8afdd3fef3fe49a31cde03fffd73cdf234be03f401d4c6eba84da3f202db1121042d63f3083b7ab8216a53f2ed29af6aac4da3fa394ea83f2cced3f947494622e, '', NULL),
(16, 'pbkdf2_sha256$1000000$Wuyn0ko7o7blcIpujwAIGF$j4c692VGw2lyswHF3VTvIxBdI4o/CIR1nYq6Jha8lyk=', NULL, 0, 'Karthikeykoti', 'Karthikey Koti', 'Sir', 'karthikey@gmail.com', 0, 1, '2025-05-07 20:38:24.996379', 'TEACHER', '24SUUIC207', NULL, '', NULL),
(12, 'pbkdf2_sha256$1000000$cHGy8jmydC0yXHfbOPmETk$lwTb0L8ds+da7fFic6ICnd6lQaNfYuDcOy9c3OwZxIg=', '2025-05-26 07:23:52.040355', 0, 'bhargavpoorni', 'Bhargav', 'Sir', 'bhagrav@gmail.com', 0, 1, '2025-05-07 20:13:46.057316', 'TEACHER', '24SUUDSC203', NULL, '', NULL),
(13, 'pbkdf2_sha256$1000000$68C3BsVMTadpTflm3B0O0f$Bt0yqeOaHyXGn8+W224U3x9lSwMNwR1l8aobc9Z9NlU=', NULL, 0, 'niveditamam', 'Nivedita', 'Mam', 'nivedita@gmail.com', 0, 1, '2025-05-07 20:22:15.928793', 'TEACHER', '24SUUDBMS204', NULL, '', NULL),
(14, 'pbkdf2_sha256$1000000$kLgo2CcCAX5GpQkSSha22w$6Abp/wCSFWzdM69S/WFG5JE3ar6Q8d/OrkemdEYE+wk=', NULL, 0, 'mohansir', 'Mohan', 'Sir', 'mohan@gmail.com', 0, 1, '2025-05-07 20:24:12.431164', 'TEACHER', '24SUUOS205', NULL, '', NULL),
(15, 'pbkdf2_sha256$1000000$TCG4pXoEcVIfuoeXNe4rW5$+2FRoWCp7nNJBZcn/NeXv2mTX98gBqwjr/MzGWDI3wo=', NULL, 0, 'amrutaumesh', 'Amruta', 'Mam', 'amruta@gmail.com', 0, 1, '2025-05-07 20:26:21.896579', 'TEACHER', '24SUUQA206', NULL, '', NULL),
(17, 'pbkdf2_sha256$1000000$C7XcUJNoqZGfSd0lkyNSD5$dI11BUFOLWbWw5wSAOH0gOJ62yk1mkdNl62/lIrikU4=', NULL, 0, 'bibekkumarjayswal', 'Bibek', 'Jayswal', 'bibek@gmail.com', 0, 1, '2025-05-07 21:04:57.537430', 'STUDENT', '24SUUBCACS002', NULL, '', NULL),
(18, 'pbkdf2_sha256$1000000$T1ov7aQof1CR7UJuhILLdu$CuVT784D+i6Unh7KylhpB90QVGUvwqzSIDHNL0OkfEo=', '2025-05-26 07:29:14.256983', 0, 'viveksingh', 'vivek', 'singh', 'vivek@gmail.com', 0, 1, '2025-05-26 07:17:27.531657', 'STUDENT', '24SUUBCADS037', 0x8004958c040000000000008c166e756d70792e5f636f72652e6d756c74696172726179948c0c5f7265636f6e7374727563749493948c056e756d7079948c076e6461727261799493944b0085944301629487945294284b014b80859468038c0564747970659493948c02663894898887945294284b038c013c944e4e4e4affffffff4affffffff4b00749462894200040000af0cdcaeaa6be33fc81ad63285dbbc3ff13cd4af7279ed3fa0ae2920a796dc3fcd2e4da9cd13ea3f5b2ca235a925e83ff23df3076107eb3f44633344e762c33f4d717abb697ee63fc03b50f3605f933f108558a78cfdb23ffe599b4531c4ec3f3d2c39ec7126e53f1429cb44409dd73f2cc44ef29b5ecb3f4a4f2a4b3e60db3fb5735d1881b6e13fa7566e2f1273e03faaf77ac05f6ed23f0476bbf1f5e6da3ff9a556c2fee1ee3ffe1362ea098ade3f2848dab240beb53f707330d4957cb03f8df1e564c040e93f208823ebaff3ba3f53aeaddda51cec3fd2cba145f963d23f4d52507eb8dfe33f6f35c796109fe33f10e15bde168bb93fb481c8608cf5e43f8dc3c6cd76e7ee3f0a0b3144bf46e23fb984332bdfa2ed3f16d7005b6771e23f3b6d02f1caf0ed3fbaf89c851cfde33ff1d9ca51eb91e53ff8755aad3de1d73f98c41e1446d7ef3f20ec27bb6d1cdb3f207b8fdf5df0e33f382b475e7e5bbe3f0552d25b126de93fe47867c649d5e43f5219ec46d0c8ec3fed27c1c2a9edec3f5712c1037f07e13f3cde59a93b52d63faeed460abdb7ed3f67017f827666ef3f2722dcbf4a34e63f30b7ddead6edb13f99a75b58014fe73fd4521091e787ef3fd28493f2b277db3f490f7e6dffdaeb3f9464aa97f615da3f9066f4d3cbb9b93f77d9492889d6e33f7e53789aa331de3f003de15fa7f3813f6aaaace1fb20d83ff215f25d5eadd43f44bfa158a304cb3f74689d3b8073ed3f80e84f7b2ab9823ffae8ac8c2a8fe33f11c8b0d6c68ce83f5c6c440c6cefca3ffc9e51c2579fc33ffe1c480aad86db3ffe2b4c31a389d73faf8a81ca23a6ee3f14a2234434a1e73fe810c8e3d61fb93f6a5a25ddd2c8e33fbce156ed5430c03f58908a5c00aac33f00ea314dd5698e3fb43059a9ba39dd3f58d4c33ca646bc3f48f520e537e7e23f58e064f99612c53fb38335491291e93f50c210bb3976af3fdc194a4d5eb6ca3fc899ffc082f5e63fa6ac42d41a27d23fb8db33706250e93f2ce8c6001040d13f30fe6d86212eb33f58ef937baa7fba3f57d9b0c765b3e93f0a6f93f98528d73fa0b14dda36d9a63fbe48170b5540e63f28da37522e54cd3f8a233c821e6ed73f73ac4e49ea2de83fe0793f0f3c71de3f3aa8892ed37ddc3f5465c467df82dc3fd44deb80f37cd13f70f71570e2abda3fc9e9b9e95081e93f93d1f6ae0c6ae73f9147cec51ef6e53f0a2e3674f3c3da3ff47edf671d8fd83f58b0786f721bbe3f80b8cfad52b57e3f2b95d2d17e28ed3f9b745990c79bec3f33a632f2e215ed3f804a8ca50da8db3f5405e0e8db09cd3f829ced545b20d43fb00370e154bcdf3ff87c7a6743ecbd3ff4bc5968ba9bd23f7be13c41c455ee3fabc1c48fd659e43f60cc0809a018c23fd46392a0f0fcc83ff5de7651293fe03f90ba6a7491b3b33f947494622e, '', '9926017870');

-- --------------------------------------------------------

--
-- Table structure for table `users_customuser_groups`
--

DROP TABLE IF EXISTS `users_customuser_groups`;
CREATE TABLE IF NOT EXISTS `users_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_customuser_groups_customuser_id_group_id_76b619e3_uniq` (`customuser_id`,`group_id`),
  KEY `users_customuser_groups_customuser_id_958147bf` (`customuser_id`),
  KEY `users_customuser_groups_group_id_01390b14` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users_customuser_user_permissions`
--

DROP TABLE IF EXISTS `users_customuser_user_permissions`;
CREATE TABLE IF NOT EXISTS `users_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq` (`customuser_id`,`permission_id`),
  KEY `users_customuser_user_permissions_customuser_id_5771478b` (`customuser_id`),
  KEY `users_customuser_user_permissions_permission_id_baaa2f74` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
