{{ config(materialized='table') }}


select 
    *
from {{ ref('niederschlag_stationsliste_6190') }}