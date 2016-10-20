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
	description text
);
insert into flunscher (name) values ('Fabian');
insert into flunscher (name) values ('Marita');
insert into flunscher (name) values ('Hans-Jürgen');
