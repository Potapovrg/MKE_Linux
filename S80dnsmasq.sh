orangepi@orangepizero2:~$ cat S80dnsmasq
#!/bin/sh

DAEMON="dnsmasq"
PIDFILE="/var/run/$DAEMON.pid"

[ -f /etc/dnsmasq.conf ] || exit 0

case "$1" in
        start)
                printf "Starting dnsmasq: "
                start-stop-daemon -S -p "$PIDFILE" -x "/usr/sbin/$DAEMON" -- \
                        --pid-file="$PIDFILE"
                [ $? = 0 ] && echo "OK" || echo "FAIL"
                ;;
        stop)
                printf "Stopping dnsmasq: "
                start-stop-daemon -K -q -p "$PIDFILE" -x "/usr/sbin/$DAEMON"
                [ $? = 0 ] && echo "OK" || echo "FAIL"
                ;;
        restart|reload)
                $0 stop
                $0 start
                ;;
        *)
                echo "Usage: $0 {start|stop|restart}"
                exit 1
esac

exit 0
