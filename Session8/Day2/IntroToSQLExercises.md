# Introduction to SQL Exercises

The problems associated with the Introduction to SQL lecture required the execution of queries on the [CasJobs](https://skyserver.sdss.org/CasJobs/) interface pointing to the SDSS database. For this reason, there is no associated jupyter notebook. 

Students were asked to solve the following problems: 

1.	Write two versions of a query to get the objID, specObjID, ra, dec, ugriz mags+errors and redshift for the first 1000 objects that have spectra, one without a JOIN and one with a JOIN. You can run it in SkyServer or CasJobs on SDSS DR15.
2.	Modify the second version of the query in 1) to include objects that don’t have spectra associated with them. Compare the results with 1).
3.	Run a Quick query in the CasJobs DR15 context to get the objID, ra, dec for the first 100 imaging objects with ra,dec between (180.0, -0.5) and (181.0, -0.4). Save the result in a MyDB table called MyObjs.
4.	Add an int enumerator column called “id” to MyObjs, see the CasJobs FAQ entry for adding an enumerator to a table.
5.	Write 2 versions of a query to find the nearest neighbor for each of the objects in MyObjs. One of the versions should use the CROSS APPLY operator, the other version should use just a plain JOIN.
6.	Run each of the queries (using the Submit button, not Quick) and save results in tables MyNbrs1 and MyNbrs2 resp.. Compare the contents of the two tables.
7.	Create a (max 1000 rows) table in CasJobs for the functions that we created in class.
8.	Create a “poor man’s luminosity function” for objects between z=0.3 and 0.4, using only reliable spectra and excluding invalid magnitudes, and without using a JOIN.