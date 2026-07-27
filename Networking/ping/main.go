package main

import (
	"fmt"
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

	return nil
}
