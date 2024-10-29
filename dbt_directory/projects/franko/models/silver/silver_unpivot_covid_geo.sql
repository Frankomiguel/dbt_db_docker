-- depends_on: {{ ref('silver_covid_geo') }}
{{
    dbt_utils.unpivot(
        relation=ref("silver_covid_geo"),
        cast_to="integer",
        exclude=["Province_State","Country_Region","lat","long","transf_province_state"],        
        field_name="covid_for_date",
        value_name="covid_for_date_value"
    )
}}
