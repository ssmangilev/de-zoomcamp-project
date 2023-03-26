{{ config(materialized='table') }}


select 
    *
from {{ ref('eistage_stationsliste_9120') }}