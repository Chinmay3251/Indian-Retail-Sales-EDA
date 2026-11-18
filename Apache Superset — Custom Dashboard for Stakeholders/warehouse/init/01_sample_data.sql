CREATE TABLE IF NOT EXISTS sample_sales (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    category VARCHAR(60) NOT NULL,
    product VARCHAR(100) NOT NULL,
    region VARCHAR(30) NOT NULL,
    quantity INTEGER NOT NULL,
    revenue NUMERIC(12,2) NOT NULL,
    profit NUMERIC(12,2) NOT NULL
);

INSERT INTO sample_sales (order_date, category, product, region, quantity, revenue, profit) VALUES
('2026-01-05','Electronics','Headphones','North',12,24000,4800),
('2026-01-08','Furniture','Desk','West',5,35000,7000),
('2026-01-12','Office Supplies','Notebook','South',40,8000,2400),
('2026-02-03','Electronics','Keyboard','East',15,18000,3600),
('2026-02-11','Furniture','Chair','North',8,28000,5600),
('2026-02-18','Office Supplies','Pen Set','West',30,4500,1200),
('2026-03-04','Electronics','Mouse','South',25,12500,2500),
('2026-03-09','Furniture','Shelf','East',7,21000,4200),
('2026-03-17','Office Supplies','Folder','North',50,5000,1500),
('2026-04-02','Electronics','Monitor','West',6,42000,8400),
('2026-04-07','Furniture','Table','South',4,32000,6400),
('2026-04-15','Office Supplies','Stapler','East',18,3600,1080),
('2026-05-01','Electronics','Speaker','North',10,22000,4400),
('2026-05-12','Furniture','Cabinet','West',3,24000,4800),
('2026-05-22','Office Supplies','Marker','South',35,7000,2100),
('2026-06-02','Electronics','Camera','East',4,56000,11200),
('2026-06-10','Furniture','Bookcase','North',6,18000,3600),
('2026-06-18','Office Supplies','Paper','West',60,9000,2700),
('2026-07-03','Electronics','Tablet','South',7,49000,9800),
('2026-07-11','Furniture','Sofa','East',2,40000,8000),
('2026-07-19','Office Supplies','Whiteboard','North',9,13500,4050);
