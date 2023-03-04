<?php

class VulnerableClass {
    public $username;

    public function login() {
        $password = $_GET['password'];
        if ($password == 'password') {
            $this->username = $_GET['username'];
            return 'Welcome, ' . $this->username;
        } else {
            return 'Invalid password!';
        }
    }

    public function getInfo() {
        return 'Your username is: ' . $this->username;
    }

    public function vulnerableFunction() {
        $input = $_GET['input'];
        eval($input);
    }
}
