# #!/usr/bin/env bash
# # SeqRepo file cache and threading performance
# # Assumes mac doesn't have the GNU date command and uses gdate from homebrew coreutils

# seqrepo_path=/Users/kferrite/dev/biocommons.seqrepo/seqrepo/2021-01-29
# m=10000
# n=4

# function m_time {
#     t0=$(gdate +%s%N)
#     $@ #>/dev/null
#     t1=$(gdate +%s%N)
#     python -c "print(f'{($t1-$t0)/1e9:.2f}')"
# }


# # Depending on the ulimit fd setting and
# # m value (and maybe n value), this will throw OSErrors
# # threading, no fd cache, with new seqrepo per request
# t=$(m_time ./threading-test2 -s $seqrepo_path -m $m -n $n --reinit-seqrepo)
# echo "$t | No file descriptor cache, with threading"

import argparse
import pathlib
import random
import subprocess
import logging
import time

import multiprocessing # as multiprocessing

from biocommons.seqrepo import SeqRepo
from biocommons.seqrepo.dataproxy import SeqRepoRESTDataProxy

_logger = logging.getLogger()

def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-n", "--n-threads", type=int, default=1)
    ap.add_argument("-s", "--seqrepo-path", type=pathlib.Path, required=True)
    ap.add_argument("-m", "--max-accessions", type=int)
    ap.add_argument("-f", "--fd-cache-size", type=int, default=0)
    opts = ap.parse_args(argv)
    return opts


def lsof_count(dirname: str) -> int:
    lsof_cmd = [
        "bash", "-c",
        f"lsof +D {dirname} | wc -l"]
    lsof_p = subprocess.Popen(
        lsof_cmd,
        stdout=subprocess.PIPE)
    (stdout, _) = lsof_p.communicate()
    stdout = stdout.decode("utf-8").strip()
    return int(stdout)


class LsofWorker(multiprocessing.Process):
    def __init__(self, dirname, check_interval=5):
        """
        check_interval: seconds between open file checks
        """
        self.dirname = dirname
        self.check_interval = check_interval
        super().__init__()

    def run(self):
        try:
            while True:
                ct = lsof_count(self.dirname)
                print(f"{self.dirname} open file count {ct}", flush=True)
                time.sleep(self.check_interval)
        except InterruptedError:
            pass


def main(argv):
    opts = parse_args(argv)

    sr = SeqRepo(root_dir=opts.seqrepo_path, fd_cache_size=opts.fd_cache_size) 

    acs = set(a["alias"] for a in sr.aliases.find_aliases(namespace="RefSeq", alias="NM_%"))
    acs = random.sample(sorted(acs), opts.max_accessions or len(acs))
    sr_dataproxy = SeqRepoRESTDataProxy("http://127.0.0.1:5000/seqrepo")

    # print(lsof_count(opts.seqrepo_path))
    lsof_p = LsofWorker(opts.seqrepo_path, 1)
    lsof_p.start()

    for ac in acs:
        sr_dataproxy.get_sequence(f"{ac}", 0, 5)

    time.sleep(10)

    lsof_p.terminate()


if __name__ == "__main__":
    import coloredlogs
    import sys
    coloredlogs.install(level="WARN")
    _logger.info("Calling main")
    main(argv=sys.argv[1:])
