{{ config(materialized='table') }}


select 
    *
from {{ ref('sonnenscheindauer_stationsliste_7100.csv') }}