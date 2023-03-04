<?php
    include('file1.php');
    include('file2.php');
    include('file3.php');
    if(isset($_GET['action'])){
        $action = $_GET['action'];
        if($action == 'file1'){
            $input = $_GET['input'];
            $file1 = new File1();
            $file1->process_input($input);
        }
        else if($action == 'file2'){
            $input = $_GET['input'];
            $file2 = new File2();
            $file2->process_input($input);
        }
        else if($action == 'file3'){
            $input1 = $_GET['input1'];
            $input2 = $_GET['input2'];
            $file3 = new File3();
            $file3->process_input($input1, $input2);
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