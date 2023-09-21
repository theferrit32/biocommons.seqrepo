This demo looks at open file descriptors not being quickly closed in the `seqrepo-rest-service` main branch. (tested @ `26aa654`)


Run seqrepo-rest-service with ulimit 1000. This is sufficiently high to show there is a significant lag in when file descriptors in objects pending garbage collection actually get closed.
```
ulimit -n 1000; seqrepo-rest-service /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29
```

## Test 1

- ulimit -n 1000
- 2000 queries
- Locked FastaDir cache (LockableFabzReader)
- lsof on seqrepo directory every 1 second
```
$ python gc-lag.py -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -f -1 -m 2000 | ggrep 'open file count'
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 30
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 60
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 94
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 121
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 155
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 180
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 214
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 235
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 273
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 296
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 332
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 356
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 387
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 410
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 448
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 484
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 505
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 539
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 553
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 588
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 611
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 647
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 670
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 702
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 725
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 761
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 786
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 818
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 841
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 879
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 900
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 934
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 957
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 991
Traceback (most recent call last):
  File "/Users/kferrite/dev/biocommons.seqrepo/misc/threading-tests/gc-lag.py", line 107, in <module>
    main()
  File "/Users/kferrite/dev/biocommons.seqrepo/misc/threading-tests/gc-lag.py", line 96, in main
    sr_dataproxy.get_sequence(f"{ac}", 0, 5)
  File "/Users/kferrite/dev/biocommons.seqrepo/src/biocommons/seqrepo/dataproxy.py", line 100, in get_sequence
    return self._get_sequence(identifier, start=start, end=end)
  File "/Users/kferrite/dev/biocommons.seqrepo/src/biocommons/seqrepo/dataproxy.py", line 155, in _get_sequence
    resp.raise_for_status()
  File "/Users/kferrite/dev/biocommons.seqrepo/venv/lib/python3.10/site-packages/requests/models.py", line 1021, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 500 Server Error: INTERNAL SERVER ERROR for url: http://127.0.0.1:5000/seqrepo/1/sequence/NM_001329652.2?start=0&end=5
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 1005
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 1005
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 1005
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 1005
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 1005
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 1005
```

## Test 2

- ulimit -n 1000
- 2000 queries
- No FastaDir cache
- lsof on seqrepo directory every 1 second
```
$ python gc-lag.py -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -f 0 -m 2000 | ggrep 'open file count'
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 35
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 92
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 147
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 194
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 239
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 290
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 353
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 399
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 446
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 496
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 539
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 585
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 647
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 698
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 747
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 796
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 843
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 896
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 956
Traceback (most recent call last):
  File "/Users/kferrite/dev/biocommons.seqrepo/misc/threading-tests/gc-lag.py", line 104, in <module>
    main()
  File "/Users/kferrite/dev/biocommons.seqrepo/misc/threading-tests/gc-lag.py", line 93, in main
    sr_dataproxy.get_sequence(f"{ac}", 0, 5)
  File "/Users/kferrite/dev/biocommons.seqrepo/src/biocommons/seqrepo/dataproxy.py", line 100, in get_sequence
    return self._get_sequence(identifier, start=start, end=end)
  File "/Users/kferrite/dev/biocommons.seqrepo/src/biocommons/seqrepo/dataproxy.py", line 155, in _get_sequence
    resp.raise_for_status()
  File "/Users/kferrite/dev/biocommons.seqrepo/venv/lib/python3.10/site-packages/requests/models.py", line 1021, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 500 Server Error: INTERNAL SERVER ERROR for url: http://127.0.0.1:5000/seqrepo/1/sequence/NM_001305156.2?start=0&end=5
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 997
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 997
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 997
```
