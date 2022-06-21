package db

// "context"
// "os"
// "github.com/jackc/pgx/v4"

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
