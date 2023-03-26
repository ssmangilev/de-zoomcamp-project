{{ config(materialized='table') }}


select 
    *
from {{ ref('sommertage_stationsliste_6190') }}