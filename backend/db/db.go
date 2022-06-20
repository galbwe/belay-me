package db

import (
	"errors"
	// "context"
	// "os"
	// "github.com/jackc/pgx/v4"
)

// func connect(url string) {
// 	conn, err := pgx.Connect(context.Background(), url)
// 	if err != nil {
// 		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
// 		os.Exit(1)
// 	}
// 	return conn
// }

type User struct {
	ID           string
	Email        string
	PasswordHash string
}

type UserDB interface {
	GetUsers() ([]User, error)
	CreateUser(User) (User, error)
	GetUserById(ID string) (User, error)
	DeleteUser(ID string) (User, error)
	EditUserWithId(ID string) (User, error)
}

type LocalMemUserDB struct {
	users []User
}

func (db *LocalMemUserDB) GetUserById(ID string) (User, error) {
	for _, user := range (*db).users {
		if user.ID == ID {
			return user, nil
		}
	}
	return User{}, errors.New("GetUserById: no user found")
}

func (db *LocalMemUserDB) GetUsers() ([]User, error) {
	return (*db).users, nil
}

func (db *LocalMemUserDB) CreateUser(u User) (User, error) {
	// check that user with the same id does not already exist
	if _, err := (*db).GetUserById(u.ID); err == nil {
		return User{}, errors.New("CreateUser: a user with that id already exists")
	}
	(*db).users = append(db.users, u)
	return u, nil
}

func (db *LocalMemUserDB) DeleteUser(ID string) (User, error) {
	// find the index of the user with a matching ID
	for i, u := range (*db).users {
		if u.ID == ID {
			// remove the user with a matching id
			(*db).users = append((*db).users[:i], (*db).users[i+1:]...)
			return u, nil
		}
	}
	return User{}, errors.New("DeleteUser: no user was found with a matching id")
}

func (db *LocalMemUserDB) EditUser(ID string, u User) (User, error) {
	// check that the client is not trying to modify the user's ID
	if ID != u.ID {
		return User{}, errors.New("EditUser: cannot modify a User ID")
	}

	// find the index of the user with a matching ID
	for i, user := range (*db).users {
		if user.ID == ID {
			// if a match is found, replace the current index with new user data
			(*db).users[i] = u
			return u, nil
		}
	}
	return User{}, errors.New("EditUser: no user was found with a matching id")
}
