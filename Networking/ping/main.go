package main

import (
	"fmt"
	"net"
	"os"
	"time"
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

	return nil
}
