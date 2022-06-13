package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

type user struct {
	ID           string `json:"id"`
	Email        string `json:"email"`
	PasswordHash string `json:"passwordHash"`
}

var users = []user{
	{ID: "1", Email: "user1@gmail.com", PasswordHash: "password1"},
	{ID: "2", Email: "user2@gmail.com", PasswordHash: "password2"},
	{ID: "3", Email: "user3@gmail.com", PasswordHash: "password3"},
}

// get a list of users
func getUsers(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, users)
}

func main() {
	router := gin.Default()
	router.GET("/users", getUsers)

	router.Run("localhost:8080")
}