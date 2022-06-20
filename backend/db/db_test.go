package db

import (
	"testing"
)

func mockUsers() []User {
	return []User{
		{ID: "1", Email: "user1@gmail.com", PasswordHash: "password1"},
		{ID: "2", Email: "user2@gmail.com", PasswordHash: "password2"},
		{ID: "3", Email: "user3@gmail.com", PasswordHash: "password3"},
	}
}

func TestGetUserById(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	// test retrieving one user by id
	u1, _ := (&db).GetUserById("1")
	if u1.ID != "1" || u1.Email != "user1@gmail.com" || u1.PasswordHash != "password1" {
		t.Errorf("Expected user %+v, but received %+v", users[0], u1)
	}
}

func TestNoUserFoundWithId(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	// test user not found
	u, err := (&db).GetUserById("asdfasdfas")
	if err == nil {
		t.Errorf("Expected err to not be nil")
	}
	if u.ID != "" || u.Email != "" || u.PasswordHash != "" {
		t.Errorf("Expected user %+v, but received %+v", User{}, u)
	}
}

func TestCreateUser(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	// test creating a user
	_, err := (&db).CreateUser(User{ID: "4", Email: "user4@gmail.com", PasswordHash: "password4"})
	if err != nil {
		t.Errorf("Expected err to be nil, but found %v", err)
	}
	if len(db.users) != 4 {
		t.Errorf("Expected db.users to have 4 elements after adding user, found %v", len(db.users))
	}
}

func TestCannotCreateUsersWithDuplicateIds(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	_, err := (&db).CreateUser(User{ID: "1", Email: "otheruser1@gmail.com", PasswordHash: "otherpassword1"})
	if err == nil {
		t.Error("Expected err to not be nil.")
	}
	if len(db.users) != 3 {
		t.Errorf("Expected db.users to have 3 elements. Found %v", len(db.users))
	}
}

func TestGetAllUsers(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	retrievedUsers, _ := (&db).GetUsers()
	for i, u := range retrievedUsers {
		if u != users[i] {
			t.Errorf("Expected user lists to be identical, but %+v != %+v at index %v", u, users[i], i)
		}
	}
}

func TestDeleteUser(t *testing.T) {
	//can delete first user in slice
	checkDeletingUser(t, "1")
	// can delete user in the middle of the slice
	checkDeletingUser(t, "2")
	// can delete last user in slice
	checkDeletingUser(t, "3")
}

func checkDeletingUser(t *testing.T, ID string) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	originalUser, _ := db.GetUserById(ID)
	user, _ := (&db).DeleteUser(ID)
	if user != originalUser {
		t.Errorf("Expected deleted user to be equal to %+v, but found %+v", originalUser, user)
	}
	if len(db.users) != 2 {
		t.Errorf("Expected db.users to have 2 elements, found %v", len(db.users))
	}
}

func TestDeleteUserNoUserFoundWithId(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	_, e := (&db).DeleteUser("asdfasdfasdfas")
	if e == nil {
		t.Errorf("Expected error to be nil, but found %v", e)
	}
	if len(db.users) != 3 {
		t.Errorf("Expected db.users to have 3 elements, but found %v", len(db.users))
	}
}

func TestEditUser(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	ID := "3"

	originalUser, _ := (&db).GetUserById(ID)

	updatedUser := User{
		ID:           originalUser.ID,
		Email:        "newemail@gmail.com",
		PasswordHash: "newpassword",
	}

	u, _ := (&db).EditUser(ID, updatedUser)
	if edited, _ := (&db).GetUserById(ID); edited != u {
		t.Errorf("EditUser: Expected edited user to equal %+v, but found %+v", edited, u)
	}
	if edited, _ := db.GetUserById(ID); edited != updatedUser {
		t.Errorf("EditUser: Expected edited user to equal %+v, but found %+v", edited, updatedUser)
	}
	if len(db.users) != 3 {
		t.Errorf("EditUser: Expected db.users to have length 3, but found %v", len(db.users))
	}
}

func TestEditUserNoIdFound(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	ID := "asdfasdfasdfa"
	updatedUser := User{
		ID:           ID,
		Email:        "newemail@gmail.com",
		PasswordHash: "newpassword",
	}

	_, e := (&db).EditUser(ID, updatedUser)

	if e == nil {
		t.Error("EditUser: Expected an error, but found nil")
	}
}

func TestEditUserCannotChangeID(t *testing.T) {
	var users []User
	users = mockUsers()
	var db LocalMemUserDB
	db.users = users

	ID := "3"
	updatedUser := User{
		ID:           "somefancynewid",
		Email:        "newemail@gmail.com",
		PasswordHash: "newpassword",
	}

	_, e := (&db).EditUser(ID, updatedUser)

	if e == nil {
		t.Error("EditUser: Expected an error when trying to edit user ID, but found nil")
	}
}
