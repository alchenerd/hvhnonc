BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS `hvhnonc_places` (
	`ID`	INTEGER,
	`description`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(`ID`)
);


CREATE TABLE IF NOT EXISTS `hvhnonc_users` (
	`ID`	INTEGER,
	`username`	TEXT NOT NULL UNIQUE,
	`hash_SHA256`	TEXT NOT NULL,
	`salt`	TEXT NOT NULL,
	PRIMARY KEY(`ID`)
);


INSERT OR IGNORE INTO `hvhnonc_users` (ID,username,hash_SHA256,salt) 
VALUES (1,'administrator','a5d4b16f5d9374c2570a8d970fcad6b427c0c77364696dfadb91ebe8dad52a31','ae97c3df19a860c906fdf00d67ef8781');


CREATE TABLE IF NOT EXISTS `hvhnonc_unit` (
	`ID`	INTEGER,
	`description`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(`ID`)
);


CREATE TABLE IF NOT EXISTS `hvhnonc_subcategory` (
	`parent_ID`	INTEGER,
	`ID`	INTEGER,
	`description`	INTEGER NOT NULL UNIQUE,
	FOREIGN KEY(`parent_ID`) REFERENCES `hvhnonc_category`(`ID`) on update cascade on delete set null,
	PRIMARY KEY(`parent_ID`,`ID`)
);


CREATE TABLE IF NOT EXISTS `hvhnonc_out` (
	`ID`	INTEGER,
	`in_ID`	INTEGER,
	`object_ID`	TEXT,
	`serial_ID`	TEXT,
	`category`	TEXT NOT NULL,
	`subcategory`	TEXT NOT NULL,
	`name`	TEXT NOT NULL,
	`brand`	TEXT,
	`spec`	TEXT,
	`unit`	TEXT NOT NULL DEFAULT '個',
	`out_date`	TEXT NOT NULL,
	`price`	INTEGER NOT NULL,
	`amount`	INTEGER NOT NULL CHECK(amount > 0),
	`storage`	TEXT,
	`reason`	TEXT,
	`post_treatment`	TEXT,
	`remark`	TEXT,
	PRIMARY KEY(`ID`),
	FOREIGN KEY(`in_ID`) REFERENCES `hvhnonc_in`(`ID`) on delete set null,
	FOREIGN KEY(`category`) REFERENCES `hvhnonc_category`(`description`) on update cascade on delete set null,
	FOREIGN KEY(`subcategory`) REFERENCES `hvhnonc_subcategory`(`description`) on update cascade on delete set null
);

CREATE TABLE IF NOT EXISTS `hvhnonc_in` (
	`ID`	INTEGER,
	`object_ID`	TEXT NOT NULL,
	`serial_ID`	TEXT NOT NULL,
	`category`	TEXT NOT NULL,
	`subcategory`	TEXT NOT NULL,
	`name`	TEXT NOT NULL,
	`brand`	TEXT,
	`spec`	TEXT,
	`unit`	TEXT NOT NULL DEFAULT '個',
	`purchase_date`	TEXT NOT NULL,
	`acquire_date`	TEXT NOT NULL,
	`price`	INTEGER NOT NULL,
	`amount`	INTEGER CHECK(amount > 0),
	`place`	TEXT NOT NULL,
	`keep_year`	INTEGER NOT NULL,
	`source`	TEXT DEFAULT '購置' CHECK(source in ( '購置' , '撥用' , '贈送' )),
	`keep_department`	TEXT NOT NULL,
	`use_department`	TEXT,
	`keeper`	TEXT,
	`remark`	TEXT,
	PRIMARY KEY(`ID`),
	FOREIGN KEY(`category`) REFERENCES `hvhnonc_category`(`description`) on update cascade on delete set null,
	FOREIGN KEY(`subcategory`) REFERENCES `hvhnonc_subcategory`(`description`) on update cascade on delete set null
);

CREATE TABLE IF NOT EXISTS `hvhnonc_department` (
	`ID`	INTEGER,
	`description`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(`ID`)
);


CREATE TABLE IF NOT EXISTS `hvhnonc_category` (
	`ID`	INTEGER,
	`description`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(`ID`)
);


CREATE TABLE IF NOT EXISTS `hvhnonc_in_cache` (
	`this_ID`	INTEGER NOT NULL DEFAULT 0,
	`this_value`	TEXT NOT NULL DEFAULT 'none',
	`change_ID`	INTEGER NOT NULL,
	`change_value`	TEXT NOT NULL, 
	PRIMARY KEY(`this_ID`, `this_value`, `change_ID`, `change_value`),
	FOREIGN KEY(`this_ID`) REFERENCES `hvhnonc_fields`(`ID`) on update cascade on delete cascade
);


CREATE TABLE IF NOT EXISTS `hvhnonc_out_cache` (
	`this_ID`	INTEGER NOT NULL DEFAULT 0,
	`this_value`	TEXT NOT NULL DEFAULT 'none',
	`change_ID`	INTEGER NOT NULL,
	`change_value`	TEXT NOT NULL,
	PRIMARY KEY(`this_ID`, `this_value`, `change_ID`, `change_value`), 
	FOREIGN KEY(`this_ID`) REFERENCES `hvhnonc_fields`(`ID`) on update cascade on delete cascade
);


CREATE TABLE IF NOT EXISTS `hvhnonc_fields` (
	`ID`	INTEGER,
	`description`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(`ID`)
);

INSERT OR IGNORE INTO `hvhnonc_category` VALUES (1, '事務用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (2, '衛生用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (3, '炊事用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (4, '餐飲用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (5, '被服用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (6, '防護用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (7, '陳設用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (8, '康樂用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (9, '手工用具');
INSERT OR IGNORE INTO `hvhnonc_category` VALUES (10, '醫療用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 1, '文書用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 2, '複印用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 3, '記數用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 4, '劃線用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 5, '釘裝用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 6, '傳音用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 7, '放置用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 8, '供水用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 9, '照明用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 10, '遮蔽用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 11, '竹製用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 12, '電器用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 13, '化驗用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (1, 14, '什項用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (2, 1, '清潔用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (2, 2, '盥洗用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (2, 3, '洗燙用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (2, 4, '美容用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (3, 1, '爐灶用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (3, 2, '調製用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (3, 3, '炊蒸用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (4, 1, '盛裝用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (4, 2, '飲食用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (5, 1, '舖蓋用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (5, 2, '穿著用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (5, 3, '防雨用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (6, 1, '消防用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (6, 2, '救生用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (6, 3, '防空用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (6, 4, '警勤用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (6, 5, '戒護用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (6, 6, '工業安全用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (7, 1, '陳飾用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (7, 2, '陳列用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (7, 3, '裝潢用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (7, 4, '儲存用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (8, 1, '音樂用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (8, 2, '運動用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (8, 3, '電影用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (8, 4, '戲劇用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (8, 5, '攝影用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 1, '農工用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 2, '木工用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 3, '鐵工用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 4, '泥水工用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 5, '起重用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 6, '修車用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 7, '臺面劃線用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (9, 8, '度量用具');

INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 1, '護理用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 2, '調劑用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 3, '內科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 4, '外科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 5, '婦產科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 6, '耳鼻喉科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 7, '泌尿科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 8, '眼科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 9, '牙科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 10, '放射科用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 11, '檢驗用具');
INSERT OR IGNORE INTO `hvhnonc_subcategory` VALUES (10, 12, '獸醫用具');

INSERT OR IGNORE INTO `hvhnonc_department` (description) VALUES ('秘書室');
INSERT OR IGNORE INTO `hvhnonc_department` (description) VALUES ('輔導室');
INSERT OR IGNORE INTO `hvhnonc_department` (description) VALUES ('保健組');

INSERT OR IGNORE INTO `hvhnonc_fields` (`ID`, `description`) VALUES (0, '無');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('物品大項');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('物品細目');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('物品名稱');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('單位');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('品牌');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('規格');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('物品編號');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('流水號');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('購置日期_年');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('購置日期_月');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('購置日期_日');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('建帳日期_年');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('建帳日期_月');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('建帳日期_日');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('來源');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('價格');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('數量');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('存置地點');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('保管年限');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('保管單位');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('使用單位');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('保管人');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('備註事項');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('檢索');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('除帳原因');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('繳存地點');
INSERT OR IGNORE INTO `hvhnonc_fields` (`description`) VALUES ('除帳備註');

COMMIT;
