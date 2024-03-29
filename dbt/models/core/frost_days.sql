{{ config(materialized='table') }}

with stg_frostdays as (
    select * from {{ ref('Frostdays')}}
),
stations_6190 as (
    select *, "1961-1990" as period_of_time from {{ ref('frostdays_stations_6190')}}
),
stations_7100 as (
    select *, "1971-2000" as period_of_time from {{ ref('frostdays_stations_7100')}}
),
stations_8110 as (
    select *, "1981-2010" as period_of_time from {{ ref('frostdays_stations_8110')}}
),
stations_9120 as (
    select *, "1991-2020" as period_of_time from {{ ref('frostdays_stations_9120')}}
),
stations_unioned as (
    select * from stations_6190
    union all
    select *from stations_7100
    union all
    select * from stations_8110
    union all
    select * from stations_9120
)
<<<<<<< HEAD
select stg_frostdays.*, stations_unioned.Stationsname, stations_unioned.Breite,
stations_unioned.Stationshoehe, stations_unioned.Bundesland  from stg_frostdays
=======
select stg_frostdays.*, stations_unioned.Stationsname, stations_unioned.Breite, stations_unioned.Laenge,
stations_unioned.Stationshoehe, stations_unioned.Bundesland from stg_hotdays from stg_frostdays
>>>>>>> 6e13e65 (Fix dbt models)
inner join stations_unioned
on stg_frostdays.stations_id = stations_unioned.Stations_id and
    stg_frostdays.period_of_time = stations_unioned.period_of_time
