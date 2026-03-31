--1) How many containers of antibiotics are currently available?
SELECT quantityOnHand FROM item WHERE itemDescription ='bottle of antibiotics';
/*2) Which volunteer(s), if any, have phone numbers that do not start with the number 2 and
whose last name is not Jones. Query should retrieve names rather than ids.*/
SELECT volunteerName FROM volunteer
WHERE volunteerTelephone NOT LIKE '2%'
AND volunteerName NOT LIKE '% Jones';
/*3) Which volunteer(s) are working on transporting tasks? Query should retrieve names
rather than ids. */
SELECT volunteer FROM volunteertask
WHERE taskType = 'transporting';
/*4) Which task(s) have yet to be assigned to any volunteers (provide task descriptions, not
the codes?*/
SELECT taskDescription FROM task
WHERE taskCode NOT IN (SELECT taskCode FROM assignment);
--5) Which type(s) of package contain some kind of bottle?
SELECT DISTINCT pt.packageTypeName
FROM package_type pt
JOIN package p
    ON pt.packageTypeId = p.packageTypeId
JOIN package_contents pc
    ON p.packageId = pc.packageId
JOIN item i
    ON pc.itemId = i.itemId
WHERE i.itemDescription LIKE '%bottle%';
--6) Which items, if any, are not in any packages? Answer should be item descriptions.
SELECT i.itemDescription
FROM item i
LEFT JOIN package_contents pc
    ON i.itemId = pc.itemId
WHERE pc.packageId IS NULL;
/*7) Which task(s) are assigned to volunteer(s) that live in New Jersey (NJ)? Answer should
have the task description and not the task ids.*/
SELECT DISTINCT t.taskDescription
FROM task t
JOIN assignment a
    ON t.taskCode = a.taskCode
JOIN volunteer v
    ON a.volunteerId = v.volunteerId
WHERE v.volunteerAddress LIKE '%NJ%';
/*8) Which volunteers began their assignments in the first half of 2021? Answer should have
the volunteer names and not their ids.*/
SELECT DISTINCT v.volunteerName
FROM volunteer v
JOIN assignment a
    ON v.volunteerId = a.volunteerId
WHERE a.startDateTime >= '2021-01-01'
  AND a.startDateTime < '2021-07-01';
/*9) Which volunteers have been assigned to tasks that include packing spam? Answer
should have the volunteer names and not their ids.*/
SELECT DISTINCT v.volunteerName
FROM volunteer v
JOIN assignment a
    ON v.volunteerId = a.volunteerId
JOIN package p
    ON a.taskCode = p.taskCode
JOIN package_contents pc
    ON p.packageId = pc.packageId
JOIN item i
    ON pc.itemId = i.itemId
WHERE i.itemDescription = 'can of spam';
/*10) Which item(s) (if any) have a total value of exactly $100 in one package? Answer should
be item descriptions.*/
SELECT DISTINCT i.itemDescription
FROM item i
JOIN package_contents pc
    ON i.itemId = pc.itemId
WHERE i.itemValue * pc.itemQuantity = 100;

/*11) How many volunteers are assigned to tasks with each different status? The answer
should show each different status and the number of volunteers sorted from highest to
lowest)*/
SELECT ts.taskStatusName,
       COUNT(DISTINCT a.volunteerId) AS volunteerCount
FROM assignment a
JOIN task t
    ON a.taskCode = t.taskCode
JOIN task_status ts
    ON t.taskStatusId = ts.taskStatusId
GROUP BY ts.taskStatusName
ORDER BY volunteerCount DESC;
/*12) Which task creates the heaviest set of packages and what is the weight? Show both the
taskCode and the weight (You should be able to do this without using any sub-queries).*/
SELECT taskCode,
       SUM(packageWeight) AS totalWeight
FROM package
GROUP BY taskCode
ORDER BY totalWeight DESC
LIMIT 1;

--13) How many tasks are there that do not have a type of “packing”?
SELECT COUNT(*) AS numberOfTasks
FROM task t
JOIN task_type tt
    ON t.taskTypeId = tt.taskTypeId
WHERE tt.taskTypeName <> 'packing';
/*14) Of those items that have been packed, which item (or items) were touched by fewer
than 3 volunteers? Answer should be item descriptions.*/
SELECT i.itemDescription
FROM item i
JOIN package_contents pc
    ON i.itemId = pc.itemId
JOIN package p
    ON pc.packageId = p.packageId
LEFT JOIN assignment a
    ON p.taskCode = a.taskCode
GROUP BY i.itemId, i.itemDescription
HAVING COUNT(DISTINCT a.volunteerId) < 3;
/*15) Which packages have a total value of more than 100? Show the packageIds and their
value sorted from lowest to highest.*/
SELECT pc.packageId,
       SUM(i.itemValue * pc.itemQuantity) AS totalValue
FROM package_contents pc
JOIN item i
    ON pc.itemId = i.itemId
GROUP BY pc.packageId
HAVING SUM(i.itemValue * pc.itemQuantity) > 100
ORDER BY totalValue ASC;

