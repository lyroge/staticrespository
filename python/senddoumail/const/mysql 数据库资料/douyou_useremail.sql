/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50508
Source Host           : localhost:3306
Source Database       : douban_caiji

Target Server Type    : MYSQL
Target Server Version : 50508
File Encoding         : 65001

Date: 2013-10-13 12:45:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `douyou_useremail`
-- ----------------------------
DROP TABLE IF EXISTS `douyou_useremail`;
CREATE TABLE `douyou_useremail` (
  `id` int(11) NOT NULL,
  `user` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `ip` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of douyou_useremail
-- ----------------------------
INSERT INTO `douyou_useremail` VALUES ('0', 'douyouone@163.com', 'douyou147852', null);
INSERT INTO `douyou_useremail` VALUES ('1', 'douyouone@163.com', 'douyou147852', null);
INSERT INTO `douyou_useremail` VALUES ('2', 'douyouthree@163.com', 'douyou147852', null);
