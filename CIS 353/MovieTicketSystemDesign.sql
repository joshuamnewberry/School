----- 1. Create Tables

-- Create CUSTOMER table
CREATE TABLE CUSTOMER (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15),
    JoinDate DATE
);

-- Create PREMIUM_ACCOUNT table (1:N with CUSTOMER)
CREATE TABLE PREMIUM_ACCOUNT (
    AccountID INT PRIMARY KEY,
    CustomerID INT UNIQUE,
    LoyaltyPoints INT,
    RenewalDate DATE,
    DiscountRate NUMERIC(3, 2),
    VIPLoungeAccess BOOLEAN,
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID)
);

-- Create MOVIE table
CREATE TABLE MOVIE (
    MovieID INT PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    Genre VARCHAR(50),
    Duration INT, -- Duration in minutes
    ReleaseDate DATE
);

-- Create BOOKING table (1:M from CUSTOMER)
CREATE TABLE BOOKING (
    BookingID INT PRIMARY KEY,
    CustomerID INT,
    TotalPrice NUMERIC(6, 2) NOT NULL,
    Timestamp TIMESTAMP NOT NULL,
    PaymentMethod VARCHAR(20),
    Status VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID)
);

-- Create BOOKING_MOVIE table (M:N mapping between BOOKING and MOVIE)
CREATE TABLE BOOKING_MOVIE (
    BookingID INT,
    MovieID INT,
    PRIMARY KEY (BookingID, MovieID),
    FOREIGN KEY (BookingID) REFERENCES BOOKING(BookingID),
    FOREIGN KEY (MovieID) REFERENCES MOVIE(MovieID)
);

----- 2. Insert Sample Data

-- Insert 5 Customers
INSERT INTO CUSTOMER (CustomerID, Name, Email, Phone, JoinDate)
VALUES (1, 'Alice Smith', 'alice@email.com', '555-0101', DATE '2025-01-15');
INSERT INTO CUSTOMER (CustomerID, Name, Email, Phone, JoinDate)
VALUES (2, 'Bob Johnson', 'bob.j@email.com', '555-0102', DATE '2025-03-22');
INSERT INTO CUSTOMER (CustomerID, Name, Email, Phone, JoinDate)
VALUES (3, 'Charlie Davis', 'charlie@email.com', '555-0103', DATE '2025-06-10');
INSERT INTO CUSTOMER (CustomerID, Name, Email, Phone, JoinDate)
VALUES (4, 'Diana Prince', 'diana@email.com', '555-0104', DATE '2025-08-05');
INSERT INTO CUSTOMER (CustomerID, Name, Email, Phone, JoinDate)
VALUES (5, 'Evan Wright', 'evan.w@email.com', '555-0105', DATE '2026-01-20');

-- Insert 5 Premium Accounts
INSERT INTO PREMIUM_ACCOUNT (AccountID, CustomerID, LoyaltyPoints, RenewalDate, DiscountRate, VIPLoungeAccess)
VALUES (101, 1, 1500, DATE '2027-01-15', 0.15, TRUE);
INSERT INTO PREMIUM_ACCOUNT (AccountID, CustomerID, LoyaltyPoints, RenewalDate, DiscountRate, VIPLoungeAccess)
VALUES (102, 3, 500, DATE '2026-06-10', 0.05, FALSE);
INSERT INTO PREMIUM_ACCOUNT (AccountID, CustomerID, LoyaltyPoints, RenewalDate, DiscountRate, VIPLoungeAccess)
VALUES (103, 4, 3200, DATE '2027-08-05', 0.20, TRUE);
INSERT INTO PREMIUM_ACCOUNT (AccountID, CustomerID, LoyaltyPoints, RenewalDate, DiscountRate, VIPLoungeAccess)
VALUES (104, 5, 100, DATE '2027-01-20', 0.05, FALSE);
INSERT INTO PREMIUM_ACCOUNT (AccountID, CustomerID, LoyaltyPoints, RenewalDate, DiscountRate, VIPLoungeAccess)
VALUES (105, 2, 850, DATE '2027-03-22', 0.10, TRUE);

-- Insert 5 Movies
INSERT INTO MOVIE (MovieID, Title, Genre, Duration, ReleaseDate)
VALUES (1001, 'Galactic Wars', 'Sci-Fi', 135, DATE '2025-11-20');
INSERT INTO MOVIE (MovieID, Title, Genre, Duration, ReleaseDate)
VALUES (1002, 'The Silent Hill', 'Horror', 110, DATE '2026-02-14');
INSERT INTO MOVIE (MovieID, Title, Genre, Duration, ReleaseDate)
VALUES (1003, 'Laugh Out Loud', 'Comedy', 95, DATE '2026-03-01');
INSERT INTO MOVIE (MovieID, Title, Genre, Duration, ReleaseDate)
VALUES (1004, 'Desert Run', 'Action', 120, DATE '2026-04-10');
INSERT INTO MOVIE (MovieID, Title, Genre, Duration, ReleaseDate)
VALUES (1005, 'Historical Echoes', 'Documentary', 105, DATE '2025-09-15');

-- Insert 5 Bookings
INSERT INTO BOOKING (BookingID, CustomerID, TotalPrice, Timestamp, PaymentMethod, Status)
VALUES (5001, 1, 35.50, TIMESTAMP '2026-04-20 14:30:00', 'Credit Card', 'Completed');
INSERT INTO BOOKING (BookingID, CustomerID, TotalPrice, Timestamp, PaymentMethod, Status)
VALUES (5002, 2, 18.00, TIMESTAMP '2026-04-21 18:15:00', 'PayPal', 'Completed');
INSERT INTO BOOKING (BookingID, CustomerID, TotalPrice, Timestamp, PaymentMethod, Status)
VALUES (5003, 1, 50.00, TIMESTAMP '2026-04-22 10:00:00', 'Credit Card', 'Completed');
INSERT INTO BOOKING (BookingID, CustomerID, TotalPrice, Timestamp, PaymentMethod, Status)
VALUES (5004, 4, 25.00, TIMESTAMP '2026-04-23 19:45:00', 'Debit Card', 'Cancelled');
INSERT INTO BOOKING (BookingID, CustomerID, TotalPrice, Timestamp, PaymentMethod, Status)
VALUES (5005, 5, 45.00, TIMESTAMP '2026-04-24 20:00:00', 'Credit Card', 'Completed');

-- Insert 5 Booking-Movie associations (Resolving M:N)
INSERT INTO BOOKING_MOVIE (BookingID, MovieID)
VALUES (5001, 1001);
INSERT INTO BOOKING_MOVIE (BookingID, MovieID)
VALUES (5001, 1004);
INSERT INTO BOOKING_MOVIE (BookingID, MovieID)
VALUES (5002, 1003);
INSERT INTO BOOKING_MOVIE (BookingID, MovieID)
VALUES (5003, 1001);
INSERT INTO BOOKING_MOVIE (BookingID, MovieID)
VALUES (5004, 1002);
INSERT INTO BOOKING_MOVIE (BookingID, MovieID)
VALUES (5005, 1004);

----- 3. Sample Clientele Questions

-- Question 1: Which customers have made a completed booking,
-- and what payment method did they use?
SELECT c.Name, b.BookingID, b.PaymentMethod
FROM CUSTOMER c
JOIN BOOKING b ON c.CustomerID = b.CustomerID
WHERE b.Status = 'Completed';

-- Question 2: Which movies in our catalog have currently never
-- been booked by any customer?
SELECT Title, Genre 
FROM MOVIE 
WHERE MovieID NOT IN (
    SELECT DISTINCT MovieID 
    FROM BOOKING_MOVIE
);

-- Question 3: Which customers have spent more on a single booking
-- than the average price of all bookings in the system?
SELECT c.Name, b.TotalPrice
FROM CUSTOMER c
JOIN BOOKING b ON c.CustomerID = b.CustomerID
WHERE b.TotalPrice > (
    SELECT AVG(TotalPrice) 
    FROM BOOKING
);

-- Question 4: What is the total number of movie tickets booked for each
-- genre based on completed bookings?
SELECT m.Genre, COUNT(bm.MovieID) AS TicketsSold
FROM MOVIE m
JOIN BOOKING_MOVIE bm ON m.MovieID = bm.MovieID
JOIN BOOKING b ON bm.BookingID = b.BookingID 
WHERE b.Status = 'Completed'
GROUP BY m.Genre
ORDER BY TicketsSold DESC;

-- Question 5: Provide the names and email addresses of customers who
-- booked an 'Action' movie and currently have access to the VIP Lounge.
SELECT DISTINCT c.Name, c.Email
FROM CUSTOMER c
JOIN PREMIUM_ACCOUNT p ON c.CustomerID = p.CustomerID
JOIN BOOKING b ON c.CustomerID = b.CustomerID
JOIN BOOKING_MOVIE bm ON b.BookingID = bm.BookingID
JOIN MOVIE m ON bm.MovieID = m.MovieID
WHERE p.VIPLoungeAccess = TRUE 
AND m.Genre = 'Action';