#!/bin/bash
# Arguments and defaults
TESTS_CONTAINER=${1:-"ghcr.io/szyminson/ctr-tools-test:latest"}
CONTAINER_NAME=${2:-"ctr-tools-test"}
IN_CONTAINER_RESULT_DIR=${3:-"/var/ctr-tools-test/results"}
RESULT_BASE_DIR=${4:-"/tmp"}
SIG_HANDLER="docker rm $CONTAINER_NAME; podman rm $CONTAINER_NAME; exit"

# Setup tmux logging if in a tmux session
if [ "$TERM" = "screen" ] && [ -n "$TMUX" ]; then
    TMUX_LOG_FILE="$RESULT_BASE_DIR/tmux.log"
    # Move previous log to different file if exists
    [ -f $TMUX_LOG_FILE ] && mv $TMUX_LOG_FILE "$TMUX_LOG_FILE.$(date +%s)"
    tmux pipe-pane -o "cat >> $TMUX_LOG_FILE"
fi

echo -e "\nRunning Docker test\n"
docker run --rm --name $CONTAINER_NAME -v "$RESULT_BASE_DIR/docker:$IN_CONTAINER_RESULT_DIR" \
    $TESTS_CONTAINER
echo -e "\nRunning podman test\n"
podman run --rm --name $CONTAINER_NAME -v "$RESULT_BASE_DIR/podman:$IN_CONTAINER_RESULT_DIR" \
    $TESTS_CONTAINER
