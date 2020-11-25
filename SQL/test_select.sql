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

