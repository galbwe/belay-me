package db

import (
	"context"
	"fmt"
	"os"
	"testing"

	"github.com/jackc/pgx/v4/pgxpool"
)

func postgresUrl() string {
	return "postgres://belay_me:belay_me@localhost:5432/belay_me"
}

func postgresPool() pgxpool.Pool {
	url := postgresUrl()
	pool, err := pgxpool.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	return *pool
}

func setupPostgresDatabase() {
	pool := postgresPool()

	createUserTable := `CREATE TABLE users (
		id VARCHAR PRIMARY KEY,
		email VARCHAR NOT NULL,
		password_hash VARCHAR NOT NULL
	);`

	insertUserData := `
		INSERT INTO users (id, email, password_hash) VALUES
		('1', 'user1@gmail.com', 'password1'),
		('2', 'user2@gmail.com', 'password2'),
		('3', 'user3@gmail.com', 'password3');
	`

	pool.Query(context.Background(), createUserTable)
	pool.Query(context.Background(), insertUserData)
}

func teardownPostgresDatabase() {
	pool := postgresPool()

	deleteUserData := "DELETE FROM users;"

	dropUserTable := "DROP TABLE users"

	pool.Query(context.Background(), deleteUserData)
	pool.Query(context.Background(), dropUserTable)
}

func getUserDB() PostgresUserDB {
	db := PostgresUserDB{}
	url := postgresUrl()
	(&db).Connect(url)
	return db
}

func TestGetUsers(t *testing.T) {
	setupPostgresDatabase()
	db := getUserDB()
	users, _ := (&db).GetUsers()

	expectedUsers := []User{
		{ID: "1", Email: "user1@gmail.com", PasswordHash: "password1"},
		{ID: "2", Email: "user2@gmail.com", PasswordHash: "password2"},
		{ID: "3", Email: "user3@gmail.com", PasswordHash: "password3"},
	}

	for i, u := range users {
		if u != expectedUsers[i] {
			t.Errorf("GetUsers: unexpected return values. Expected %+v, but found %+v", expectedUsers[i], u)
		}
	}
	teardownPostgresDatabase()
}
