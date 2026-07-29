package main

import "fmt"

func main() {
	err := trace()
	if err != nil {
		fmt.Println(err)
	}
}

func trace() error {

	return nil
}
