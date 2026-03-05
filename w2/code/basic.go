package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
)

type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// dummy database
var users = []User{
	{ID: "1", Name: "Thai Tu Fy", Email: "a@dota2.com"},
	{ID: "2", Name: "Do Nam Trung", Email: "b@example.com"},
}

// endpoint /users
func usersHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	switch r.Method {
	case http.MethodGet:
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(users)

	case http.MethodPost:
		var newUser User
		err := json.NewDecoder(r.Body).Decode(&newUser)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			json.NewEncoder(w).Encode(map[string]string{"error": "Invalid data"})
			return
		}
		users = append(users, newUser)
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(newUser)

	default:
		w.WriteHeader(http.StatusMethodNotAllowed) // for other methods
	}
}

func usersByIDHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	id := strings.TrimPrefix(r.URL.Path, "/users/")

	index := -1
	for i, u := range users {
		if u.ID == id {
			index = i
			break
		}
	}

	if index == -1 {
		w.WriteHeader(http.StatusNotFound)
		return
	}

	switch r.Method {
	case http.MethodPut:
		var updatedUser User
		err := json.NewDecoder(r.Body).Decode(&updatedUser)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		updatedUser.ID = id
		users[index] = updatedUser

		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(users[index])

	case http.MethodPatch:
		var patchData map[string]string
		err := json.NewDecoder(r.Body).Decode(&patchData)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			return
		}

		if newName, ok := patchData["name"]; ok {
			users[index].Name = newName
		}
		if newEmail, ok := patchData["email"]; ok {
			users[index].Email = newEmail
		}

		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(users[index])

	case http.MethodDelete:
		users = append(users[:index], users[index+1:]...)

		w.WriteHeader(http.StatusNoContent)

	default:
		w.WriteHeader(http.StatusMethodNotAllowed) // for other methods
	}
}

func main() {
	http.HandleFunc("/users", usersHandler)
	http.HandleFunc("/users/", usersByIDHandler)

	port := ":8080"
	fmt.Printf("Server started at http://localhost%s\n", port)

	err := http.ListenAndServe(port, nil)
	if err != nil {
		log.Fatal("Error: ", err)
	}
}

// GET: curl "http://localhost:8080/users"
//
// POST: curl -X POST "http://localhost:8080/users" \
//   -H "Content-Type: application/json" \
//   -d '{"id":"3","name":"Nguyen Van A","email":"c@example.com"}'
//
// DELETE: curl -X DELETE "http://localhost:8080/users/1"
//
//  PUT: curl -X PUT "http://localhost:8080/users/1" \
//   -d '{"id":"1","name":"meepo","email":"m@dota2.com"}'
//
// PATCH: curl -X PATCH "http://localhost:8080/users/3" \
//   -d '{"name":"invoker"}'
