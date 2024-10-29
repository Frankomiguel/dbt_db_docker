{{
    config(materialized = 'table', 
    tags = ["golden_task"]) 
}}
SELECT 
    transf_province_state ,
    country_region ,
    lat   ,   
    long   , 
    covid_for_date_value ,     
    replace(replace(covid_for_date,'date_',''),'_','-')::date as covid_for_date
FROM {{ref( 'silver_unpivot_covid_geo')}}
WHERE country_region = 'Australia'
