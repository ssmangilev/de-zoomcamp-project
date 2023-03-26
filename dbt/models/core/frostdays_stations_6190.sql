{{ config(materialized='table') }}


select 
    *
from {{ ref('frosttage_stationsliste_6190.csv') }}