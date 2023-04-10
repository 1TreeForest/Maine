<?php
require_once 'coverage.php';
class File4
{
    function process_input4($username, $password, $pet)
    {
        $username = strip_tags($username);
        $password = strip_tags($password);
        $pet = strip_tags($pet);

        // Connect to database
        $dbconn = new mysqli('localhost', 'root', 'toor', 'maine_test');
        if ($dbconn->connect_error) {
            die("Connection failed: " . $dbconn->connect_error);
        }

        // Check if login credentials are valid
        $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
        $result = $dbconn->query($query);
        if ($result->num_rows > 0) {
            echo "Login successful!<br>";

            // Check if pet input exists in database
            try {
                $input_query = "SELECT * FROM pets WHERE pet_name = '$pet'";
                $input_result = $dbconn->query($input_query);
            } catch (mysqli_sql_exception $exception) {
                header("HTTP/1.1 500 Internal Server Error");
                echo "Error: " . $exception->getMessage();
            }
            if ($dbconn->error) {
                $error = "Query error: " . $dbconn->error;
                die($error);
            }
            if ($input_result->num_rows > 0) {
                $pet_info = $input_result->fetch_assoc();
                echo "Pet found!<br>";
                echo "Pet name: " . $pet_info['pet_name'] . "<br>";
                echo "Owner ID: " . $pet_info['owner_id'] . "<br>";
                echo "ID: " . $pet_info['id'] . "<br>";
            } else {
                echo "Pet not found!<br>";
            }
        } else {
            echo "Invalid login!<br>";
        }
        $dbconn->close();
    }
}
