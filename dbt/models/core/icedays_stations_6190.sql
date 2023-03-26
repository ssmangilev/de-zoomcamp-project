{{ config(materialized='table') }}


select 
    *
from {{ ref('eistage_stationsliste_6190.csv') }}