{{ config(materialized='table') }}


select 
    *
from {{ ref('heissetage_stationsliste_8110.csv') }}