/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50508
Source Host           : localhost:3306
Source Database       : douban_caiji

Target Server Type    : MYSQL
Target Server Version : 50508
File Encoding         : 65001

Date: 2013-10-13 12:43:51
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `douyou_content`
-- ----------------------------
DROP TABLE IF EXISTS `douyou_content`;
CREATE TABLE `douyou_content` (
  `content_id` int(10) NOT NULL,
  `content` text CHARACTER SET utf8,
  PRIMARY KEY (`content_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of douyou_content
-- ----------------------------
INSERT INTO `douyou_content` VALUES ('1', '邀请100位不曾丢失书店梦想的朋友，2014年，一起开家独立书店！  http://www.douban.com/event/19940346/');
