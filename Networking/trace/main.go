package main

import (
	"fmt"
	"net"
	"os"

	"golang.org/x/net/ipv4"
)

func main() {
	err := trace(os.Args[1], 30)
	if err != nil {
		fmt.Println(err)
	}
}

func establishConn(target string) (*ipv4.PacketConn, *net.IPAddr, error) {

	raddres, err := net.ResolveIPAddr("ip4", target)
	if err != nil {
		return nil, nil, fmt.Errorf("Unable to resolve %s: %w", target, err)
	}
	conn, err := net.ListenIP("ip4:icmp", nil)
	if err != nil {
		return nil, raddres, fmt.Errorf("Unable to establish listener: %w", err)
	}
	return ipv4.NewPacketConn(conn), raddres, nil
}
func trace(target string, hops int) error {

	conn, raddres, err := establishConn(target)
	if err != nil {
		return err
	}

	defer conn.Close()
	data := []byte("hola amigo")

	for ttl := 1; ttl <= hops; ttl++ {

	}
	return nil
}
