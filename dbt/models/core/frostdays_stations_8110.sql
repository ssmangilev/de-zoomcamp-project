{{ config(materialized='table') }}


select 
    *
from {{ ref('frosttage_stationsliste_8110') }}