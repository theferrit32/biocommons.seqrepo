## Single threaded performance with/without cache, with/without lock, with/without close

### Cache enabled, with and without locks

With cache at default size (128), one thread, no locks
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 1 -f 128
2023-10-02 19:46:27 wm12f-58b biocommons.seqrepo.fastadir.fastadir[57585] WARNING File descriptor caching enabled (size=128)
2023-10-02 19:46:27 wm12f-58b root[57585] INFO Starting run with 1 threads
2023-10-02 19:46:29 wm12f-58b root[57585] INFO Queueing 10000 accessions
2023-10-02 19:46:29 wm12f-58b root[57585] INFO Done filling input queue
CacheInfo(hits=9878, misses=122, maxsize=128, currsize=122)
2023-10-02 19:46:40 wm12f-58b root[57585] INFO Fetched 10000 sequences in 8.471630096435547 s with 1 threads; 1180 seq/sec
```

With cache at default size (128), one thread, with locks
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 1 -f -1
2023-10-02 19:48:06 wm12f-58b biocommons.seqrepo.fastadir.fastadir[57624] INFO File descriptor caching unlimited with locks
2023-10-02 19:48:06 wm12f-58b root[57624] INFO Starting run with 1 threads
2023-10-02 19:48:07 wm12f-58b root[57624] INFO Queueing 10000 accessions
2023-10-02 19:48:08 wm12f-58b root[57624] INFO Done filling input queue
CacheInfo(hits=9880, misses=120, maxsize=128, currsize=120)
2023-10-02 19:48:19 wm12f-58b root[57624] INFO Fetched 10000 sequences in 8.96427321434021 s with 1 threads; 1116 seq/sec
```
(no real difference between above two)


### Cache disabled, with and without explicit close on file descriptor

No cache, one thread
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 1 -f 0
2023-10-02 19:54:49 wm12f-58b biocommons.seqrepo.fastadir.fastadir[57816] INFO File descriptor caching disabled
2023-10-02 19:54:49 wm12f-58b root[57816] INFO Starting run with 1 threads
2023-10-02 19:54:51 wm12f-58b root[57816] INFO Queueing 10000 accessions
2023-10-02 19:54:51 wm12f-58b root[57816] INFO Done filling input queue
2023-10-02 19:56:24 wm12f-58b root[57816] INFO Fetched 10000 sequences in 90.37285280227661 s with 1 threads; 111 seq/sec
```

No cache, one thread, with `close` in `fetch`
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 1 -f -2
2023-10-02 20:38:05 wm12f-58b biocommons.seqrepo.fastadir.fastadir[69261] INFO File descriptor caching disabled, with close
2023-10-02 20:38:05 wm12f-58b root[69261] INFO Starting run with 1 threads
2023-10-02 20:38:07 wm12f-58b root[69261] INFO Queueing 10000 accessions
2023-10-02 20:38:07 wm12f-58b root[69261] INFO Done filling input queue
2023-10-02 20:39:38 wm12f-58b root[69261] INFO Fetched 10000 sequences in 88.3554949760437 s with 1 threads; 113 seq/sec
```
(no real difference between above two)






## Multithreading

Same as above, but with multiple threads

### Cache enabled, with and without locks

With cache at default size (128), 10 threads, no locks
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 10 -f 128
2023-10-02 21:52:31 wm12f-58b biocommons.seqrepo.fastadir.fastadir[72961] WARNING File descriptor caching enabled (size=128)
2023-10-02 21:52:31 wm12f-58b root[72961] INFO Starting run with 10 threads
2023-10-02 21:52:33 wm12f-58b root[72961] INFO Queueing 10000 accessions
2023-10-02 21:52:33 wm12f-58b root[72961] INFO Done filling input queue
[E::bgzf_read_block] Invalid BGZF header at offset 10051541
[E::fai_retrieve] Failed to retrieve block. (Seeking in a compressed, .gzi unindexed, file?)
...(etc)
```

With cache at default size (128), 10 threads, with locks
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 10 -f -1
2023-10-02 22:01:48 wm12f-58b biocommons.seqrepo.fastadir.fastadir[73402] INFO File descriptor caching unlimited with locks
2023-10-02 22:01:48 wm12f-58b root[73402] INFO Starting run with 10 threads
2023-10-02 22:01:50 wm12f-58b root[73402] INFO Queueing 10000 accessions
2023-10-02 22:01:50 wm12f-58b root[73402] INFO Done filling input queue
CacheInfo(hits=9868, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9869, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
CacheInfo(hits=9873, misses=127, maxsize=128, currsize=119)
2023-10-02 22:01:58 wm12f-58b root[73402] INFO Fetched 10000 sequences in 4.627795934677124 s with 10 threads; 2161 seq/sec
```


### Cache disabled, with and without explicit close on file descriptor

No cache, 10 threads
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 10 -f 0
2023-10-02 21:59:30 wm12f-58b biocommons.seqrepo.fastadir.fastadir[73336] INFO File descriptor caching disabled
2023-10-02 21:59:30 wm12f-58b root[73336] INFO Starting run with 10 threads
2023-10-02 21:59:32 wm12f-58b root[73336] INFO Queueing 10000 accessions
2023-10-02 21:59:32 wm12f-58b root[73336] INFO Done filling input queue
2023-10-02 22:00:22 wm12f-58b root[73336] INFO Fetched 10000 sequences in 47.0308198928833 s with 10 threads; 213 seq/sec
```

No cache, 10 threads, with `close` in `fetch`
```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 10 -f -2
2023-10-02 22:02:43 wm12f-58b biocommons.seqrepo.fastadir.fastadir[73420] INFO File descriptor caching disabled, with close
2023-10-02 22:02:43 wm12f-58b root[73420] INFO Starting run with 10 threads
2023-10-02 22:02:44 wm12f-58b root[73420] INFO Queueing 10000 accessions
2023-10-02 22:02:44 wm12f-58b root[73420] INFO Done filling input queue
2023-10-02 22:03:32 wm12f-58b root[73420] INFO Fetched 10000 sequences in 44.82555437088013 s with 10 threads; 223 seq/sec
```
(no real difference between above two)


### Adding an explicit to FastaDir.fetch

Added an option `--seqrepo-lsof-count` that performs an lsof count on the seqrepo directory (platform dependent, works on MacOS and Linuxes with BSD/GNU utils)

```
(venv) kferrite@wm12f-58b threading-tests % ./threading-test2 -s /Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 -m 10000 -n 10 -f -2 --seqrepo-lsof-count
2023-10-02 22:16:10 wm12f-58b biocommons.seqrepo.fastadir.fastadir[73932] INFO File descriptor caching disabled, with close
2023-10-02 22:16:10 wm12f-58b root[73932] INFO Starting run with 10 threads
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 9
2023-10-02 22:16:12 wm12f-58b root[73932] INFO Queueing 10000 accessions
2023-10-02 22:16:12 wm12f-58b root[73932] INFO Done filling input queue
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 9
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 9
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 9
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 12
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 13
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 18
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 10
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 15
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 16
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 10
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 13
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 18
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 10
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 13
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 17
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 15
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 9
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 18
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 18
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 11
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 15
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 17
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 18
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 18
/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29 open file count 19
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-7, started 123145539461120)>: Done; processed 1006 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-1, started 123145438724096)>: Done; processed 993 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-2, started 123145455513600)>: Done; processed 990 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-8, started 123145556250624)>: Done; processed 988 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-4, started 123145489092608)>: Done; processed 1000 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-6, started 123145522671616)>: Done; processed 1013 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-3, started 123145472303104)>: Done; processed 997 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-5, started 123145505882112)>: Done; processed 1000 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-10, started 123145589829632)>: Done; processed 1016 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO <Worker(Thread-9, started 123145573040128)>: Done; processed 997 accessions
2023-10-02 22:16:59 wm12f-58b root[73932] INFO Fetched 10000 sequences in 43.89950704574585 s with 10 threads; 228 seq/sec
```


## Summary

Adding a `.close` in `FastaDir.fetch` when no file descriptor caching is used resolves the issue with large growth in open file descriptors sitting in memory awaiting garbage collection, with no additional performance impact compared to the option with no file descriptor caching *without* a `.close` call.

Removing the file descriptor cache creates a major hit to performance. A roughly 10x slowdown in these tests. (1180/sec vs 111/sec). Leaving the cache enabled and adding a mutex lock to it that `FastaDir.fetch` acquires before the read operation preserves the performance benefit of the file descriptor cache with no significant time overhead. (1180/sec no lock vs 1116/sec with lock (not significant))
