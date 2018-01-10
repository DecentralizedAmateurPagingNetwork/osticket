# Extensions for osTicket for DAPNET use

Main idea: Get a notification on the POCSAG receiver via DAPNET, if a ticket is created, assigned or close.

* Add a mysql table to combine the needed data. Data insert into this table via mysql trigger.
* Pyhton script run via cron to read new table and generate paging calls 
