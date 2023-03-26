{{ config(materialized='table') }}


select 
    *
from {{ ref('temperatur_stationsliste_9120.csv') }}