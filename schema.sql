create table users (
  id integer primary key autoincrement,
  username text not null,
  realname text not null,
  password text not null
);
create table news (
  id integer primary key autoincrement,
  title text not null,
  content text not null,
  date date not null
);
create table doorlogs (
  id integer primary key autoincrement,
  date date not null,
  description text not null,
  note text
);
insert into users (username, realname, password) values ('--Username--', '--Real Name--', '--Salted-PW-Hash-Here--');
