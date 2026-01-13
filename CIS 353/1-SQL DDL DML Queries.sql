/*
Outline: 

(1) Data types: char, varchar, numeric, float, date, timestamp
(2) DDL: Create, alter, drop
(3) DML: insert, update, delete

*/

---------------CREATE---------------

create table vehicles (
 
 	make varchar(10), 
	model varchar(10), 
	year smallint, 
	mileage int,
	price numeric(10,2)
);
desc vehicles;



---------------ALTER---------------

--(Q1) ADD a column 'used' with varchar(3) datatype to the vehicles table

 

--(Q2) DROP the 'used' column from vehicles table



--(Q3) Drop the vechiles table


----------------------------------------------------------------------------------- 

CREATE TABLE employees (
	
	id CHAR(3),                  
	full_name VARCHAR(20), 
	emailid VARCHAR(30), 
	age SMALLINT,
	salary NUMERIC(9,2),
	address varchar(50)
);


desc employees;


---------------Insert (into, values)---------------

INSERT INTO employees(id, full_name, emailid, age, salary, address) VALUES ('111', 'James Smith', 'jsmith@gmail.com', 23, 84765.43, 'dodge st, MI');

INSERT INTO employees(id, full_name, emailid, age, salary, address) VALUES ('222', 'Mark Richard', 'mrichard@gmail.com', 27, 78765.43, 'dodge st, MI');

INSERT INTO employees(id, full_name, emailid, age, salary, address) VALUES ('333', 'David', 'david@gmail.com', 55, 98765.43, 'dodge st, MI');

INSERT INTO employees(id, full_name, emailid, age, salary, address) VALUES ('444', 'Sam', 'sam@gmail.com', 35, null, 'dodge st, MI');

INSERT INTO employees(id, full_name, emailid, age, salary) VALUES ('555', 'Kim', 'Kim@gmail.com', 34, 99999);

INSERT INTO employees(id, full_name, emailid, age, address) VALUES ('666', 'Maria', 'Maria@gmail.com', 35, 'pacific st, MI');

INSERT INTO employees VALUES ('777', 'Tom', 'Tom@gmail.com', 53, 198765.43, 'main st, MI');

INSERT INTO employees (id, full_name, emailid, salary, address) VALUES ('888', 'Vince', 'Vince@gmail.com', 198765.43, 'main st, MI');



--(Q4) display all the data from Employees table


--(Q5) find employees having age less than 35 with salary of at-least 85K


--(Q6) Delete all rows from employees  


--(Q7) delete employees having age greater than 50 or salary more than 5 digits


--(Q8) update address of all employees to  (Campus Dr, Allendale, MI);


--(Q9) update salary of new hires ('Sam' and 'Maria') to 125000



---------------Date and TimeStamp---------------


--(Q10) ADD a column 'date_hired' with date datatype to the employees table

 
--(Q11) ADD a column 'time_hired' with timestamp datatype to the employees table

 
--(Q12) update date_hired for Maria to Nov-23-2018


--(Q13) update time_hired for Sam to 2003/05/03 7:02:44 pm






