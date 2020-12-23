use test_hedgetracker;

-- select * from form
-- where date = '2020-11-16'
-- ;

-- SELECT *, COUNT(*) 
-- FROM stock
-- GROUP BY ticker, CUSIP
-- HAVING COUNT(*) > 0;

-- SELECT *
-- FROM stock
-- WHERE ticker = 'T';

SELECT *
FROM form
ORDER BY hedge_id, period DESC;

-- SELECT *
-- FROM stock

SELECT *
FROM holdings;

-- SELECT s.s_name, h.cusip, h.shares, h.value
-- FROM holdings as h
-- RIGHT JOIN stock as s
-- ON s.CUSIP = h.cusip

SELECT *
FROM stock;