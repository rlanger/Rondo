drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title string not null,
	description string not null,
	start_datetime datetime not null,
	location string not null
);