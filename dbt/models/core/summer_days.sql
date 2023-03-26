{{ config(materialized='table') }}

with stg_summerdays as (
    select * from {{ ref('Summerdays')}}
),
stations_6190 as (
    select *, "1961-1990" as period_of_time from {{ ref('summerdays_stations_6190')}}
),
stations_7100 as (
    select *, "1971-2000" as period_of_time from {{ ref('summerdays_stations_7100')}}
),
stations_8110 as (
    select *, "1981-2010" as period_of_time from {{ ref('summerdays_stations_8110')}}
),
stations_9120 as (
    select *, "1991-2020" as period_of_time from {{ ref('summerdays_stations_9120')}}
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
select stg_summerdays.*, stations_unioned.Stationsname, stations_unioned.Breite,
stations_unioned.Stationshoehe, stations_unioned.Bundesland from stg_summerdays
inner join stations_unioned
on stg_summerdays.stations_id = stations_unioned.Stations_id and
    stg_summerdays.period_of_time = stations_unioned.period_of_time
