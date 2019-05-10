# Introduction to SQL Exercises –– Solutions

The problems associated with the Introduction to SQL lecture required the execution of queries on the [CasJobs](https://skyserver.sdss.org/CasJobs/) interface pointing to the SDSS database. For this reason, there is no associated jupyter notebook. 

Students were asked to solve the following problems: 

1.	Write two versions of a query to get the objID, specObjID, ra, dec, ugriz mags+errors and redshift for the first 1000 objects that have spectra, one without a JOIN and one with a JOIN. You can run it in SkyServer or CasJobs on SDSS DR15.
    
    The version without a JOIN uses a pre-computed join between specobjall and photoobjall, called SpecPhotoAll.  I have actually used a view of SpecPhotoAll called SpecPhoto that contains the “good” observations. Also, there are a whole bunch of magnitude measurements in the 5 SDSS bands that you can choose from, but generally the modelMag is the best choice if you’re not sure.
        
        SELECT TOP 1000
			sp.objID, sp.specObjID, sp.ra, sp.dec, 
            sp.modelMag_u, sp.modelMag_g, sp.modelMag_r, sp.modelMag_i, sp.modelMag_z, 
            sp.modelMagErr_u, sp.modelMagErr_g, sp.modelMagErr_g, sp.modelMagErr_i, sp.modelMagErr_z, 
            sp.z
		FROM SpecPhoto sp

    In the second version, the join is between PhotoObj and SpecObj, which are similarly the “good” observations views of PhotoObjAll and SpecObjAll. Note, as mentioned in class, the way to join is via the bestobjid foreign key in the spectrum table.

        SELECT TOP 1000 
            p.objID, s.specObjID, p.ra, p.dec, 
            p.modelMag_u, p.modelMag_g, p.modelMag_r, p.modelMag_i, p.modelMag_z, 
            p.modelMagErr_u, p.modelMagErr_g, p.modelMagErr_g, p.modelMagErr_i, p.modelMagErr_z, 
            s.z
        FROM PhotoObj p 
        JOIN SpecObj s ON s.bestObjID = p.objID

2.	Modify the second version of the query in 1) to include objects that don’t have spectra associated with them. Compare the results with 1). 

    If you want to include objects that don’t have spectra, you need to do an OUTER JOIN instead of the regular join, so the query would be:

        SELECT TOP 1000 
    	    p.objID, s.specObjID, p.ra, p.dec, 
            p.modelMag_u, p.modelMag_g, p.modelMag_r, p.modelMag_i, p.modelMag_z, 
            p.modelMagErr_u, p.modelMagErr_g, p.modelMagErr_g, p.modelMagErr_i, p.modelMagErr_z, 
            s.z
        FROM PhotoObj p 
        LEFT OUTER JOIN SpecObj s ON s.bestObjID = p.objID

    When you compare the results with 1b) above, what do you see?  Do you see any specobjids that are non-NULL? Why not? (hint: what percentage of imaging is covered by spectroscopic follow-up in SDSS?)

3. Run a Quick query in the CasJobs DR15 context to get the objID, ra, dec for the first 100 imaging objects with ra,dec between (180.0, -0.5) and (181.0, -0.4). Save the result in a MyDB table called MyObjs.
	
        SELECT TOP 100
        	objID, ra, dec
        INTO MyDB.MyObjs
        FROM PhotoObj
        WHERE ra BETWEEN 180 and 181
           AND dec between -0.5 and -0.4

4.	Add an int enumerator column called “id” to MyObjs, see the CasJobs FAQ entry for adding an enumerator to a table. 

    As per the Enumerator Column example on the Advanced CasJobs Queries help page, here is the SQL code (should be run in the MyDB context, in Quick mode) to add an extra enumerator column to the table above:

        CREATE TABLE MyObjs2 (
        	id INT identity(1,1),
        objID BIGINT,	
        ra FLOAT,
        	dec FLOAT
        )
        GO
        INSERT MyObjs2 ( objid, ra, dec )
        SELECT objID, ra,dec
        FROM MyObjs

    Once you are done running the above code, you can delete the MyObjs table and rename MyObjs2 to MyObjs, using the Drop and Rename menu buttons on the MyDB page (Drop MyObjs and Rename MyObjs2 to MyObjs). 

5.	Write 2 versions of a query to find the nearest neighbor for each of the objects in MyObjs. One of the versions should use the CROSS APPLY operator, the other version should use just a plain JOIN.

    CROSS APPLY solution:

		SELECT a.id, a.objid as objid1, b.objid as objid2
        INTO MyDB.MyNbrs1
        FROM MyDB.MyObjs a
        CROSS APPLY dbo.fGetNearestObjEq( a.ra, a..dec, 1.0 ) b  
    
    However, there’s a problem when you examine the output: quite a few of the matched objects are self-matches!  One way to get rid of the self-matches is using the following variant of the above query, which uses a nested query in the CROSS APPLY:

        SELECT a.id, a.objid as objid1, b.objid as objid2
        INTO MyDB.MyNbrs1
        FROM MyDB.MyObjs a
          CROSS APPLY (SELECT TOP 1 objid 
              FROM dbo.fGetNearbyObjEq( a.ra, a..dec, 1.0 ) 
              WHERE objid != a.objID ORDER BY distance) b

    For the JOIN version, as in 1), you should look for a precomputed option, which in this case is the Neighbors table containing the precomputed neighbors within 30” of each object in PhotoObjAll.  Here is that version of the query, and there are examples of using the Neighbors table in the queries shown in class. Note that the “nearest” (rather than all nearby objects within 30”) requires an additional twist to this query, in the WHERE clause.

        SELECT a.id, a.objid as objid1, b.neighborobjid as objid2 
        INTO MyDB.MyNbrs2
        FROM MyDB.MyObjs a
          JOIN Neighbors b ON b.objid=a.objid
        WHERE 
        b.distance = (SELECT min(distance) from Neighbors n 
        WHERE n.objid=a.objid)     -- find the closest neighbor

6.	Run each of the queries (using the Submit button, not Quick) and save results in tables MyNbrs1 and MyNbrs2 resp. Compare the contents of the two tables. 

    You will probably see 100 rows in each of the two tables, meaning that matches were found for each object, but in the second table you might find the order being haphazard. You should check if the same neighbors were found in each case.
    
7.	Create a (max 1000 rows) table in CasJobs for the functions that we created in class.

	The functions we created in class where the MaxDataX and MaxNDataX functions:

    	CREATE FUNCTION MaxDataX (@ymin float)
        RETURNS FLOAT AS
        BEGIN
        		DECLARE @x float = null;
        		SELECT TOP 1 @x = x
        		FROM MyData
        		WHERE y > @ymin
        		ORDER BY X DESC
        		RETURN @x;
        END
        GO
	
	and:

        CREATE FUNCTION dbo.MaxNDataX(@ymin float, @n int)
        RETURNS @ret TABLE (
        	MaxX float not null
        ) AS
        BEGIN
        	INSERT @ret SELECT TOP (@n) X
        		FROM MyData
        		WHERE y > @ymin
        	RETURN;
        END
        GO

    To create a table called MyData with 1000 rows, you can either get the x, y, values from one of the tables in SDSS, or you can generate the values using a random number generator.   Using the simpler option, here is how to get it from SDSS, which has the Cartesian coordinates in the photo tables as cx, cy.  We use the PhotoTag view of the PhotoObjAll table since we only really want the 2 columns, and we also use the implicit table creation syntax (SELECT … INTO rather than INSERT … SELECT). Run this in the SDSS DR15 context:

        SELECT TOP 1000 cx as x, cy as y
        INTO MyDB.MyData
        FROM PhotoTag  -- the vertical partition view of PhotoObjAll with much fewer columns

    Now you can run the test queries from the slide shown in class (or your own tests), in the MyDB context:

        select dbo.MaxDataX(PI()/10)
        select dbo.MaxDataX(99999)
        select f.* from webuser.MaxNDataX(-2,5) as f

8.	Create a “poor man’s luminosity function” for objects between z=0.3 and 0.4, using only reliable spectra and excluding invalid magnitudes, and without using a JOIN.

    This is a gimme (and it’s fine if you cheat!) - there is actually an example of how you’d do a simple luminosity function with the r magnitude using the Photoz (photometric redshift) table in the Sample SQL Queries page on SkyServer.  The point is for you to learn how to do a basic histogram. It introduces the ROUND() function (in this case, rounding to 1 decimal place).  We need the Photoz table because the SDSS pipeline outputs don’t have absolute magnitudes in them. You’ll need to run this query in Submit mode in the DR15 context.

        SELECT round(absMagR,1) as absMagR, COUNT(*) as n
        FROM Photoz
        WHERE
         	z BETWEEN 0.4 and 0.5
         	and photoErrorClass=1 and nnCount>95
         	and zErr BETWEEN 0 and 0.03
        group by round(absMagR,1)
        order by round(absMagR,1) 

