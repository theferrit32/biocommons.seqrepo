#!/usr/bin/env bash
# SeqRepo file cache and threading performance
# Assumes mac doesn't have the GNU date command and uses gdate from homebrew coreutils

seqrepo_path=/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29
m=10000
n=4

function m_time {
    t0=$(gdate +%s%N)
    $@ #>/dev/null
    t1=$(gdate +%s%N)
    python -c "print(f'{($t1-$t0)/1e9:.2f}')"
}


# Depending on the ulimit fd setting and
# m value (and maybe n value), this will throw OSErrors
# threading, no fd cache, with new seqrepo per request
t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n --reinit-seqrepo)
echo "$t | No file descriptor cache, with threading"
