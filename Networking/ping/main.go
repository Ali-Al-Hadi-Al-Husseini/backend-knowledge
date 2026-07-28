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
		message, err := echoReq.Marshal(nil)
		if err != nil {
			return fmt.Errorf("failed to serilieze message")
		}

		err = conn.SetReadDeadline(time.Now().Add(1 * time.Second))
		if err != nil {
			return fmt.Errorf("Failed to readdead line")
		}
		startTime := time.Now()
		_, err = conn.Write(message)
		if err != nil {
			return fmt.Errorf("server unreachable")
		}

		resp := make([]byte, 512)
		n, peer, err := conn.ReadFrom(resp)
		endTime := time.Now()

		if err != nil {
			return fmt.Errorf("failed to read ICMP response: %w", err)
		}

		parsedMsg, err := icmp.ParseMessage(1, resp[:n])
		if err != nil {
			return fmt.Errorf("failed to parse ICMP message: %w", err)
		}
		echoType := parsedMsg.Type
		body := parsedMsg.Body.(*icmp.Echo)
		proto := parsedMsg.Type.Protocol()

		switch parsedMsg.Type {
		case ipv4.ICMPTypeEchoReply:
			elapsed := endTime.Sub(startTime)
			fmt.Printf("%d bytes from %s: pid=%d, icmp_type=%v, icmp_seq=%d, data=%s, time:%dμs\n", body.Len(proto), peer, body.ID, echoType, body.Seq, string(body.Data), elapsed.Milliseconds())
		default:
			fmt.Printf("received unexpected message from %s: pid=%d, icmp_type=%v, icmp_seq=%d, data=%s\n", peer, body.ID, echoType, body.Seq, string(body.Data))
		}
		time.Sleep(delay * time.Second)
	}
	return nil
}
