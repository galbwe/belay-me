package db

import (
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v4/pgxpool"
)

type PostgresUserDB struct {
	pool *pgxpool.Pool
}

func (db *PostgresUserDB) Connect(url string) {
	// connect to the database
	pool, err := pgxpool.Connect(context.Background(), url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	(*db).pool = pool
}

func (db *PostgresUserDB) GetUsers() ([]User, error) {
	selectUsers := `
		SELECT id, email, password_hash
		FROM users order by id;
	`
	rows, e := db.pool.Query(context.Background(), selectUsers)
	if e != nil {
		return []User{}, e
	}
	users := []User{}
	var currentId string
	var currentEmail string
	var currentPasswordHash string
	for rows.Next() {
		e := rows.Scan(&currentId, &currentEmail, &currentPasswordHash)
		if e != nil {
			return []User{}, e
		}
		users = append(users, User{ID: currentId, Email: currentEmail, PasswordHash: currentPasswordHash})
	}
	return users, nil
}
