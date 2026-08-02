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
	err := trace(os.Args[1], 64)
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

	fmt.Printf("traceroute to %s (%s), %d hops max, 40 byte packets\n", target, raddres, hops)
	for ttl := 1; ttl <= hops; ttl++ {
		conn.SetTTL(ttl)

		echoReq := icmp.Message{
			Type: ipv4.ICMPTypeEcho,
			Code: 0,
			Body: &icmp.Echo{
				ID:   os.Getpid() & 0xffff,
				Seq:  ttl,
				Data: data[:],
			},
		}
		message, err := echoReq.Marshal(nil)
		if err != nil {
			return fmt.Errorf("unable to Marshal message")
		}
		err = conn.SetReadDeadline(time.Now().Add(3 * time.Second))
		if err != nil {
			return fmt.Errorf("unavle to readdead line")
		}

		_, err = conn.WriteTo(message, nil, raddres)
		if err != nil {
			return fmt.Errorf("server unreachable")
		}

	}
	return nil
}
