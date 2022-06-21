package main

import (
	"net/http"
	"os"

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

func postUsers(c *gin.Context) {
	var newUser user
	if err := c.BindJSON(&newUser); err != nil {
		return
	}
	users = append(users, newUser)
	c.IndentedJSON(http.StatusCreated, newUser)
}

func getUserById(c *gin.Context) {
	id := c.Param("id")

	for _, user := range users {
		if user.ID == id {
			c.IndentedJSON(http.StatusOK, user)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "User not found"})
}

func main() {
	router := gin.Default()
	router.GET("/users", getUsers)
	router.POST("/users", postUsers)
	router.GET("/users/:id", getUserById)

	baseUrl := os.Getenv("BASE_URL")
	if baseUrl == "" {
		baseUrl = "localhost:8080"
	}
	router.Run(baseUrl)
}
