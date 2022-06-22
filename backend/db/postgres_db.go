package db

import (
	"context"
	"errors"
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
	for rows.Next() {
		u := User{}
		e := rows.Scan(&u.ID, &u.Email, &u.PasswordHash)
		if e != nil {
			return []User{}, e
		}
		users = append(users, u)
	}
	return users, nil
}

func (db *PostgresUserDB) GetUserById(ID string) (User, error) {
	selectUserById := `
		SELECT id, email, password_hash
		FROM users
		where id = $1;
	`
	rows, e := db.pool.Query(context.Background(), selectUserById, ID)
	if e != nil {
		rows.Close()
		return User{}, e
	}

	u := User{}

	success := rows.Next()
	if !success {
		rows.Close()
		return User{}, errors.New("No User found with ID")
	}
	e = rows.Scan(&u.ID, &u.Email, &u.PasswordHash)

	if e != nil {
		rows.Close()
		return User{}, e
	}

	rows.Close()
	return u, nil
}

func (db *PostgresUserDB) CreateUser(u User) (User, error) {
	insertUser := `
		INSERT INTO users (id, email, password_hash)
		VALUES ($1, $2, $3)
		RETURNING id, email, password_hash;
	`

	rows, e := db.pool.Query(
		context.Background(),
		insertUser,
		u.ID,
		u.Email,
		u.PasswordHash,
	)

	if e != nil {
		rows.Close()
		return User{}, e
	}

	success := rows.Next()
	if !success {
		rows.Close()
		return User{}, errors.New("Could not create new user")
	}

	newUser := User{}

	e = rows.Scan(&newUser.ID, &newUser.Email, &newUser.PasswordHash)

	if e != nil {
		rows.Close()
		return User{}, e
	}

	rows.Close()
	return newUser, nil
}
