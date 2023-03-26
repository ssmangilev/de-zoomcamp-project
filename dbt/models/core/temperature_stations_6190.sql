{{ config(materialized='table') }}


select 
    *
from {{ ref('temperatur_stationsliste_6190') }}