-- depends_on: {{ ref('golden_data') }}
{{
    config(materialized = 'table', 
    tags = ["golden_task"]) 
}}
SELECT 
    transf_province_state ,
    country_region ,
    sum(covid_for_date_value) AS cnt_2021_first_quarter
FROM {{ref( 'golden_data')}}
WHERE 1=1
AND covid_for_date BETWEEN '2021-01-01' AND '2021-04-01'
GROUP BY 1,2
