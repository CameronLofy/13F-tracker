use test_hedgetracker;


-- SELECT H.h_name, H.hedge_id, F.f_type, F.date, F.period
-- FROM hedge_fund AS H, form AS F
-- WHERE H.hedge_id=F.hedge_id
-- ORDER BY H.hedge_id;

-- SELECT *
-- FROM holdings
-- WHERE holdings.form_id = 
-- 	(SELECT form_id
--     FROM form, hedge_fund
--     WHERE form.period = 
-- 		(SELECT MAX(form.period)
--         FROM form
--         WHERE form.hedge_id = 1067983
--         )
-- 	);
    
-- SELECT hedge.h_name, s.s_name, s.ticker, h.shares, h.value
-- FROM holdings as h
-- JOIN hedge_fund as hedge
-- ON h.hedge_id = hedge.hedge_id
-- JOIN stock as s
-- ON s.cusip = h.cusip
-- WHERE form_id = (
-- 	SELECT form_id
-- 	FROM form
-- 	WHERE form.hedge_id = 1067983 AND form.period = 
-- 		(SELECT form.period
-- 		FROM form, hedge_fund
-- 		WHERE form.hedge_id = hedge_fund.hedge_id
--         ORDER BY form.period DESC LIMIT 1
-- 		)
-- 	)
-- ORDER BY s.s_name ASC;


-- SELECT hedge.h_name, s.s_name, s.ticker, h.shares, h.value
-- FROM holdings as h
-- JOIN hedge_fund as hedge
-- ON h.hedge_id = hedge.hedge_id
-- JOIN stock as s
-- ON h.cusip = s.cusip
-- WHERE form_id = (
-- 	SELECT form_id
-- 	FROM form
-- 	WHERE form.hedge_id = 1067983 AND form.period = 
-- 		'2020-09-30'
-- 	)
-- ORDER BY s.s_name ASC;


SELECT *
FROM holdings as h
JOIN hedge_fund as hedge
ON hedge.hedge_id = h.hedge_id
JOIN stock
ON h.cusip = stock.cusip
WHERE h.form_id = (
	SELECT form_id
	FROM form
	WHERE form.hedge_id = 1067983 AND form.period = 
		'2020-09-30'
	)
