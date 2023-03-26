{{ config(materialized='table') }}


select 
    *
from {{ ref('sonnenscheindauer_stationsliste_6190') }}