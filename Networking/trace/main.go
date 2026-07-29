package main

import (
	"fmt"
	"net"
	"os"
)

func main() {
	err := trace(os.Args[1])
	if err != nil {
		fmt.Println(err)
	}
}

func establishConn(target string) (*net.IPConn, error) {

	raddres, err := net.ResolveIPAddr("ip4", target)
	if err != nil {
		return nil, fmt.Errorf("Unable to resolve target: %w", target)
	}
	conn, err := net.DialIP("ip4", nil, raddres)
	if err != nil {
		return nil, fmt.Errorf("Unable to dial ip: %w", raddres)
	}

	return conn, nil
}
func trace(target string) error {

	conn, err := establishConn(target)
	if err != nil {
		return err
	}

	defer conn.Close()
	return nil
}
