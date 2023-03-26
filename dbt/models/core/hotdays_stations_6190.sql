{{ config(materialized='table') }}


select 
    *
from {{ ref('heissetage_stationsliste_6190') }}