{{ config(materialized='table') }}


select 
    *
from {{ ref('temperatur_stationsliste_7100.csv') }}