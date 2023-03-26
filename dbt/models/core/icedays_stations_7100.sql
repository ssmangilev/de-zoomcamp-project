{{ config(materialized='table') }}


select 
    *
from {{ ref('eistage_stationsliste_7100.csv.csv') }}