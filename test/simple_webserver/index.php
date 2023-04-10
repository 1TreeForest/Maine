<?php
require_once('coverage.php');
include('file1.php');
include('file2.php');
include('file3.php');
include('file4.php');
if (isset($_GET['action'])) {
    $action = $_GET['action'];
    if ($action == 'file1') {
        $input = $_GET['input'];
        $file1 = new File1();
        $file1->process_input1($input);
    } else if ($action == 'file2') {
        $input = $_GET['input'];
        $file2 = new File2();
        $file2->process_input2($input);
    } else if ($action == 'file3') {
        $input1 = $_GET['input1'];
        $input2 = $_GET['input2'];
        $file3 = new File3();
        $file3->process_input3($input1, $input2);
    } else if ($action == 'file4') {
        $username = $_GET['input1'];
        $password = $_GET['input2'];
        $pet = $_GET['input3'];
        $file4 = new File4();
        $file4->process_input4($username, $password, $pet);
    }
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>Welcome to my website</title>
</head>

<body>
    <h1>Hello World!</h1>
    <p>This is a simple PHP page.</p>
</body>

</html>