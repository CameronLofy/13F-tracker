use test_hedgetracker;
SELECT H.h_name, H.hedge_id, F.f_type, F.date, F.period
FROM hedge_fund AS H, form AS F
WHERE H.hedge_id=F.hedge_id
ORDER BY H.hedge_id
