create database ReviewDatas;
use ReviewDatas;
drop database ReviewDatas;

CREATE TABLE jd_mdcomments(
Id  int not null,
已采 varchar(5),
已发 varchar(5),
电商平台 varchar(4),
品牌 varchar(4)not null,
评论 text not null,
时间 timestamp not NULL,
型号 text not null,
PageUrl varchar(120)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

select *from jd_mdcomments;

CREATE TABLE jd_mdcomments(
id  int not null auto_increment primary key,
user varchar(20),
productname varchar(100),
productxh varchar(50),
mdcomment text not null ,
ordertime timestamp not NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;