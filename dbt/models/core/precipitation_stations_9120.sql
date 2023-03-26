{{ config(materialized='table') }}


select 
    *
from {{ ref('niederschlag_stationsliste_9120.csv') }}