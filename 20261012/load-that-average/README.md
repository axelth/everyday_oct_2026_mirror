# Load that Average
## Overview
Let's try and remember for once and for all what load average is.

This program will have a background task that stores the load average in an sqlite table, and an HTTPServer that serves a table of past figures.

A stretch goal is to graph the load averages.

## Load Average

What information do we have?
```sh
$ apropos "load average"
getloadavg (3)       - get system load averages
loads.bt (8)         - Prints load averages. Uses bpftrace/eBPF.
proc_loadavg (5)     - load average
tload (1)            - graphic representation of system load average
```

`man prod_loadavg`
> NAME
>        /proc/loadavg - load average
> 
> DESCRIPTION
>        /proc/loadavg
>               The first three fields in this file are load average figures giv‐
>               ing  the number of jobs in the run queue (state R) or waiting for
>               disk I/O (state D) averaged over 1, 5, and 15 minutes.  They  are
>               the same as the load average numbers given by uptime(1) and other
>               programs.   The fourth field consists of two numbers separated by
>               a slash (/).  The first of  these  is  the  number  of  currently
>               runnable  kernel  scheduling  entities (processes, threads).  The
>               value after the slash is the number of kernel scheduling entities
>               that currently exist on the system.  The fifth field is  the  PID
>               of the process that was most recently created on the system.

So how does that look?

```sh
$ cat /proc/loadavg
0.14 0.21 0.20 1/1340 308509
```

So, I guess a load average of under 1.0 means that we don't really have any jobs waiting?
But let's double check what being in the "run queue" mean.
Actually, "run queue" is not the operative word, "state R" is. "state R" means "currently running, or able to run", and both of these are in the kernel's run queue. 

This article has a good overview and good links
https://qiita.com/ryuichi1208/items/3b21aee6c38bcfdb12b1

## Plan
### Get loadaverage
We could go read it from the `proc` tree like above, but it's also exposed in python's `os.getloadavg() -> tuple[float, float, float]`, so let's just use that.

### Store loadaverage
Store our loadavg tuple together with timestamp in an SQLite database.
The schema will be
```sql
CREATE TABLE load_averages (
  id INTEGER PRIMARY KEY,
  timestamp INTEGER NOT NULL,
  one_min REAL NOT NULL,
  five_min REAL NOT NULL,
  fifteen_min REAL NOT NULL
);
```
### Presentation

When the program receives a GET request, it will return an html document with a table listing the 30 most recent values of the `load_averages` table.

It would be fun to do the following two expansions.
1. graph the load averages.
2. make the time axis logarithmic so we have high resolution for the last few minutes, and then increasingly sparse.

### Background Task?

### Configuration
We need to know where the SQLite database file is. We will pass this in as a commandline option.
We may also want to configure the sample rate
