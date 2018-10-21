/* Each username must map to a password and a list of Templates. 
We must have tuples of form (userId, templateList)
Where templateList is a list of tuples with the form (templateName, rootNode).
rootNode references the root node of the tree corresponding to a given template name. 

Each tree consists of a series of sub-trees defined below. 
*/ 




/*Must create Tree "objects" each of which contains:

treeId- an id number for the current node and it's subtree
goalString - the actual content of the user's goal or sub-goal
isComplete- a boolean indicating whether the goal is complete or not
upperTimeBound-  a tuple of ints corresponding to the user's self-set upper time bound (hours, minutes) or an interval(if it will work)
lowerTimeBound-  a tuple of ints corresponding to the user's self-set lower time bound (hours, minutes) or an interval(if it will work)
elapsedTime- quadruple of ints corresponding to (days, hours, minutes, seconds) or an interval(if it will work)



*/ 
create table Users(
  username TEXT primary key, 
  password TEXT, 
)


/*Each row of the tree table is a Node and can be thought of
 as the root node of a subtree*/
create table Tree(
    id serial primary key,
    username TEXT, 
    templateName TEXT,

    isRoot boolean, 

    goalString TEXT, 
    isComplete boolean, 

    /*interval should be registering as a keyword here */ 
    upperTimeBound interval, 
    lowerTimeBound interval, 
    elapsedTime  interval, 

    /*specification of path from root node to current node*/
    path ltree
);
create index tree_path_idx on Tree using gist (path);



-- /*This is the most dangerous location for a bug so far*/ 
-- CREATE FUNCTION ins_Id_Into_Path(ltree, int, intid) RETURNS ltree
--    AS 'select subpath($1,0,$2) || $3 || subpath($1,$2);' 
--    LANGUAGE SQL IMMUTABLE;


/*This is an insert function but it needs to be re-written in proper SQL */ 
CREATE FUNCTION ins_Node_Into_Tree(ltree, int, int/*parentId*/, childId, childGoalString, childIsComplete, childUpperTimeBound, childLowerTimeBound, childElapsedTime,
      parentPath || childId)) 
  RETURNS ltree
    BEGIN 
    parentPath := SELECT path FROM Tree WHERE id = parentId;
   /* AS 'select subpath($1,0,$2) || $3 || subpath($1,$2);'*/ 
   INSERT INTO subTree(id, goalString, isComplete,upperTimeBound, lowerTimeBound, elapsedTime, path )
   VALUES (childId, childGoalString, childIsComplete, childUpperTimeBound, childLowerTimeBound, childElapsedTime,
      parentPath || childId)  /* Updates the path of the new node*/

   END 
    LANGUAGE SQL IMMUTABLE;

ltreetest=> SELECT ins_label(path,2,'Space') FROM test WHERE path <@ 'Top.Science.Astronomy';
                ins_label


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


/* I need to update the path of rootNode and each of its descendants all in
 a single operation. But how can I do this? Two LTREE functions, NLEVEL() 
 and SUBPATH(), can help. */ 
 /*First, NLEVEL.It simply counts the number of levels in each path string; 
 internally, it parses the path string for period characters.
  As you might guess, this returns the number of levels 
 in a given path string: */ 
select letter, path, nlevel(path) from tree;



/*LTREE provides another new SQL function that will also help
 us write a general tree path formula: SUBPATH. As you might
  guess, this returns a selected substring from a given path. */ 
  select NODE, subpath(path, OFFSET_FROM_TOPNODE) from tree where path <@ 'SUBPATH';



