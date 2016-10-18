drop table if exists flunschs;
create table flunschs (
	id integer primary key autoincrement,
	title text not null,
	owner text not null,
	desc text
);
