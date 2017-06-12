#Schema for attempts and user IDs
drop table if exists entries;
create table entries (
  id integer primary key,
  attempt1 text not null,
  attempt2 text not null,
  attempt3 text not null,
  attempt4 text not null,
  attempt5 text not null,
  checked integer default 
  #sqlite does not have booleans, use integers 0/1
);