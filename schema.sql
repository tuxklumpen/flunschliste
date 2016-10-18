drop table if exists flunscher;
drop table if exists flunschs;
create table flunscher (
	id integer primary key autoincrement,
	name text not null
);
create table flunschs (
	id integer primary key autoincrement,
	title text not null,
	owner integer not null,
	desc text
);
