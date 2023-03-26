{{ config(materialized='table') }}


select 
    *
from {{ ref('eistage_stationsliste_8110.csv') }}