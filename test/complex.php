<?php
session_start();

// Set initial values for username and password
$username = '';
$password = '';

// Check if the user is already logged in
if(isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true){
    header('location: welcome.php');
    exit;
}

// Check if the form has been submitted
if($_SERVER['REQUEST_METHOD'] == 'POST'){
    // Check if the username and password are correct
    if($_POST['username'] == 'myusername' && $_POST['password'] == 'mypassword'){
        // Set session variables and redirect to welcome page
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $_POST['username'];
        header('location: welcome.php');
    }else{
        // Display error message if username or password is incorrect
        $error = 'Invalid username or password';
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <?php if(isset($error)){ echo "<p>$error</p>"; } ?>
    <form method="post">
        <label for="username">Username:</label>
        <input type="text" name="username" value="<?php echo htmlspecialchars($username); ?>" required>
        <br>
        <label for="password">Password:</label>
        <input type="password" name="password" value="<?php echo htmlspecialchars($password); ?>" required>
        <br>
        <button type="submit">Login</button>
    </form>
    <?php if(isset($_SESSION['message'])) { echo "<p>{$_SESSION['message']}</p>"; unset($_SESSION['message']); } ?>
</body>
</html>

<?php
// Logout function
if(isset($_GET['action']) && $_GET['action'] == 'logout'){
    // Unset session variables and redirect to login page
    $_SESSION = array();
    session_destroy();
    header('location: login.php');
}
?>
