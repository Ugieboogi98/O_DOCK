-- Figure Archive AI: restore into a new empty PostgreSQL database.
BEGIN;
SET standard_conforming_strings = on;

CREATE TABLE collection_jobs (
	id SERIAL NOT NULL, 
	collector VARCHAR(120) NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	started_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	ended_at TIMESTAMP WITH TIME ZONE, 
	count INTEGER NOT NULL, 
	error_summary TEXT, 
	PRIMARY KEY (id)
)

;
INSERT INTO "collection_jobs" ("id","collector","status","started_at","ended_at","count","error_summary") VALUES (1,'bundled_official_metadata','completed','2026-10-21T12:07:06.050880+08:00','2026-10-21T12:07:06.050337+08:00',114,NULL);
SELECT setval(pg_get_serial_sequence('collection_jobs','id'), (SELECT MAX(id) FROM collection_jobs), true);

CREATE TABLE manufacturers (
	id SERIAL NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	name_ko VARCHAR(120) NOT NULL, 
	official_url TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)

;
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (1,'FuRyu','후류','https://furyu-hm.com/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (2,'Bandai Spirits','반다이 스피리츠','https://www.bandaispirits.co.jp/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (3,'MegaHouse','메가하우스','https://megahobby.jp/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (4,'Good Smile Company','굿스마일 컴퍼니','https://www.goodsmile.com/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (5,'SEGA','세가','https://segaplaza.jp/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (6,'Kotobukiya','코토부키야','https://www.kotobukiya.co.jp/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (7,'TAITO','타이토','https://www.taito.co.jp/');
INSERT INTO "manufacturers" ("id","name","name_ko","official_url") VALUES (8,'Hot Toys','핫토이','https://www.hottoys.jp/');
SELECT setval(pg_get_serial_sequence('manufacturers','id'), (SELECT MAX(id) FROM manufacturers), true);

CREATE TABLE retailers (
	id SERIAL NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	site_url TEXT NOT NULL, 
	seller_type VARCHAR(60) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)

;
INSERT INTO "retailers" ("id","name","site_url","seller_type") VALUES (1,'매니아하우스','https://www.maniahouse.co.kr','unverified');
INSERT INTO "retailers" ("id","name","site_url","seller_type") VALUES (2,'히어로타임','https://www.herotime.co.kr','unverified');
INSERT INTO "retailers" ("id","name","site_url","seller_type") VALUES (3,'피규어팜','https://www.figurefarm.net','unverified');
INSERT INTO "retailers" ("id","name","site_url","seller_type") VALUES (4,'코믹스아트','https://www.comics-art.co.kr','unverified');
SELECT setval(pg_get_serial_sequence('retailers','id'), (SELECT MAX(id) FROM retailers), true);

CREATE TABLE used_marketplaces (
	id SERIAL NOT NULL, 
	name VARCHAR(80) NOT NULL, 
	url TEXT NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)

;
INSERT INTO "used_marketplaces" ("id","name","url","currency") VALUES (1,'메루카리','https://jp.mercari.com/','JPY');
INSERT INTO "used_marketplaces" ("id","name","url","currency") VALUES (2,'중고나라','https://web.joongna.com/','KRW');
INSERT INTO "used_marketplaces" ("id","name","url","currency") VALUES (3,'번개장터','https://m.bunjang.co.kr/','KRW');
INSERT INTO "used_marketplaces" ("id","name","url","currency") VALUES (4,'당근','https://www.daangn.com/','KRW');
SELECT setval(pg_get_serial_sequence('used_marketplaces','id'), (SELECT MAX(id) FROM used_marketplaces), true);

CREATE TABLE product_lines (
	id SERIAL NOT NULL, 
	manufacturer_id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (manufacturer_id, name), 
	FOREIGN KEY(manufacturer_id) REFERENCES manufacturers (id)
)

;
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (1,6,'MEGAMI DEVICE');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (2,6,'M.S.G Modeling Support Goods');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (3,6,'Atelier Yumia: The Alchemist of Memories & the Envisioned Land');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (4,6,'SADAKO');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (5,6,'ARMORED CORE');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (6,6,'MEGA MAN');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (7,6,'Legend of the Galactic Heroes');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (8,6,'HEXA GEAR');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (9,6,'Evangelion: New Theatrical Edition');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (10,6,'Magic Repo Man : Dumped by My Party, I’ll Cash In With a Cute Support Fairy to Become the Strongest!');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (11,6,'ZOIDS');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (12,6,'FRAME ARMS GIRL');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (13,6,'Sasaki and Peeps');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (14,6,'Brave Exkaiser');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (15,6,'Magic Knight Rayearth');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (16,6,'MEGALOMARIA UNLIMITED UNIVERSE');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (17,6,'銀河特急 ミルキー☆サブウェイ');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (18,6,'FRAME ARMS');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (19,6,'ARCANADEA');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (20,3,'Look Up');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (21,3,'G.E.M.');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (22,1,'TENITOL');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (23,1,'F:NEX');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (24,4,'Nendoroid');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (25,2,'S.H.Figuarts');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (26,5,'Luminasta');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (27,7,'Coreful');
INSERT INTO "product_lines" ("id","manufacturer_id","name") VALUES (28,8,'Video Game Masterpiece');
SELECT setval(pg_get_serial_sequence('product_lines','id'), (SELECT MAX(id) FROM product_lines), true);

CREATE TABLE seller_verifications (
	id SERIAL NOT NULL, 
	retailer_id INTEGER NOT NULL, 
	verification_type VARCHAR(60) NOT NULL, 
	evidence_url TEXT NOT NULL, 
	verified_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(retailer_id) REFERENCES retailers (id)
)

;

CREATE TABLE figures (
	id SERIAL NOT NULL, 
	manufacturer_id INTEGER NOT NULL, 
	product_line_id INTEGER, 
	name_original TEXT NOT NULL, 
	name_ko TEXT, 
	franchise TEXT, 
	character TEXT, 
	type VARCHAR(60) NOT NULL, 
	scale VARCHAR(40), 
	height_mm INTEGER, 
	material VARCHAR(200), 
	official_url TEXT NOT NULL, 
	collected_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	quality VARCHAR(40) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(manufacturer_id) REFERENCES manufacturers (id), 
	FOREIGN KEY(product_line_id) REFERENCES product_lines (id), 
	UNIQUE (official_url)
)

;
CREATE INDEX ix_figures_manufacturer_id ON figures (manufacturer_id);
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (1,6,1,'PUNI☆MOFU RACING XIAO with Honda Z50J Gorilla',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054087327/','2026-10-21T11:32:22.273302+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (2,6,2,'HEAVY WEAPON UNIT 77 ACTIVE BOOSTER',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054083886/','2026-10-21T11:32:22.273336+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (3,6,3,'Yumia Liessfeldt Sun Shower Ver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054070602/','2026-10-21T11:32:22.273554+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (4,6,4,'SADAKO BISHOUJO STATUE',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054098590/','2026-10-21T11:32:22.273559+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (5,6,5,'MIRAGE C02-URANUS',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054083251/','2026-10-21T11:32:22.273564+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (6,6,6,'BLUES',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054093892/','2026-10-21T11:32:22.273567+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (7,6,6,'ROCKMAN',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054093878/','2026-10-21T11:32:22.273570+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (8,6,7,'Free Planets Alliance 13th Fleet Flagship Hyperion',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054063635/','2026-10-21T11:32:22.273573+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (9,6,8,'V-THOR',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054057979/','2026-10-21T11:32:22.273576+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (10,6,9,'EVANGELION 13 Awake Ver.',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054026708/','2026-10-21T11:32:22.273579+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (11,6,10,'Empee',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054084869/','2026-10-21T11:32:22.273581+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (12,6,11,'D-STYLE IRONKONG  ［Clear Parts Append］',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054096985/','2026-10-21T11:32:22.273585+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (13,6,12,'DURGA I DARKNESS QUEEN Ver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054082131/','2026-10-21T11:32:22.273589+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (14,6,13,'ELSA',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054062416/','2026-10-21T11:32:22.273597+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (15,6,11,'D-STYLE DEATH SAURER',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054097036/','2026-10-21T11:32:22.273601+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (16,6,14,'GREAT EXKIZER FULL EDITION',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054088782/','2026-10-21T11:32:22.273763+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (17,6,1,'BUSTER DOLL PALADIN',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054098002/','2026-10-21T11:32:22.273767+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (18,6,1,'BUSTER DOLL TANK',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054097999/','2026-10-21T11:32:22.273770+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (19,6,15,'Hikaru Shidou',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054076413/','2026-10-21T11:32:22.273772+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (20,6,16,'SANA AKABISHI【DRESS CODE】',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054081745/','2026-10-21T11:32:22.273775+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (21,6,16,'METAMORPHOSE UNIT PHLEGETHON',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054098279/','2026-10-21T11:32:22.273778+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (22,6,16,'METAMORPHOSE UNIT CRIMINAL BUSTER',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054089505/','2026-10-21T11:32:22.273782+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (23,6,17,'MAKINA',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054087334/','2026-10-21T11:32:22.273785+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (24,6,2,'HEAVY WEAPON UNIT78 CUSTOMIZE CORE WING BLADE',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054083893/','2026-10-21T11:32:22.273788+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (25,6,8,'V-THOR Assault Type "Ji rei" (Swift Thunder)',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054087594/','2026-10-21T11:32:22.273791+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (26,6,18,'LX-00 RAY FALX:RE2',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054066261/','2026-10-21T11:32:22.273794+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (27,6,11,'MV-02 FINE & ZEKE',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4904810098799/','2026-10-21T11:32:22.273797+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (28,6,1,'PUNI☆MOFU RACING LANG with Honda Z50J Gorilla',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054087310/','2026-10-21T11:32:22.273800+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (29,6,5,'CREST CR-C75U2 DELTA Ver.',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054088713/','2026-10-21T11:32:22.273803+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (30,6,19,'YUKUMO',NULL,NULL,NULL,'model_kit',NULL,NULL,NULL,'https://www.kotobukiya.co.jp/en/product/detail/p4934054097616/','2026-10-21T11:32:22.273806+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (31,3,20,'るかっぷ 刀剣乱舞ONLINE 山姥切国広',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6115/','2026-10-21T11:32:22.273808+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (32,3,20,'るかっぷ 刀剣乱舞ONLINE 山姥切長義',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6114/','2026-10-21T11:32:22.273812+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (33,3,20,'るかっぷ 転生したらスライムだった件 リムル=テンペスト',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6125/','2026-10-21T11:32:22.273815+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (34,3,20,'るかっぷ 転生したらスライムだった件 ディアブロ',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6124/','2026-10-21T11:32:22.273819+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (35,3,20,'るかっぷ アオのハコ 鹿野千夏',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6123/','2026-10-21T11:32:22.273822+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (36,3,20,'るかっぷ 超かぐや姫！ 月見ヤチヨ',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6122/','2026-10-21T11:32:22.273845+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (37,3,20,'るかっぷ NARUTO-ナルト- 疾風伝 奈良シカマル にこっとver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6121/','2026-10-21T11:32:22.273850+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (38,3,20,'るかっぷ NARUTO-ナルト- 疾風伝 我愛羅 にこっとver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6120/','2026-10-21T11:32:22.273854+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (39,3,20,'るかっぷ TVアニメ『BLEACH』 ウルキオラ・シファー',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6119/','2026-10-21T11:32:22.273859+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (40,3,20,'るかっぷ TVアニメ『BLEACH』 グリムジョー・ジャガージャック',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6118/','2026-10-21T11:32:22.273863+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (41,3,20,'るかっぷ 鬼滅の刃 獪岳',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6117/','2026-10-21T11:32:22.273867+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (42,3,20,'るかっぷ 鬼滅の刃 我妻善逸 むん！ver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6116/','2026-10-21T11:32:22.273870+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (43,3,21,'G.E.M.シリーズ NARUTO-ナルト- 疾風伝 てのひらミナト',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6044/','2026-10-21T11:32:22.273873+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (44,3,21,'G.E.M.シリーズ 鬼滅の刃 てのひらしのぶさん【再販】',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/5941/','2026-10-21T11:32:22.273876+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (45,3,21,'G.E.M.シリーズ 文豪ストレイドッグス てのひら太宰さん',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/6045/','2026-10-21T11:32:22.273898+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (46,3,21,'G.E.M.シリーズ 進撃の巨人 てのひらエレン',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/5958/','2026-10-21T11:32:22.273901+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (47,3,21,'G.E.M.シリーズ 進撃の巨人 てのひらリヴァイ兵士長',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://megahobby.jp/products/item/5957/','2026-10-21T11:32:22.273904+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (48,1,22,'TENITOL 魔王ちゃん [mini]',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-pdrgvfdk','2026-10-21T11:32:22.273907+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (49,1,22,'TENITOL ヴェルジュ(バニー) [mini]',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-g6ou28xc','2026-10-21T11:32:22.273910+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (50,1,22,'TENITOL ヴェルナー(バニー) [mini]',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-76b3a42i','2026-10-21T11:32:22.273913+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (51,1,22,'TENITOL TALL フリーレン クラシカルワンピースver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-zua4ajhp','2026-10-21T11:32:22.273915+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (52,1,22,'TENITOL TALL フェルン クラシカルワンピースver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-b4hj45rl','2026-10-21T11:32:22.273931+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (53,1,23,'Nachoneko Birthday ver. 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-sdk3vil3','2026-10-21T11:32:22.273934+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (54,1,22,'TENITOL TALL 鹿目まどか&暁美ほむら スペシャルセット',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-7dckkixl','2026-10-21T11:32:22.273937+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (55,1,22,'TENITOL TALL 鹿目まどか',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-5mey8dnc','2026-10-21T11:32:22.273940+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (56,1,22,'TENITOL TALL 暁美ほむら',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-8l8kty5p','2026-10-21T11:32:22.273945+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (57,1,22,'TENITOL フリーレン[petit]',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-2boxqwvy','2026-10-21T11:32:22.273947+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (58,1,22,'TENITOL TALL 椎名真昼 Winter clothes ver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-tw74jsdd','2026-10-21T11:32:22.273949+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (59,1,22,'TENITOL TALL 白 水着ドレスver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-jjld9ls','2026-10-21T11:32:22.273952+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (60,1,23,'周防パトラ バニーver. 1/6スケールフィギュア',NULL,NULL,NULL,'figure','1/6',NULL,NULL,'https://furyu-hm.com/products/fnx-6ukfptbj','2026-10-21T11:32:22.273954+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (61,1,23,'しぐれうい “Wishing Umbrella” 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-otf2ucmj','2026-10-21T11:32:22.273956+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (62,1,23,'フリーレン フォトフレームフィギュア',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/fnx-cyv366r3','2026-10-21T11:32:22.273959+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (63,1,23,'D：キラーワイフ - シークレットポリス 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-ijix7fvh','2026-10-21T11:32:22.273981+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (64,1,23,'ウンファ：タクティカル・アップ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-y6lveiog','2026-10-21T11:32:22.274045+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (65,1,23,'エクス・アルビオ  1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-xx6e5hvu','2026-10-21T11:32:22.274048+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (66,1,23,'でびでび・でびる 1/2スケールソフビフィギュア',NULL,NULL,NULL,'figure','1/2',NULL,NULL,'https://furyu-hm.com/products/fnx-ffj4xo67','2026-10-21T11:32:22.274051+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (67,1,23,'加賀美ハヤト 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-gvbar3ab','2026-10-21T11:32:22.274053+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (68,1,23,'不破湊  1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-5pdxfzyr','2026-10-21T11:32:22.274056+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (69,1,23,'レイン・パターソン  1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-umij6sfl','2026-10-21T11:32:22.274058+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (70,1,23,'花畑チャイカ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-uyw3vcpy','2026-10-21T11:32:22.274075+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (71,1,23,'叢雲カゲツ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-l223w3yb','2026-10-21T11:32:22.274077+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (72,1,23,'常守 朱＆狡噛 慎也 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-t2yqzufv','2026-10-21T11:32:22.274080+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (73,1,23,'吉徳×F:NEX 桜ミク -日本人形- 1/4スケールフィギュア',NULL,NULL,NULL,'figure','1/4',NULL,NULL,'https://furyu-hm.com/products/fnx-f2hvus68','2026-10-21T11:32:22.274082+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (74,1,23,'エリ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-xmfsokp','2026-10-21T11:32:22.274085+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (75,1,23,'牧瀬紅莉栖＆岡部倫太郎 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-l8esnsk4','2026-10-21T11:32:22.274088+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (76,1,23,'ディーゼル - ミッドナイト・ストロベリー 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-dzv65oov','2026-10-21T11:32:22.274090+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (77,1,23,'久世しずか&雲母坂まりな 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-js9sg8wl','2026-10-21T11:32:22.274093+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (78,1,23,'ベルベット 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-u89oyls','2026-10-21T11:32:22.274095+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (79,1,23,'吉徳×F:NEX A2 -日本人形-1/4スケールフィギュア',NULL,NULL,NULL,'figure','1/4',NULL,NULL,'https://furyu-hm.com/products/fnx-lxn773cl','2026-10-21T11:32:22.274098+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (80,1,23,'七海千秋 illustration by めつぶしあんこ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-38x5ij3z','2026-10-21T11:32:22.274100+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (81,1,23,'霧切響子 illustration by めつぶしあんこ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-64rr4p2x','2026-10-21T11:32:22.274102+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (82,1,23,'楪いのり 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-kmfaju93','2026-10-21T11:32:22.274105+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (83,1,23,'雪ノ下雪乃 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-mso9ai4','2026-10-21T11:32:22.274108+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (84,1,23,'由比ヶ浜結衣 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-ls0faj9a','2026-10-21T11:32:22.274110+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (85,1,23,'一色いろは 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-masiut8q','2026-10-21T11:32:22.274112+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (86,1,23,'小木曽雪菜 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-dpwjgci3','2026-10-21T11:32:22.274114+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (87,1,23,'冬馬かずさ 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-ycppgzdc3','2026-10-21T11:32:22.274116+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (88,1,23,'ロキシー・ミグルディア・グレイラット マントver. 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-nsif54iq','2026-10-21T11:32:22.274118+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (89,1,23,'ファム・スール 1/7スケールフィギュア',NULL,NULL,NULL,'figure','1/7',NULL,NULL,'https://furyu-hm.com/products/fnx-kxbc2838','2026-10-21T11:32:22.274121+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (90,1,22,'TENITOL TALL ロキシー・ミグルディア・グレイラット',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-kro74nqz','2026-10-21T11:32:22.274123+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (91,1,22,'TENITOL TALL イヅツミクラシカルメイドスタイルver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-vo5xu6lc','2026-10-21T11:32:22.274126+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (92,1,23,'ファリン(キメラ) ドレススタイルver. ノンスケールフィギュア',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/fnx-qd8wqon7','2026-10-21T11:32:22.274128+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (93,1,22,'TENITOL TALL レーシングミク 2026 いいね！Ver.',NULL,NULL,NULL,'figure',NULL,NULL,NULL,'https://furyu-hm.com/products/tnl-pf4zuw8h','2026-10-21T11:32:22.274130+08:00','catalog_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (94,4,24,'Nendoroid Hyakkimaru',NULL,'Dororo',NULL,'figure',NULL,100,'PVC / ABS','https://www.goodsmile.com/en/product/6143','2026-10-21T11:32:22.274135+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (95,4,24,'Nendoroid Blake Belladonna',NULL,'RWBY',NULL,'figure',NULL,100,'PVC / ABS','https://www.goodsmile.com/en/product/8370','2026-10-21T11:32:22.274141+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (96,4,24,'Nendoroid Vanilla',NULL,'NEKOPARA',NULL,'figure',NULL,100,'PVC / ABS','https://www.goodsmile.com/en/product/6761','2026-10-21T11:32:22.274202+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (97,4,24,'Nendoroid Gon Freecss',NULL,'HUNTER x HUNTER',NULL,'figure',NULL,100,NULL,'https://www.goodsmile.com/en/product/6357','2026-10-21T11:32:22.274206+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (98,4,24,'Nendoroid Ireena',NULL,'The Greatest Demon Lord Is Reborn as a Typical Nobody',NULL,'figure',NULL,100,NULL,'https://www.goodsmile.com/en/product/11488','2026-10-21T11:32:22.274208+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (99,4,24,'Nendoroid Mimic',NULL,'Frieren: Beyond Journey''s End',NULL,'figure',NULL,NULL,NULL,'https://www.goodsmile.com/en/product/60956','2026-10-21T11:32:22.274211+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (100,4,24,'Nendoroid Mai Sakurajima',NULL,'Rascal Does Not Dream of Bunny Girl Senpai',NULL,'figure',NULL,100,'PVC / ABS','https://www.goodsmile.com/en/product/6029','2026-10-21T11:32:22.274213+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (101,4,24,'Nendoroid Woosa',NULL,'Black Desert',NULL,'figure',NULL,100,NULL,'https://www.goodsmile.com/en/product/1141000','2026-10-21T11:32:22.274216+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (102,4,24,'Nendoroid Kurisu Makise: Lab Coat Ver. [Basic]',NULL,'STEINS;GATE',NULL,'figure',NULL,100,NULL,'https://www.goodsmile.com/en/product/1142378','2026-10-21T11:32:22.274218+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (103,2,25,'フリーレン','S.H.Figuarts 프리렌','葬送のフリーレン','フリーレン','figure',NULL,120,'PVC / ABS','https://tamashiiweb.com/item/14690/','2026-10-21T11:32:22.274220+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (104,2,25,'フェルン','S.H.Figuarts 페른','葬送のフリーレン','フェルン','figure',NULL,NULL,NULL,'https://tamashiiweb.com/item/14735/','2026-10-21T11:32:22.274229+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (105,2,25,'ヒンメル','S.H.Figuarts 힘멜','葬送のフリーレン','ヒンメル','figure',NULL,NULL,NULL,'https://tamashiiweb.com/item/15747/','2026-10-21T11:32:22.274235+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (106,5,26,'葬送のフリーレン Luminasta “フリーレン” ~葬送のフリーレン~',NULL,'葬送のフリーレン','フリーレン','figure',NULL,NULL,NULL,'https://segaplaza.jp/prize/D121425/','2026-10-21T11:32:22.274245+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (107,5,26,'葬送のフリーレン Luminasta “フリーレン” ~インミミック~',NULL,'葬送のフリーレン','フリーレン','figure',NULL,NULL,NULL,'https://segaplaza.jp/prize/D122835/','2026-10-21T11:32:22.274340+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (108,5,26,'葬送のフリーレン Luminasta “フリーレン” ~SUMMER DRESS~',NULL,'葬送のフリーレン','フリーレン','figure',NULL,NULL,NULL,'https://segaplaza.jp/prize/D123005/','2026-10-21T11:32:22.274347+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (109,7,27,'葬送のフリーレン Coreful フィギュア フェルン(タイクレ限定)',NULL,'葬送のフリーレン','フェルン','figure',NULL,NULL,NULL,'https://www.taito.co.jp/taito-prize/0451852500','2026-10-21T11:32:22.274351+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (110,7,27,'葬送のフリーレン Coreful フィギュア フリーレン~ドレスver.~',NULL,'葬送のフリーレン','フリーレン','figure',NULL,NULL,NULL,'https://www.taito.co.jp/taito-prize/0451950600','2026-10-21T11:32:22.274357+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (111,7,27,'葬送のフリーレン Coreful フィギュア フリーレン',NULL,'葬送のフリーレン','フリーレン','figure',NULL,NULL,NULL,'https://www.taito.co.jp/en/taito-prize/0451972800','2026-10-21T11:32:22.274525+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (112,8,28,'【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(スカーレット・スパイダー・スーツ版)',NULL,NULL,NULL,'figure','1/6',300,NULL,'https://www.hottoys.jp/item/view/100008115.php','2026-10-21T11:32:22.274532+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (113,8,28,'【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(スパイダー・パンク・スーツ版)',NULL,NULL,NULL,'figure','1/6',300,NULL,'https://www.hottoys.jp/item/view/100007491.php','2026-10-21T11:32:22.274536+08:00','official_metadata');
INSERT INTO "figures" ("id","manufacturer_id","product_line_id","name_original","name_ko","franchise","character","type","scale","height_mm","material","official_url","collected_at","quality") VALUES (114,8,28,'【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(クラシック・スーツ版)',NULL,NULL,NULL,'figure','1/6',300,NULL,'https://www.hottoys.jp/item/view/100009109','2026-10-21T11:32:22.274539+08:00','official_metadata');
SELECT setval(pg_get_serial_sequence('figures','id'), (SELECT MAX(id) FROM figures), true);

CREATE TABLE figure_variants (
	id SERIAL NOT NULL, 
	figure_id INTEGER NOT NULL, 
	variant_key VARCHAR(200) NOT NULL, 
	sku VARCHAR(120), 
	jan_code VARCHAR(30), 
	edition VARCHAR(200), 
	reissue_no INTEGER, 
	release_date VARCHAR(40), 
	release_precision VARCHAR(20), 
	PRIMARY KEY (id), 
	UNIQUE (figure_id, variant_key), 
	FOREIGN KEY(figure_id) REFERENCES figures (id)
)

;
CREATE INDEX ix_figure_variants_figure_id ON figure_variants (figure_id);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (1,1,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (2,2,'source-page',NULL,NULL,NULL,NULL,'2027-04','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (3,3,'source-page',NULL,NULL,NULL,NULL,'2027-09','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (4,4,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (5,5,'source-page',NULL,NULL,NULL,NULL,'2027-03','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (6,6,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (7,7,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (8,8,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (9,9,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (10,10,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (11,11,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (12,12,'source-page',NULL,NULL,NULL,NULL,'2027-03','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (13,13,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (14,14,'source-page',NULL,NULL,NULL,NULL,'2027-08','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (15,15,'source-page',NULL,NULL,NULL,NULL,'2027-02','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (16,16,'source-page',NULL,NULL,NULL,NULL,'2027-03','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (17,17,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (18,18,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (19,19,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (20,20,'source-page',NULL,NULL,NULL,NULL,'2027-03','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (21,21,'source-page',NULL,NULL,NULL,NULL,'2027-03','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (22,22,'source-page',NULL,NULL,NULL,NULL,'2027-03','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (23,23,'source-page',NULL,NULL,NULL,NULL,'2027-04','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (24,24,'source-page',NULL,NULL,NULL,NULL,'2027-02','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (25,25,'source-page',NULL,NULL,NULL,NULL,'2027-02','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (26,26,'source-page',NULL,NULL,NULL,NULL,'2026-12','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (27,27,'source-page',NULL,NULL,NULL,NULL,'2027-04','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (28,28,'source-page',NULL,NULL,NULL,NULL,'2027-04','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (29,29,'source-page',NULL,NULL,NULL,NULL,'2027-02','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (30,30,'source-page',NULL,NULL,NULL,NULL,'2026-12','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (31,31,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (32,32,'source-page',NULL,NULL,NULL,NULL,'2027-06','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (33,33,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (34,34,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (35,35,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (36,36,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (37,37,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (38,38,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (39,39,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (40,40,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (41,41,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (42,42,'source-page',NULL,NULL,NULL,NULL,'2027-05','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (43,43,'source-page',NULL,NULL,NULL,NULL,'2027-02','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (44,44,'source-page',NULL,NULL,NULL,NULL,'2027-02','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (45,45,'source-page',NULL,NULL,NULL,NULL,'2027-01','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (46,46,'source-page',NULL,NULL,NULL,NULL,'2026-12','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (47,47,'source-page',NULL,NULL,NULL,NULL,'2026-12','month');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (48,48,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (49,49,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (50,50,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (51,51,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (52,52,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (53,53,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (54,54,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (55,55,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (56,56,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (57,57,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (58,58,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (59,59,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (60,60,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (61,61,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (62,62,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (63,63,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (64,64,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (65,65,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (66,66,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (67,67,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (68,68,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (69,69,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (70,70,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (71,71,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (72,72,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (73,73,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (74,74,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (75,75,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (76,76,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (77,77,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (78,78,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (79,79,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (80,80,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (81,81,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (82,82,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (83,83,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (84,84,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (85,85,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (86,86,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (87,87,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (88,88,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (89,89,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (90,90,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (91,91,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (92,92,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (93,93,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (94,94,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (95,95,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (96,96,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (97,97,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (98,98,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (99,99,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (100,100,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (101,101,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (102,102,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (103,103,'source-page',NULL,NULL,NULL,NULL,'2026-02-14','day');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (104,104,'source-page',NULL,NULL,NULL,NULL,'2024-06-29','day');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (105,105,'source-page',NULL,NULL,NULL,NULL,'2026-09-12','day');
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (106,106,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (107,107,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (108,108,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (109,109,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (110,110,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (111,111,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (112,112,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (113,113,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "figure_variants" ("id","figure_id","variant_key","sku","jan_code","edition","reissue_no","release_date","release_precision") VALUES (114,114,'source-page',NULL,NULL,NULL,NULL,NULL,NULL);
SELECT setval(pg_get_serial_sequence('figure_variants','id'), (SELECT MAX(id) FROM figure_variants), true);

CREATE TABLE product_images (
	id SERIAL NOT NULL, 
	variant_id INTEGER NOT NULL, 
	image_url TEXT NOT NULL, 
	source_url TEXT NOT NULL, 
	usage_status VARCHAR(40) NOT NULL, 
	license_evidence TEXT, 
	checked_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(variant_id) REFERENCES figure_variants (id)
)

;

CREATE TABLE release_prices (
	id SERIAL NOT NULL, 
	variant_id INTEGER NOT NULL, 
	price_amount NUMERIC(14, 2) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	price_kind VARCHAR(40) NOT NULL, 
	tax_included BOOLEAN, 
	source_url TEXT NOT NULL, 
	checked_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (variant_id, source_url, price_kind), 
	CHECK (price_amount >= 0), 
	FOREIGN KEY(variant_id) REFERENCES figure_variants (id)
)

;
CREATE INDEX ix_release_prices_variant_id ON release_prices (variant_id);
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (1,31,5060.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273808+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (2,32,5060.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273812+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (3,33,4840.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273815+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (4,34,4840.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273819+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (5,35,4510.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273822+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (6,36,4950.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273845+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (7,37,4620.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273850+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (8,38,4620.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273854+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (9,39,4730.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273859+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (10,40,4730.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273863+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (11,41,4620.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273867+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (12,42,4400.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/lookup/','2026-10-21T11:32:22.273870+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (13,43,8250.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/gem/','2026-10-21T11:32:22.273873+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (14,44,8580.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/gem/','2026-10-21T11:32:22.273876+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (15,45,8800.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/gem/','2026-10-21T11:32:22.273898+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (16,46,8800.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/gem/','2026-10-21T11:32:22.273901+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (17,47,8800.00,'JPY','official_list',TRUE,'https://megahobby.jp/products/gem/','2026-10-21T11:32:22.273904+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (18,103,8800.00,'JPY','official_list',TRUE,'https://tamashiiweb.com/item/14690/','2026-10-21T11:32:22.274220+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (19,104,8800.00,'JPY','official_list',TRUE,'https://tamashiiweb.com/item/14735/','2026-10-21T11:32:22.274229+08:00');
INSERT INTO "release_prices" ("id","variant_id","price_amount","currency","price_kind","tax_included","source_url","checked_at") VALUES (20,105,9900.00,'JPY','official_list',TRUE,'https://tamashiiweb.com/item/15747/','2026-10-21T11:32:22.274235+08:00');
SELECT setval(pg_get_serial_sequence('release_prices','id'), (SELECT MAX(id) FROM release_prices), true);

CREATE TABLE retail_price_records (
	id SERIAL NOT NULL, 
	variant_id INTEGER NOT NULL, 
	retailer_id INTEGER NOT NULL, 
	price_type VARCHAR(40) NOT NULL, 
	amount NUMERIC(14, 2) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	shipping NUMERIC(14, 2), 
	availability VARCHAR(40) NOT NULL, 
	match_status VARCHAR(40) NOT NULL, 
	product_url TEXT NOT NULL, 
	observed_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (variant_id, product_url, observed_at, price_type), 
	CHECK (amount >= 0), 
	FOREIGN KEY(variant_id) REFERENCES figure_variants (id), 
	FOREIGN KEY(retailer_id) REFERENCES retailers (id)
)

;
CREATE INDEX ix_retail_price_records_variant_id ON retail_price_records (variant_id);

CREATE TABLE search_runs (
	id SERIAL NOT NULL, 
	variant_id INTEGER NOT NULL, 
	query TEXT NOT NULL, 
	provider VARCHAR(60) NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	payload JSON NOT NULL, 
	executed_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (variant_id, query, provider), 
	FOREIGN KEY(variant_id) REFERENCES figure_variants (id)
)

;

CREATE TABLE source_documents (
	id SERIAL NOT NULL, 
	variant_id INTEGER NOT NULL, 
	title TEXT NOT NULL, 
	url TEXT NOT NULL, 
	source_type VARCHAR(60) NOT NULL, 
	language VARCHAR(10) NOT NULL, 
	body TEXT NOT NULL, 
	usage_status VARCHAR(80) NOT NULL, 
	content_hash VARCHAR(64) NOT NULL, 
	collected_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (variant_id, url), 
	FOREIGN KEY(variant_id) REFERENCES figure_variants (id)
)

;
CREATE INDEX ix_source_documents_variant_id ON source_documents (variant_id);
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (1,1,'PUNI☆MOFU RACING XIAO with Honda Z50J Gorilla — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: PUNI☆MOFU RACING XIAO with Honda Z50J Gorilla
manufacturer: Kotobukiya
product_line: MEGAMI DEVICE
release_date: 2027-05
release_precision: month','factual_metadata_only','95871345df8f83490c131c8269a6d9b102ea84b392db8a117a1cec701e52a85e','2026-10-21T11:32:22.273302+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (2,2,'HEAVY WEAPON UNIT 77 ACTIVE BOOSTER — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: HEAVY WEAPON UNIT 77 ACTIVE BOOSTER
manufacturer: Kotobukiya
product_line: M.S.G Modeling Support Goods
release_date: 2027-04
release_precision: month','factual_metadata_only','79da2d19eb43b36fcaa9290cde67f205a6bb19965ab68d5f263891042a534171','2026-10-21T11:32:22.273336+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (3,3,'Yumia Liessfeldt Sun Shower Ver. — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: Yumia Liessfeldt Sun Shower Ver.
manufacturer: Kotobukiya
product_line: Atelier Yumia: The Alchemist of Memories & the Envisioned Land
release_date: 2027-09
release_precision: month','factual_metadata_only','b2f63e7b293b9628448f5e9c99818f3f606bf694e69a492441f1cce9dd3d513e','2026-10-21T11:32:22.273554+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (4,4,'SADAKO BISHOUJO STATUE — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: SADAKO BISHOUJO STATUE
manufacturer: Kotobukiya
product_line: SADAKO
release_date: 2027-05
release_precision: month','factual_metadata_only','fec1d2ed835fd6c737ff3a35f46baadb372f1f37ed7890ab9818625e233bf7be','2026-10-21T11:32:22.273559+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (5,5,'MIRAGE C02-URANUS — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: MIRAGE C02-URANUS
manufacturer: Kotobukiya
product_line: ARMORED CORE
release_date: 2027-03
release_precision: month','factual_metadata_only','9d16a573b6bd7283de237fda81219cb6bee2b9ba5df7b9293bbf25e9397c9475','2026-10-21T11:32:22.273564+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (6,6,'BLUES — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: BLUES
manufacturer: Kotobukiya
product_line: MEGA MAN
release_date: 2027-06
release_precision: month','factual_metadata_only','377c62880b8cbe6c32c5247bc1c696c5f42ac5779d9b816934bfd30fdda7db49','2026-10-21T11:32:22.273567+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (7,7,'ROCKMAN — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: ROCKMAN
manufacturer: Kotobukiya
product_line: MEGA MAN
release_date: 2027-06
release_precision: month','factual_metadata_only','3ed0d0607e636d6076eb33775c8c8e4ededd7a6f02ffeefb12a053a3c7db97e3','2026-10-21T11:32:22.273570+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (8,8,'Free Planets Alliance 13th Fleet Flagship Hyperion — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: Free Planets Alliance 13th Fleet Flagship Hyperion
manufacturer: Kotobukiya
product_line: Legend of the Galactic Heroes
release_date: 2027-06
release_precision: month','factual_metadata_only','cf5f2ac7c5097dabf0b6b82e6cd9d11d4a4460caeded0580d25978e20a495663','2026-10-21T11:32:22.273573+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (9,9,'V-THOR — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: V-THOR
manufacturer: Kotobukiya
product_line: HEXA GEAR
release_date: 2027-06
release_precision: month','factual_metadata_only','ab1c8b855f595b4bbc299c483d92572aad8af734d7b55c10a37a3d7553ce6cdc','2026-10-21T11:32:22.273576+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (10,10,'EVANGELION 13 Awake Ver. — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: EVANGELION 13 Awake Ver.
manufacturer: Kotobukiya
product_line: Evangelion: New Theatrical Edition
release_date: 2027-06
release_precision: month','factual_metadata_only','62c87c1dc2c61b6f4a55b89e4e604d7cd2513668290117486f267dd41d0f428d','2026-10-21T11:32:22.273579+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (11,11,'Empee — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: Empee
manufacturer: Kotobukiya
product_line: Magic Repo Man : Dumped by My Party, I’ll Cash In With a Cute Support Fairy to Become the Strongest!
release_date: 2027-05
release_precision: month','factual_metadata_only','352eac173bd058e7860e8c4f09ae022996df39b83eb3994ecdded56f3b1fcb9d','2026-10-21T11:32:22.273581+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (12,12,'D-STYLE IRONKONG  ［Clear Parts Append］ — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: D-STYLE IRONKONG  ［Clear Parts Append］
manufacturer: Kotobukiya
product_line: ZOIDS
release_date: 2027-03
release_precision: month','factual_metadata_only','fe9fdfd74e17824fd70ae17ef725454ff848600c2cfef98afafd5813da86fe3f','2026-10-21T11:32:22.273585+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (13,13,'DURGA I DARKNESS QUEEN Ver. — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: DURGA I DARKNESS QUEEN Ver.
manufacturer: Kotobukiya
product_line: FRAME ARMS GIRL
release_date: 2027-05
release_precision: month','factual_metadata_only','43cfcba1c71ff73bca84525d6d4e3a0d0dbf8c34f560e5354527998c77239d67','2026-10-21T11:32:22.273589+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (14,14,'ELSA — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: ELSA
manufacturer: Kotobukiya
product_line: Sasaki and Peeps
release_date: 2027-08
release_precision: month','factual_metadata_only','f8446413c05d369af11efe7495b67f620c5d31240257e267c0229b7adfa08bdf','2026-10-21T11:32:22.273597+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (15,15,'D-STYLE DEATH SAURER — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: D-STYLE DEATH SAURER
manufacturer: Kotobukiya
product_line: ZOIDS
release_date: 2027-02
release_precision: month','factual_metadata_only','cd4b527f917826cb30a44630d20a5ab7e75e675d6bc680d86aade69f5e889bd5','2026-10-21T11:32:22.273601+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (16,16,'GREAT EXKIZER FULL EDITION — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: GREAT EXKIZER FULL EDITION
manufacturer: Kotobukiya
product_line: Brave Exkaiser
release_date: 2027-03
release_precision: month','factual_metadata_only','022c9a98911b2b7147268b0b76e77c0b91c99f520b7435851fb31028af14c8b1','2026-10-21T11:32:22.273763+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (17,17,'BUSTER DOLL PALADIN — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: BUSTER DOLL PALADIN
manufacturer: Kotobukiya
product_line: MEGAMI DEVICE
release_date: 2027-05
release_precision: month','factual_metadata_only','c137fd63a9a9f046c28d3090cd4741b827fb0603e3f3724b54950d8f3e04e867','2026-10-21T11:32:22.273767+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (18,18,'BUSTER DOLL TANK — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: BUSTER DOLL TANK
manufacturer: Kotobukiya
product_line: MEGAMI DEVICE
release_date: 2027-05
release_precision: month','factual_metadata_only','176809cb8efc37f0b268623691e950d0c291f923e73aa381e9b98a71062bdbfb','2026-10-21T11:32:22.273770+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (19,19,'Hikaru Shidou — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: Hikaru Shidou
manufacturer: Kotobukiya
product_line: Magic Knight Rayearth
release_date: 2027-05
release_precision: month','factual_metadata_only','a39f9ebf8a01cdf3bac6374cbc450d0ebdbb653a0367562468e87398ba5a75a4','2026-10-21T11:32:22.273772+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (20,20,'SANA AKABISHI【DRESS CODE】 — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: SANA AKABISHI【DRESS CODE】
manufacturer: Kotobukiya
product_line: MEGALOMARIA UNLIMITED UNIVERSE
release_date: 2027-03
release_precision: month','factual_metadata_only','959c6b1114bcbeae57b8a6147b55e8ebb484b28d6da1bfa40490f55cf857d139','2026-10-21T11:32:22.273775+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (21,21,'METAMORPHOSE UNIT PHLEGETHON — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: METAMORPHOSE UNIT PHLEGETHON
manufacturer: Kotobukiya
product_line: MEGALOMARIA UNLIMITED UNIVERSE
release_date: 2027-03
release_precision: month','factual_metadata_only','46454fce6ecddf3912f194d16b5125cbd8fc86d7851f01ee346095328413231f','2026-10-21T11:32:22.273778+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (22,22,'METAMORPHOSE UNIT CRIMINAL BUSTER — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: METAMORPHOSE UNIT CRIMINAL BUSTER
manufacturer: Kotobukiya
product_line: MEGALOMARIA UNLIMITED UNIVERSE
release_date: 2027-03
release_precision: month','factual_metadata_only','9613bc9be5e8185d101a8ffff7ae33f7857a6e883c30dc57e4e4e47875aa2ea2','2026-10-21T11:32:22.273782+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (23,23,'MAKINA — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: MAKINA
manufacturer: Kotobukiya
product_line: 銀河特急 ミルキー☆サブウェイ
release_date: 2027-04
release_precision: month','factual_metadata_only','c67f61081b1fb42a3bf235aef1c8ba5603d22ab2fff8a2e85518df2ad4ef84f2','2026-10-21T11:32:22.273785+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (24,24,'HEAVY WEAPON UNIT78 CUSTOMIZE CORE WING BLADE — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: HEAVY WEAPON UNIT78 CUSTOMIZE CORE WING BLADE
manufacturer: Kotobukiya
product_line: M.S.G Modeling Support Goods
release_date: 2027-02
release_precision: month','factual_metadata_only','f2285af6f847d86e510f6b05d9ca82a83b9695937b3a0070aa00d06a1dc401f8','2026-10-21T11:32:22.273788+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (25,25,'V-THOR Assault Type "Ji rei" (Swift Thunder) — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: V-THOR Assault Type "Ji rei" (Swift Thunder)
manufacturer: Kotobukiya
product_line: HEXA GEAR
release_date: 2027-02
release_precision: month','factual_metadata_only','f2bd5acf2cfe160fab96c23606d4258246a72b6f38961fdb25b91b43693ff77f','2026-10-21T11:32:22.273791+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (26,26,'LX-00 RAY FALX:RE2 — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: LX-00 RAY FALX:RE2
manufacturer: Kotobukiya
product_line: FRAME ARMS
release_date: 2026-12
release_precision: month','factual_metadata_only','689b3ff158e43700923750faddffad4ccd3a56b8c40a9056e52b0f4828d12898','2026-10-21T11:32:22.273794+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (27,27,'MV-02 FINE & ZEKE — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: MV-02 FINE & ZEKE
manufacturer: Kotobukiya
product_line: ZOIDS
release_date: 2027-04
release_precision: month','factual_metadata_only','5d93d638527f2dd0a6c57cd688b4f1e566920f92e665f0718ab18dd247159d6d','2026-10-21T11:32:22.273797+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (28,28,'PUNI☆MOFU RACING LANG with Honda Z50J Gorilla — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: PUNI☆MOFU RACING LANG with Honda Z50J Gorilla
manufacturer: Kotobukiya
product_line: MEGAMI DEVICE
release_date: 2027-04
release_precision: month','factual_metadata_only','7a5d361107cdc76ad726b5f973b43e3de458c2ef96597d96651f425075187434','2026-10-21T11:32:22.273800+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (29,29,'CREST CR-C75U2 DELTA Ver. — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: CREST CR-C75U2 DELTA Ver.
manufacturer: Kotobukiya
product_line: ARMORED CORE
release_date: 2027-02
release_precision: month','factual_metadata_only','8a370ac0661ebbb7cc64c4d47fef54b06a40d007db4be6d5c3c2c6ae4b7cd7ff','2026-10-21T11:32:22.273803+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (30,30,'YUKUMO — 공식 메타데이터 발췌','https://www.kotobukiya.co.jp/en/product/','official_metadata_extract','und','name_original: YUKUMO
manufacturer: Kotobukiya
product_line: ARCANADEA
release_date: 2026-12
release_precision: month','factual_metadata_only','53d3a5a00f365fd13ac31e2ebf87a2ed06a17f2575183a944c7fcfeb7838755e','2026-10-21T11:32:22.273806+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (31,31,'るかっぷ 刀剣乱舞ONLINE 山姥切国広 — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 刀剣乱舞ONLINE 山姥切国広
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-06
release_precision: month
price_amount: 5060
currency: JPY
price_kind: official_list','factual_metadata_only','3b2170e302b8ad9541ceb3fdf10b29654b9f411794522bee763379517ab8b2d0','2026-10-21T11:32:22.273808+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (32,32,'るかっぷ 刀剣乱舞ONLINE 山姥切長義 — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 刀剣乱舞ONLINE 山姥切長義
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-06
release_precision: month
price_amount: 5060
currency: JPY
price_kind: official_list','factual_metadata_only','be53c15f67b5d119dc471a08b3f3f27122532915b060d5aa976732f2a13a5ab5','2026-10-21T11:32:22.273812+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (33,33,'るかっぷ 転生したらスライムだった件 リムル=テンペスト — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 転生したらスライムだった件 リムル=テンペスト
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4840
currency: JPY
price_kind: official_list','factual_metadata_only','f6eb9e9548b613ee33006bd287de990327d51c47ad71f9282a388b58a0110d62','2026-10-21T11:32:22.273815+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (34,34,'るかっぷ 転生したらスライムだった件 ディアブロ — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 転生したらスライムだった件 ディアブロ
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4840
currency: JPY
price_kind: official_list','factual_metadata_only','e9a72f892581a770f1b31e78568f3666d2eb73eea71e0abf433a5489c74cd6d9','2026-10-21T11:32:22.273819+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (35,35,'るかっぷ アオのハコ 鹿野千夏 — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ アオのハコ 鹿野千夏
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4510
currency: JPY
price_kind: official_list','factual_metadata_only','1f38152df3cf3aed35dd7521ae35809d2a384fac297118d759891284b0cc1d6e','2026-10-21T11:32:22.273822+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (36,36,'るかっぷ 超かぐや姫！ 月見ヤチヨ — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 超かぐや姫！ 月見ヤチヨ
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4950
currency: JPY
price_kind: official_list','factual_metadata_only','1a968abe91d5649d0759311a80341e4b57ff8f559f1cdbf62c41f3964a9711cd','2026-10-21T11:32:22.273845+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (37,37,'るかっぷ NARUTO-ナルト- 疾風伝 奈良シカマル にこっとver. — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ NARUTO-ナルト- 疾風伝 奈良シカマル にこっとver.
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4620
currency: JPY
price_kind: official_list','factual_metadata_only','2e6e1a1d94b990ad573b79a93b604bc438e15be142d4e03e4cee7c92c46ef6c8','2026-10-21T11:32:22.273850+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (38,38,'るかっぷ NARUTO-ナルト- 疾風伝 我愛羅 にこっとver. — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ NARUTO-ナルト- 疾風伝 我愛羅 にこっとver.
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4620
currency: JPY
price_kind: official_list','factual_metadata_only','4b89398205fa88bd575ac435c6ebf8c103d74ee278536c8654e126399766a36a','2026-10-21T11:32:22.273854+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (39,39,'るかっぷ TVアニメ『BLEACH』 ウルキオラ・シファー — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ TVアニメ『BLEACH』 ウルキオラ・シファー
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4730
currency: JPY
price_kind: official_list','factual_metadata_only','58bf7eefc3d6f52df037e170208b078b03948111abfb1fb54a19074de429089f','2026-10-21T11:32:22.273859+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (40,40,'るかっぷ TVアニメ『BLEACH』 グリムジョー・ジャガージャック — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ TVアニメ『BLEACH』 グリムジョー・ジャガージャック
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4730
currency: JPY
price_kind: official_list','factual_metadata_only','cf8b7ec5ff9ca3953564c8562017121824845dd4b432b8d08863d855930b4df7','2026-10-21T11:32:22.273863+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (41,41,'るかっぷ 鬼滅の刃 獪岳 — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 鬼滅の刃 獪岳
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4620
currency: JPY
price_kind: official_list','factual_metadata_only','9db994f35cc433c905d880c7df00fe08969fe8132b02394c750a73682f774ba4','2026-10-21T11:32:22.273867+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (42,42,'るかっぷ 鬼滅の刃 我妻善逸 むん！ver. — 공식 메타데이터 발췌','https://megahobby.jp/products/lookup/','official_metadata_extract','und','name_original: るかっぷ 鬼滅の刃 我妻善逸 むん！ver.
manufacturer: MegaHouse
product_line: Look Up
release_date: 2027-05
release_precision: month
price_amount: 4400
currency: JPY
price_kind: official_list','factual_metadata_only','0764272c2e7251c7aed925b571d19cbff218fa2f4e524c64222881b368b25814','2026-10-21T11:32:22.273870+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (43,43,'G.E.M.シリーズ NARUTO-ナルト- 疾風伝 てのひらミナト — 공식 메타데이터 발췌','https://megahobby.jp/products/gem/','official_metadata_extract','und','name_original: G.E.M.シリーズ NARUTO-ナルト- 疾風伝 てのひらミナト
manufacturer: MegaHouse
product_line: G.E.M.
release_date: 2027-02
release_precision: month
price_amount: 8250
currency: JPY
price_kind: official_list','factual_metadata_only','420398a786f12197edeb1cc1f9b1109023abc7d98354af89b888a1b4e0ebb535','2026-10-21T11:32:22.273873+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (44,44,'G.E.M.シリーズ 鬼滅の刃 てのひらしのぶさん【再販】 — 공식 메타데이터 발췌','https://megahobby.jp/products/gem/','official_metadata_extract','und','name_original: G.E.M.シリーズ 鬼滅の刃 てのひらしのぶさん【再販】
manufacturer: MegaHouse
product_line: G.E.M.
release_date: 2027-02
release_precision: month
price_amount: 8580
currency: JPY
price_kind: official_list','factual_metadata_only','51239bb2f316c4e567e815816d8735779a209597f5ac6c9bb770a46f4e4edf41','2026-10-21T11:32:22.273876+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (45,45,'G.E.M.シリーズ 文豪ストレイドッグス てのひら太宰さん — 공식 메타데이터 발췌','https://megahobby.jp/products/gem/','official_metadata_extract','und','name_original: G.E.M.シリーズ 文豪ストレイドッグス てのひら太宰さん
manufacturer: MegaHouse
product_line: G.E.M.
release_date: 2027-01
release_precision: month
price_amount: 8800
currency: JPY
price_kind: official_list','factual_metadata_only','e3e80c8dc0b2b20ade00921d25d8887087b46a14fa782b23317442021fa038c8','2026-10-21T11:32:22.273898+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (46,46,'G.E.M.シリーズ 進撃の巨人 てのひらエレン — 공식 메타데이터 발췌','https://megahobby.jp/products/gem/','official_metadata_extract','und','name_original: G.E.M.シリーズ 進撃の巨人 てのひらエレン
manufacturer: MegaHouse
product_line: G.E.M.
release_date: 2026-12
release_precision: month
price_amount: 8800
currency: JPY
price_kind: official_list','factual_metadata_only','798e6fa3e6318ddc5b1f260575117a102df36e5245f4d6c79ba19894fa802980','2026-10-21T11:32:22.273901+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (47,47,'G.E.M.シリーズ 進撃の巨人 てのひらリヴァイ兵士長 — 공식 메타데이터 발췌','https://megahobby.jp/products/gem/','official_metadata_extract','und','name_original: G.E.M.シリーズ 進撃の巨人 てのひらリヴァイ兵士長
manufacturer: MegaHouse
product_line: G.E.M.
release_date: 2026-12
release_precision: month
price_amount: 8800
currency: JPY
price_kind: official_list','factual_metadata_only','d2bee8fdefc9b181b3bd3bc788236ba7e2dfb5b09190c62ccc5988ca86b14476','2026-10-21T11:32:22.273904+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (48,48,'TENITOL 魔王ちゃん [mini] — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL 魔王ちゃん [mini]
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','2d3bcd2e66b29abc685ff5d4de0491a8866648a2578bf9615d036df056821de2','2026-10-21T11:32:22.273907+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (49,49,'TENITOL ヴェルジュ(バニー) [mini] — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL ヴェルジュ(バニー) [mini]
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','a03f9b87738c9fc0522bbf50fe24f7aa5321db95b99511ace4a3bd393bb67b73','2026-10-21T11:32:22.273910+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (50,50,'TENITOL ヴェルナー(バニー) [mini] — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL ヴェルナー(バニー) [mini]
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','e01520f0e26a4dce5cdda8515174891444f7e45099393d5aafeed25b7c27e8ce','2026-10-21T11:32:22.273913+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (51,51,'TENITOL TALL フリーレン クラシカルワンピースver. — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL フリーレン クラシカルワンピースver.
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','bf6276c82db0b2af3cf9182edd531d45ad877ee874a09702d7006bd71ff18506','2026-10-21T11:32:22.273915+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (52,52,'TENITOL TALL フェルン クラシカルワンピースver. — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL フェルン クラシカルワンピースver.
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','4d6a7e020b7dbeab5533904dc383cdbbb4c624d77174b76a0d5af403c0ccd6a2','2026-10-21T11:32:22.273931+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (53,53,'Nachoneko Birthday ver. 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: Nachoneko Birthday ver. 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','a631c108a396bf56baab1f5cb4b739425389b53d01b7bee7b97435ec321e1ba0','2026-10-21T11:32:22.273934+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (54,54,'TENITOL TALL 鹿目まどか&暁美ほむら スペシャルセット — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL 鹿目まどか&暁美ほむら スペシャルセット
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','5a453205e45b09c7a970b1a1effd8bb7586bf045e5773cdb9448adbf1dc1e25b','2026-10-21T11:32:22.273937+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (55,55,'TENITOL TALL 鹿目まどか — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL 鹿目まどか
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','fad0153fb3b4ad8d7c07daf38bb1879627e0feff9fc7105268bc138295400939','2026-10-21T11:32:22.273940+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (56,56,'TENITOL TALL 暁美ほむら — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL 暁美ほむら
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','8974e5df9991f70c3d4d4da758cd25f18bfac0629b275e3f028c7d58b34dcd33','2026-10-21T11:32:22.273945+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (57,57,'TENITOL フリーレン[petit] — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL フリーレン[petit]
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','888b0e60bdab82a5eee7044197d3d0c4f17db0b3292deac2d3367135f1ad6af3','2026-10-21T11:32:22.273947+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (58,58,'TENITOL TALL 椎名真昼 Winter clothes ver. — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL 椎名真昼 Winter clothes ver.
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','b0be1b6ce14c0df105f5e8ec633df1584fa6714a532b5b57aa3d7bcb3234b2c2','2026-10-21T11:32:22.273949+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (59,59,'TENITOL TALL 白 水着ドレスver. — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL 白 水着ドレスver.
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','bcb9710abbfa268e4d8b93c5f61355486ec744c4627c6e5bd81e97d5573c67fe','2026-10-21T11:32:22.273952+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (60,60,'周防パトラ バニーver. 1/6スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 周防パトラ バニーver. 1/6スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/6','factual_metadata_only','6440c183a53bd5320d27f4ce0a33314e105a1f29cc9529ed04e069795efc5cf2','2026-10-21T11:32:22.273954+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (61,61,'しぐれうい “Wishing Umbrella” 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: しぐれうい “Wishing Umbrella” 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','b1a74362cd42b5f73ab85f654a15403fc5e04852045e690d703e2ff19fad08bf','2026-10-21T11:32:22.273956+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (62,62,'フリーレン フォトフレームフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: フリーレン フォトフレームフィギュア
manufacturer: FuRyu
product_line: F:NEX','factual_metadata_only','d2bbdd4a37a6a2dace21bed6616f0a3307ed39a298a06f5fe3abe415009f96bc','2026-10-21T11:32:22.273959+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (63,63,'D：キラーワイフ - シークレットポリス 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: D：キラーワイフ - シークレットポリス 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','0a8a63709a5bfa45478f664dd7dbebd2b8615be051b085ffffa254d0e70dbd93','2026-10-21T11:32:22.273981+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (64,64,'ウンファ：タクティカル・アップ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: ウンファ：タクティカル・アップ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','92e118bda23d15a5b90bc98342045bf6268c9597cb014f5c079bfd08c1fea5d1','2026-10-21T11:32:22.274045+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (65,65,'エクス・アルビオ  1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: エクス・アルビオ  1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','e4002f52c413efaf7ec206519935387927890172d5060815e3621bffa63cbc29','2026-10-21T11:32:22.274048+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (66,66,'でびでび・でびる 1/2スケールソフビフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: でびでび・でびる 1/2スケールソフビフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/2','factual_metadata_only','ae6ed2b28ac1fec6dad306f26494d55c32bf4700fc186c8775b0b1d721c2a54b','2026-10-21T11:32:22.274051+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (67,67,'加賀美ハヤト 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 加賀美ハヤト 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','8a43bbddfedfb97bf996e0bebcd236dd4412e65d83dad715409e6bc5abde3666','2026-10-21T11:32:22.274053+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (68,68,'不破湊  1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 不破湊  1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','d56bfb8628079ed1590ebc904af17e96165030301e7d7a5677aaa58cb9c7fddf','2026-10-21T11:32:22.274056+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (69,69,'レイン・パターソン  1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: レイン・パターソン  1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','3332405c1993d8f82e34236ee523271fa7f7577b3ebf60e5deab4aad3be29636','2026-10-21T11:32:22.274058+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (70,70,'花畑チャイカ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 花畑チャイカ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','347e9c61defa80f2934898f37812cff4c9b250c4407c464cac05bc346400d3b5','2026-10-21T11:32:22.274075+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (71,71,'叢雲カゲツ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 叢雲カゲツ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','5255957793fc4164ce366cb53feb72f660879f18cd07a1dea430e137d624b16c','2026-10-21T11:32:22.274077+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (72,72,'常守 朱＆狡噛 慎也 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 常守 朱＆狡噛 慎也 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','57eadaa988082a457d8c7319c4b7ebce569537d3a80f111fda42a238c612b812','2026-10-21T11:32:22.274080+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (73,73,'吉徳×F:NEX 桜ミク -日本人形- 1/4スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 吉徳×F:NEX 桜ミク -日本人形- 1/4スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/4','factual_metadata_only','e04654b7d30eac6db9ee0ee4e410c9f122d6af935a3d73413e863646a1850f8a','2026-10-21T11:32:22.274082+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (74,74,'エリ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: エリ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','64d95f9a25ff54ef1002421d935af985c851bebaef83ffcb684fbc3e3e25ebd0','2026-10-21T11:32:22.274085+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (75,75,'牧瀬紅莉栖＆岡部倫太郎 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 牧瀬紅莉栖＆岡部倫太郎 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','06a36f2fd098a0516b50cfe84521530ac15b6ed53b79d95db1b109446428a97f','2026-10-21T11:32:22.274088+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (76,76,'ディーゼル - ミッドナイト・ストロベリー 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: ディーゼル - ミッドナイト・ストロベリー 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','a81e603a81ecea4ea9010da8f86f55006c65152a474ad41b1e2410ee4bf167ce','2026-10-21T11:32:22.274090+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (77,77,'久世しずか&雲母坂まりな 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 久世しずか&雲母坂まりな 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','bc97258468df54d6b4d1e67e191fc65afb807d25d245c60861efaa4233169b80','2026-10-21T11:32:22.274093+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (78,78,'ベルベット 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: ベルベット 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','0d254953e0aaa946255c58e6096e01b5105f358e98a8a10e6c7c17b5325ddd1d','2026-10-21T11:32:22.274095+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (79,79,'吉徳×F:NEX A2 -日本人形-1/4スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 吉徳×F:NEX A2 -日本人形-1/4スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/4','factual_metadata_only','7177488d08a351118cd9d1f566578002f1bfb7c9ffe209896721337ee3e82585','2026-10-21T11:32:22.274098+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (80,80,'七海千秋 illustration by めつぶしあんこ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 七海千秋 illustration by めつぶしあんこ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','9a589fd3499bd3b38a658b2e3f44d88514cb72cf4dfad4f715111f84a48b21a1','2026-10-21T11:32:22.274100+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (81,81,'霧切響子 illustration by めつぶしあんこ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 霧切響子 illustration by めつぶしあんこ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','382d2a3026b192f637ace13a610db27fdb0887be42b02e4269870e108d00367b','2026-10-21T11:32:22.274102+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (82,82,'楪いのり 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 楪いのり 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','dcfb905f9988565266ac5433a7c86fb884003a75d3a13ed51ce94e7e17544356','2026-10-21T11:32:22.274105+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (83,83,'雪ノ下雪乃 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 雪ノ下雪乃 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','66e8a7e8765a13ee4c01c5d4ef655bbaf14610f73a59c722e601d8ca84bebf86','2026-10-21T11:32:22.274108+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (84,84,'由比ヶ浜結衣 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 由比ヶ浜結衣 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','d2d3eb7d57ab4d307456287f70982cda0cfcb681148fd397ec8cdf30fac87bb7','2026-10-21T11:32:22.274110+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (85,85,'一色いろは 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 一色いろは 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','f8d74c6b377c7c2ac8982f9a067e23c33839f1406b37328871a2d7a63513a46f','2026-10-21T11:32:22.274112+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (86,86,'小木曽雪菜 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 小木曽雪菜 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','e2949a7004a4eca44a34a96dd12445227e8e35cf9878044528401a05a64f5245','2026-10-21T11:32:22.274114+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (87,87,'冬馬かずさ 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: 冬馬かずさ 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','acbbafe50b54835ba686d857a7d317040dce9874d8629ece8428faa922d6af91','2026-10-21T11:32:22.274116+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (88,88,'ロキシー・ミグルディア・グレイラット マントver. 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: ロキシー・ミグルディア・グレイラット マントver. 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','c21fe382ca3cd6087de00ab69d6458979de357eb65f04ae9f40a20f576ad1067','2026-10-21T11:32:22.274118+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (89,89,'ファム・スール 1/7スケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: ファム・スール 1/7スケールフィギュア
manufacturer: FuRyu
product_line: F:NEX
scale: 1/7','factual_metadata_only','b2892540120df69a56daf4e04d99f781438379dac6dc89ad77f3f33f6652e825','2026-10-21T11:32:22.274121+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (90,90,'TENITOL TALL ロキシー・ミグルディア・グレイラット — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL ロキシー・ミグルディア・グレイラット
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','e03d548f860a21c9d0672c03c9138a7dea528b7048cd5a1a04e8655431ca1d65','2026-10-21T11:32:22.274123+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (91,91,'TENITOL TALL イヅツミクラシカルメイドスタイルver. — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL イヅツミクラシカルメイドスタイルver.
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','08e57c4a501d8fb4362bed51555255999e13cb6101a62a5c270a96aef6b5f86c','2026-10-21T11:32:22.274126+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (92,92,'ファリン(キメラ) ドレススタイルver. ノンスケールフィギュア — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: ファリン(キメラ) ドレススタイルver. ノンスケールフィギュア
manufacturer: FuRyu
product_line: F:NEX','factual_metadata_only','ee927539dd2172814eba79ef2d78b73086e4c09c6fda98296da34c2337568f02','2026-10-21T11:32:22.274128+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (93,93,'TENITOL TALL レーシングミク 2026 いいね！Ver. — 공식 메타데이터 발췌','https://furyu-hm.com/','official_metadata_extract','und','name_original: TENITOL TALL レーシングミク 2026 いいね！Ver.
manufacturer: FuRyu
product_line: TENITOL','factual_metadata_only','3ee93019413928b5835fce24875d391e59928194016270c1ab244537f932bce2','2026-10-21T11:32:22.274130+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (94,94,'Nendoroid Hyakkimaru — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/6143','official_metadata_extract','und','name_original: Nendoroid Hyakkimaru
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: Dororo
height_mm: 100
material: PVC / ABS','factual_metadata_only','3a68f5abe9625af9c07e291d47eba6274d2b6ff3fa6b24482a7a30e63fe75284','2026-10-21T11:32:22.274135+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (95,95,'Nendoroid Blake Belladonna — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/8370','official_metadata_extract','und','name_original: Nendoroid Blake Belladonna
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: RWBY
height_mm: 100
material: PVC / ABS','factual_metadata_only','eaae5736c565c84ea9d02ae72177a076452dd0e93b882a650c36240e1496def4','2026-10-21T11:32:22.274141+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (96,96,'Nendoroid Vanilla — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/6761','official_metadata_extract','und','name_original: Nendoroid Vanilla
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: NEKOPARA
height_mm: 100
material: PVC / ABS','factual_metadata_only','aac598108a63755fb99f6aa3bd7dc9b440e473c9c51aa59f094083addc47182e','2026-10-21T11:32:22.274202+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (97,97,'Nendoroid Gon Freecss — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/6357','official_metadata_extract','und','name_original: Nendoroid Gon Freecss
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: HUNTER x HUNTER
height_mm: 100','factual_metadata_only','9e30a6f7d04f537cd370761a619a142573521cc733c6883458ffeb15ccd59647','2026-10-21T11:32:22.274206+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (98,98,'Nendoroid Ireena — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/11488','official_metadata_extract','und','name_original: Nendoroid Ireena
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: The Greatest Demon Lord Is Reborn as a Typical Nobody
height_mm: 100','factual_metadata_only','9cef0b6e586739f7ede6c436a0bf4e9b57f4169eba7c1c5ac0e4bf200a63ca08','2026-10-21T11:32:22.274208+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (99,99,'Nendoroid Mimic — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/60956','official_metadata_extract','und','name_original: Nendoroid Mimic
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: Frieren: Beyond Journey''s End','factual_metadata_only','49a22277d31029e4064e6a43bca44754f933ee7ed58bd37e9aa605f51089c11d','2026-10-21T11:32:22.274211+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (100,100,'Nendoroid Mai Sakurajima — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/6029','official_metadata_extract','und','name_original: Nendoroid Mai Sakurajima
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: Rascal Does Not Dream of Bunny Girl Senpai
height_mm: 100
material: PVC / ABS','factual_metadata_only','52d063c57b4364cdedf9dfd8a09b68cc9da92bf5febdd9a4a36ff307d41cf21b','2026-10-21T11:32:22.274213+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (101,101,'Nendoroid Woosa — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/1141000','official_metadata_extract','und','name_original: Nendoroid Woosa
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: Black Desert
height_mm: 100','factual_metadata_only','a551b027d7154bd7ffb80a4400716e440555abaa0648385fdb99675d98a7b7cb','2026-10-21T11:32:22.274216+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (102,102,'Nendoroid Kurisu Makise: Lab Coat Ver. [Basic] — 공식 메타데이터 발췌','https://www.goodsmile.com/en/product/1142378','official_metadata_extract','und','name_original: Nendoroid Kurisu Makise: Lab Coat Ver. [Basic]
manufacturer: Good Smile Company
product_line: Nendoroid
franchise: STEINS;GATE
height_mm: 100','factual_metadata_only','b8cf6f93bc1bf231e71a5dd87abae3045235da9ec05de61ba139320fc406b1fc','2026-10-21T11:32:22.274218+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (103,103,'フリーレン — 공식 메타데이터 발췌','https://tamashiiweb.com/item/14690/','official_metadata_extract','und','name_original: フリーレン
name_ko: S.H.Figuarts 프리렌
manufacturer: Bandai Spirits
product_line: S.H.Figuarts
franchise: 葬送のフリーレン
character: フリーレン
release_date: 2026-02-14
release_precision: day
price_amount: 8800
currency: JPY
price_kind: official_list
height_mm: 120
material: PVC / ABS','factual_metadata_only','91145d4cd4e4c88e6e604ba80a1d9d7d1eb1f8077c869938ab6f89d06f9c7ffa','2026-10-21T11:32:22.274220+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (104,104,'フェルン — 공식 메타데이터 발췌','https://tamashiiweb.com/item/14735/','official_metadata_extract','und','name_original: フェルン
name_ko: S.H.Figuarts 페른
manufacturer: Bandai Spirits
product_line: S.H.Figuarts
franchise: 葬送のフリーレン
character: フェルン
release_date: 2024-06-29
release_precision: day
price_amount: 8800
currency: JPY
price_kind: official_list','factual_metadata_only','ccdef68b29f9b438f6c1481fba81456acfe6c7a5571cee94274555f264257f61','2026-10-21T11:32:22.274229+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (105,105,'ヒンメル — 공식 메타데이터 발췌','https://tamashiiweb.com/item/15747/','official_metadata_extract','und','name_original: ヒンメル
name_ko: S.H.Figuarts 힘멜
manufacturer: Bandai Spirits
product_line: S.H.Figuarts
franchise: 葬送のフリーレン
character: ヒンメル
release_date: 2026-09-12
release_precision: day
price_amount: 9900
currency: JPY
price_kind: official_list','factual_metadata_only','6d03eec9040a5fa7ef39392a044125bdec079c7a4336aeadec3fc9f61cb30bf4','2026-10-21T11:32:22.274235+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (106,106,'葬送のフリーレン Luminasta “フリーレン” ~葬送のフリーレン~ — 공식 메타데이터 발췌','https://segaplaza.jp/prize/D121425/','official_metadata_extract','und','name_original: 葬送のフリーレン Luminasta “フリーレン” ~葬送のフリーレン~
manufacturer: SEGA
product_line: Luminasta
franchise: 葬送のフリーレン
character: フリーレン','factual_metadata_only','d5dbc6d329d09cf53bf4c33323f834adf9bbb68768d483bf0fd330b912f952e4','2026-10-21T11:32:22.274245+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (107,107,'葬送のフリーレン Luminasta “フリーレン” ~インミミック~ — 공식 메타데이터 발췌','https://segaplaza.jp/prize/D122835/','official_metadata_extract','und','name_original: 葬送のフリーレン Luminasta “フリーレン” ~インミミック~
manufacturer: SEGA
product_line: Luminasta
franchise: 葬送のフリーレン
character: フリーレン','factual_metadata_only','e8f4bf0efc1a891a0e8889b4980c082f7e3ad4325015b481da1fc775478c8944','2026-10-21T11:32:22.274340+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (108,108,'葬送のフリーレン Luminasta “フリーレン” ~SUMMER DRESS~ — 공식 메타데이터 발췌','https://segaplaza.jp/prize/D123005/','official_metadata_extract','und','name_original: 葬送のフリーレン Luminasta “フリーレン” ~SUMMER DRESS~
manufacturer: SEGA
product_line: Luminasta
franchise: 葬送のフリーレン
character: フリーレン','factual_metadata_only','02e723369619f264832fb0466aabd9819cc005774bdba6389c5be8ad2f91c692','2026-10-21T11:32:22.274347+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (109,109,'葬送のフリーレン Coreful フィギュア フェルン(タイクレ限定) — 공식 메타데이터 발췌','https://www.taito.co.jp/taito-prize/0451852500','official_metadata_extract','und','name_original: 葬送のフリーレン Coreful フィギュア フェルン(タイクレ限定)
manufacturer: TAITO
product_line: Coreful
franchise: 葬送のフリーレン
character: フェルン','factual_metadata_only','090166ccc7754f7a4560e1d257e7a5d1a007cfd219ebe4b2f94cb6287fa6afce','2026-10-21T11:32:22.274351+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (110,110,'葬送のフリーレン Coreful フィギュア フリーレン~ドレスver.~ — 공식 메타데이터 발췌','https://www.taito.co.jp/taito-prize/0451950600','official_metadata_extract','und','name_original: 葬送のフリーレン Coreful フィギュア フリーレン~ドレスver.~
manufacturer: TAITO
product_line: Coreful
franchise: 葬送のフリーレン
character: フリーレン','factual_metadata_only','349e6b952f8474d9cfcdaed7f8b64813e5b655e113acca76b0cfe14047dad736','2026-10-21T11:32:22.274357+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (111,111,'葬送のフリーレン Coreful フィギュア フリーレン — 공식 메타데이터 발췌','https://www.taito.co.jp/en/taito-prize/0451972800','official_metadata_extract','und','name_original: 葬送のフリーレン Coreful フィギュア フリーレン
manufacturer: TAITO
product_line: Coreful
franchise: 葬送のフリーレン
character: フリーレン','factual_metadata_only','a2ab0aebb683ae120b11982ae9768beb1949e5e439c1027eb4739cb8de673e58','2026-10-21T11:32:22.274525+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (112,112,'【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(スカーレット・スパイダー・スーツ版) — 공식 메타데이터 발췌','https://www.hottoys.jp/item/view/100008115.php','official_metadata_extract','und','name_original: 【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(スカーレット・スパイダー・スーツ版)
manufacturer: Hot Toys
product_line: Video Game Masterpiece
scale: 1/6
height_mm: 300','factual_metadata_only','e60793423c581a46a280e6a255faa7269e3bda9451c7947745d917bd1b68c71f','2026-10-21T11:32:22.274532+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (113,113,'【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(スパイダー・パンク・スーツ版) — 공식 메타데이터 발췌','https://www.hottoys.jp/item/view/100007491.php','official_metadata_extract','und','name_original: 【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(スパイダー・パンク・スーツ版)
manufacturer: Hot Toys
product_line: Video Game Masterpiece
scale: 1/6
height_mm: 300','factual_metadata_only','6e9fe9e55c48f5cc38cdd2c0eb644e300f89a94cbe904889da5a700f20b1d81c','2026-10-21T11:32:22.274536+08:00');
INSERT INTO "source_documents" ("id","variant_id","title","url","source_type","language","body","usage_status","content_hash","collected_at") VALUES (114,114,'【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(クラシック・スーツ版) — 공식 메타데이터 발췌','https://www.hottoys.jp/item/view/100009109','official_metadata_extract','und','name_original: 【ビデオゲーム・マスターピース】 『Marvel’s Spider-Man』 1/6スケールフィギュア スパイダーマン(クラシック・スーツ版)
manufacturer: Hot Toys
product_line: Video Game Masterpiece
scale: 1/6
height_mm: 300','factual_metadata_only','2f1433b573f5af7aa7d6574324154cc1ef2f56921aa782c8daa98accb7ae629e','2026-10-21T11:32:22.274539+08:00');
SELECT setval(pg_get_serial_sequence('source_documents','id'), (SELECT MAX(id) FROM source_documents), true);

CREATE TABLE used_listings (
	id SERIAL NOT NULL, 
	variant_id INTEGER NOT NULL, 
	marketplace_id INTEGER NOT NULL, 
	listing_url TEXT NOT NULL, 
	asking_price NUMERIC(14, 2) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	condition VARCHAR(60) NOT NULL, 
	listing_status VARCHAR(40) NOT NULL, 
	is_set BOOLEAN NOT NULL, 
	match_status VARCHAR(40) NOT NULL, 
	region VARCHAR(120), 
	observed_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (listing_url, observed_at), 
	CHECK (asking_price >= 0), 
	FOREIGN KEY(variant_id) REFERENCES figure_variants (id), 
	FOREIGN KEY(marketplace_id) REFERENCES used_marketplaces (id)
)

;
CREATE INDEX ix_used_listings_variant_id ON used_listings (variant_id);
CREATE TABLE alembic_version (version_num VARCHAR(32) PRIMARY KEY);
INSERT INTO alembic_version VALUES ('cac17c89def2');
COMMIT;
