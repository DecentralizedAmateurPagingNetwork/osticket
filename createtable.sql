CREATE TABLE IF NOT EXISTS `notifications` (
  `id` int(11) unsigned NOT NULL,
  `firstname` varchar(32) DEFAULT NULL,
  `assignedusername` varchar(32) DEFAULT NULL,
  `staff_id` int(11) unsigned NOT NULL,
  `state` enum('created','closed','reopened','assigned','transferred','overdue','edited','viewed','error','collab','resent') NOT NULL,
  `username` varchar(128) NOT NULL,
  `data` varchar(1024) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `uid` int(11) unsigned DEFAULT NULL,
  `uid_type` char(1) NOT NULL,
  `subject` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
