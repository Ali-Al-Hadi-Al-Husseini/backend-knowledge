package main

import (
	"fmt"
	"net"
	"os"
	"time"

	"golang.org/x/net/icmp"
	"golang.org/x/net/ipv4"
)

func main() {
	err := Ping(os.Args[1], 10, 1*time.Second)
	if err != nil {
		fmt.Println(fmt.Errorf("ping error: %w", err))
	}
}

func Ping(dest string, attempts int, delay time.Duration) error {

	raddres, err := net.ResolveIPAddr("ip4", dest)
	if err != nil {
		return fmt.Errorf("Failed to resolve address %w", dest)
	}
	conn, err := net.DialIP("ip4:icmp", nil, raddres)
	if err != nil {
		return fmt.Errorf("Failed to establish connection %w", raddres)
	}

	defer conn.Close()

	data := []byte("hola amigo")

	for i := 0; i < attempts; i++ {

		echoReq := icmp.Message{
			Type: ipv4.ICMPTypeEcho,
			Code: 0,
			Body: &icmp.Echo{
				ID:   os.Getpid() & 0xffff,
				Seq:  i,
				Data: data[:],
			},
		}

	}
	return nil
}
