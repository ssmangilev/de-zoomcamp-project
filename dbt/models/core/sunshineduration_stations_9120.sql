{{ config(materialized='table') }}


select 
    *
from {{ ref('sonnenscheindauer_stationsliste_9120.csv') }}