delete from smarthomes.tb_message_twoway where userid in (select userid from smarthomes.tb_usermst  where  userid > 100000);
delete from smarthomes.tb_maillog where userid in (select userid from smarthomes.tb_usermst where   userid > 100000);
delete from smarthomes.tb_userotpmap where userid in (select userid from smarthomes.tb_usermst where  userid > 100000);
delete from  smarthomes.tb_usernotificationmap where userid in (select userid from smarthomes.tb_usermst where  userid > 100000);
delete from smarthomes.tb_usermst  where  userid > 100000;


INSERT INTO smarthomes.tb_usermst VALUES (100022, 1, 'qn6UiljSsSBM+B8mHOHIsDj18NW1pxreS8FsfuIrPVQ=', NULL, NULL, 'qn6UiljSsSBM+B8mHOHIsDj18NW1pxreS8FsfuIrPVQ=', NULL, 'z/m6Jxswmfs9eOntPNyE/8lARQT20J8ZLXPZgmSbDtc=', 0, 0, 0, NULL, NULL, '2106-04-09 09:26:32.509264', 1, '2106-04-09 09:26:32.509264', 'ReXpsN?!k{&!AT+%R[4*/w6tFnngb]&nUqPnN&1FLl(z08tOpu?vznSsFveQV^)G', '2016-04-30 09:26:32.509264', NULL, 100022, '2016-04-30 09:26:32.509264', '2016-04-30 09:26:32.509264', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

INSERT INTO smarthomes.tb_maillog VALUES (23, 23, 100022, 0, 'CONNECT@SECURETOGETHER.COM', NULL, 'Welcome to BeanBag System for Homes.

602732 is your verification code for registration. Treat this as confidential.
Please enter given verification code in Beanbag App to activate your account. 

This is a system generated mail,Please do not reply to it. In case of any problem contact: xyz@securetogether.com', 'Welcome to BeanBag System for Homes', '2016-04-30 09:26:32.830775', NULL, 101);


INSERT INTO smarthomes.tb_userotpmap VALUES (23, 100022, 23, '602732', '2016-04-30 09:26:32.837348', '2016-05-01 09:26:32.837348', 0, 6101, 0, 0);


INSERT INTO smarthomes.tb_message_twoway VALUES (23, NULL, 986796921, 'register', 100022, NULL, NULL, 0, '2016-04-30 09:26:32.509264');
