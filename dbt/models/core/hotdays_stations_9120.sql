{{ config(materialized='table') }}


select 
    *
from {{ ref('heissetage_stationsliste_9120.csv') }}