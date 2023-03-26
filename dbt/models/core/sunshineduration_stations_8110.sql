{{ config(materialized='table') }}


select 
    *
from {{ ref('sonnenscheindauer_stationsliste_8110.csv') }}