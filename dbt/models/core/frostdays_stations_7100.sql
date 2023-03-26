{{ config(materialized='table') }}


select 
    *
from {{ ref('frosttage_stationsliste_7100') }}