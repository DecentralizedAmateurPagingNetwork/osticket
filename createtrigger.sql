DELIMITER //
CREATE TRIGGER `notifications` AFTER INSERT ON `ost_thread_event`
 FOR EACH ROW INSERT INTO `notifications`
SELECT 
	`ost_thread_event`.`id`,
	`ost_staff`.`firstname`,
	`ost_staff`.`username` AS `assignedusername`,
	`ost_thread_event`.`staff_id`,
	`ost_thread_event`.`state`,
	`ost_thread_event`.`username`,
	`ost_thread_event`.`data`,
	`ost_thread_event`.`timestamp`,
	`ost_thread_event`.`uid`,
	`ost_thread_event`.`uid_type`,
	`ost_ticket__cdata`.`subject`
FROM `ost_thread_event`
LEFT JOIN `ost_staff`
ON `ost_thread_event`.`staff_id`=`ost_staff`.`staff_id`
LEFT JOIN `ost_ticket__cdata`
ON `ost_thread_event`.`thread_id`=`ost_ticket__cdata`.`ticket_id`
ORDER BY `ost_thread_event`.`id` DESC
LIMIT 1
//
DELIMITER ;
