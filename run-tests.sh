#!/bin/bash
PTS=/phoronix-test-suite/phoronix-test-suite

$PTS batch-run pts/sysbench || exit 1
LATEST_RESULT=$(ls -l /var/lib/phoronix-test-suite/test-results | tail -1 | awk '{print $NF}')
$PTS result-file-to-json $LATEST_RESULT
cp "/root/$LATEST_RESULT.json" /root/latest.json
cat /root/latest.json
