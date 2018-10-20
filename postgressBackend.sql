

create table tree(
    id serial primary key,
    letter char,
    path ltree
);
create index tree_path_idx on tree using gist (path);


insert into tree (letter, path) values ('A', 'A');
insert into tree (letter, path) values ('B', 'A.B');
insert into tree (letter, path) values ('C', 'A.C');
insert into tree (letter, path) values ('D', 'A.C.D');
insert into tree (letter, path) values ('E', 'A.C.E');
insert into tree (letter, path) values ('F', 'A.C.F');
insert into tree (letter, path) values ('G', 'A.B.G');


/*what if I needed to know how many children A had, recursively?
 That is, what if I needed to count its children, grandchildren, 
 great-grandchildren, etc.? @> solves this problem for us. I 
 can now recursively count the total number of nodes under 
 any given parent like this:*/ 

select count(*) from tree where PARENT-PATH @> path;


/*  suppose I wanted to “cut off this branch” of the tree, so to speak.
How can I do this? Simple! I just use a SQL delete statement. Note that 
 we can use @> equally well in delete statements as in select statements. */ 
delete from tree where 'A.C' @> path;

/*The power of the @> operator is that it allows Postgres
 to search efficiently across an entire tree using an index. 
 Saying this in a more technical way: The @> operator integrates
  with Postgres’s GiST index API to find and match descendant 
  nodes. To take advantage of this technology, be sure to 
  create a GiST index on your ltree column, for example like this:
*/ 
create index tree_path_idx on tree using gist (path);


update tree set path = DESTINATION_PATH || subpath(path, nlevel(SOURCE_PATH)-1)
where path <@ SOURCE_PATH;


/* One last puzzle: How can I copy a tree branch instead of moving it? 
I just use an insert SQL statement instead of update. Simple, right?
using LTREE functions and operators, I can achieve this using a single 
SQL statement! I just have to write SQL that will insert the result 
of a select, like this:*/

insert into tree (letter, path) (
    select letter, 'A.B.G' || subpath(path, 1) from tree where 'A.C' @> path
)