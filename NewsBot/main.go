package main

import (
	"database/sql"
	"database/sql/driver"
	"encoding/json"
	"fmt"
	"github.com/lib/pq"
	"net/http"
	"time"
	"log"
	"io"
	"os"
)


const ( //My database information
	host     = "localhost"
	port     = 5432
	user     = "postgres"
)

type Source struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Article struct {
	Title       string    `json:"title"`
	Author      string    `json:"author"`
	Source      Source    `json:"source"`
	PublishedAt string `json:"publishedAt"`
	URL         string    `json:"url"`
}

type NewsResponse struct {
	Status       string    `json:"status"`
	TotalResults int       `json:"totalResults"`
	Articles     []Article `json:"articles"`
} 

type NewPost struct {
	Id int 
	Post string
	User_id int
	Date string
	Likes int
	Date_created time.Time
	Img string
	Replies interface{driver.Valuer; sql.Scanner}
	PostReports interface{driver.Valuer; sql.Scanner}
	ReplyTo string

}


func main() {

	passwordByte, err := os.ReadFile("dbPassword.txt") //Cant be displaying this information publically
	if err != nil {
		fmt.Println(err)
	}

	password := string(passwordByte)


	dbnameByte, err := os.ReadFile("dbName.txt") //Cant be displaying this information publically
	if err != nil {
		fmt.Println(err)
	}

	dbname := string(dbnameByte)

	apiKeyByte, err := os.ReadFile("key.txt") //Cant be displaying this information publically
	if err != nil {
		fmt.Println(err)
	}

	apiKey := string(apiKeyByte)



	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
	
	// Open a database connection
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Check the connection
	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to the database")

	
	var apiURL string
	for {
	
		apiURL = fmt.Sprintf("https://newsapi.org/v2/top-headlines?country=gb&apiKey=%v", apiKey)

		
		testFile, err := http.Get(apiURL)
		if err != nil {
			fmt.Println(err)
		}

		body, err := io.ReadAll(testFile.Body)
		if err != nil {
			fmt.Println("Error reading response body:", err)
		return
	}
		var News NewsResponse
		err = json.Unmarshal(body, &News)
		if err != nil {
			fmt.Println(err)
		}

		stories := News.Articles
		

		for _, elem := range stories {
			post := fmt.Sprintf("%v \n Writen by %v from %v\n find full story at %v \n \n", elem.Title, elem.Author, elem.Source.Name, elem.URL)
			fmt.Println(post)

			timestamp := time.Now()
			timezone, err := time.LoadLocation("Europe/London")
			if err != nil {
				log.Fatal("Error loading timezone:", err)
			}

			currentTime := time.Now()
			formattedTime := currentTime.Format("Mon Jan 02 15:04:05 2006")

			fmt.Println("Formatted time:", formattedTime)




			var storyPost NewPost
			storyPost.Post = post
			storyPost.User_id = 25
			storyPost.Date = formattedTime
			storyPost.Likes = 0
			storyPost.Date_created = timestamp.In(timezone)
			storyPost.Img = "False"
			storyPost.Replies = pq.Array([]string{})
			storyPost.PostReports = pq.Array([]string{})
			storyPost.ReplyTo = "False"
			query := "INSERT INTO public.\"SIapp_posts\" (post, user_id, date, likes, date_created, img, replies, \"postReports\", \"replyTo\") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id"
			err = db.QueryRow(query, storyPost.Post, storyPost.User_id, storyPost.Date, storyPost.Likes, storyPost.Date_created, storyPost.Img, storyPost.Replies, storyPost.PostReports, storyPost.ReplyTo  ).Scan(&storyPost.Id)
			if err != nil {
				fmt.Println(err)
			}
			time.Sleep(15*time.Minute)
		}

	}
}
