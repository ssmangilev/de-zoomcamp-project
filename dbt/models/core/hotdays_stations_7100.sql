{{ config(materialized='table') }}


select 
    *
from {{ ref('heissetage_stationsliste_7100.csv') }}