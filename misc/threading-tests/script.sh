#!/usr/bin/env bash
# SeqRepo file cache and threading performance
# Assumes mac doesn't have the GNU date command and uses gdate from homebrew coreutils

seqrepo_path=/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29
m=1000
n=4

function m_time {
    t0=$(gdate +%s%N)
    $@ >&2
    t1=$(gdate +%s%N)
    python -c "print(f'{($t1-$t0)/1e9:.2f}')"
}

# threading, no fd cache
t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n)
echo "$t | No file descriptor cache, with threading"

# ## This sometimes throw an exception because of concurrent access to file descriptors
# t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n \
#     --fd-cache-size 128)
# echo "$t | With file descriptor cache, with threading"


t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n \
    --fd-cache-size -1)
echo "$t | With file descriptor cache, with mutex, with threading"


t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n \
    --use-multiprocessing)
echo "$t | No file descriptor cache, with multiprocessing"


t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n \
    --fd-cache-size 128 \
    --use-multiprocessing)
echo "$t | With file descriptor cache, with multiprocessing"


t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n \
    --fd-cache-size -1 \
    --use-multiprocessing)
echo "$t | With file descriptor cache, with mutex, with multiprocessing"
