{{ config(materialized='table') }}


select 
    *
from {{ ref('sommertage_stationsliste_7100') }}