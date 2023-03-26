{{ config(materialized='view') }}

with tabledata as 
(
  select *
  from {{ source('bigquery','Heissetage') }}
)
select
    {{ dbt_utils.surrogate_key(['Stations_id', 'Bezugszeitraum']) }} as id,
    Stations_id as stations_id,
    Bezugszeitraum as period_of_time,
    Datenquelle as source,
    January, February, March, April, May,
    June, July, August, September, October,
    November, December

from tabledata

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}