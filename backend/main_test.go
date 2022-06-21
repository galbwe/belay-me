package main

import (
	"net/http"
	"testing"
)

// checks that api endpoints work as expected for simple requests

func TestGetUser(t *testing.T) {
	requestUrl := "http://localhost:8080/users"
	res, _ := http.Get(requestUrl)

	if res.StatusCode != http.StatusOK {
		t.Errorf("Expected status code %d, but received %d", http.StatusOK, res.StatusCode)
	}
}
