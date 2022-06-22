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

func TestPostgresDBGetUserById(t *testing.T) {
	setupPostgresDatabase()
	db := getUserDB()

	expectedUsers := []User{
		{ID: "1", Email: "user1@gmail.com", PasswordHash: "password1"},
		{ID: "2", Email: "user2@gmail.com", PasswordHash: "password2"},
		{ID: "3", Email: "user3@gmail.com", PasswordHash: "password3"},
	}
	for _, eu := range expectedUsers {
		u, _ := (&db).GetUserById(eu.ID)
		if u != eu {
			t.Errorf("GetUserById: expected %+v, but received %+v", eu, u)
		}
	}
	teardownPostgresDatabase()
}

func TestPostgresDBGetUserByIdNotFound(t *testing.T) {
	setupPostgresDatabase()
	db := getUserDB()

	u, e := (&db).GetUserById("adfadfasdf")

	if (u != User{}) || (e == nil) {
		t.Errorf("GetUserById: Expected u=%+v and e!=%v, but found u=%+v and e=%v", User{}, nil, u, e)
	}

	teardownPostgresDatabase()
}

func TestPostgresDBCreateUser(t *testing.T) {
	setupPostgresDatabase()
	db := getUserDB()

	newUser := User{ID: "4", Email: "user4@gmail.com", PasswordHash: "password4"}

	u, e := (&db).CreateUser(newUser)

	if u != newUser {
		t.Errorf("CreateUser: Expected u = %+v, but found %+v", newUser, u)
	}
	if e != nil {
		t.Errorf("CreateUser: Expected e = nil, but found %v", e)
	}

	retrievedUser, e := (&db).GetUserById(newUser.ID)
	if e != nil {
		t.Errorf("GetUser: Expected e = nil, but found %v", e)
	}
	if retrievedUser != newUser {
		t.Errorf("CreateUser: new user was not created")
	}
	teardownPostgresDatabase()
}

// TODO: check that a user with a duplicate id cannot be created
