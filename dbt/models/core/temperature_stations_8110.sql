{{ config(materialized='table') }}


select 
    *
from {{ ref('temperatur_stationsliste_8110.csv') }}