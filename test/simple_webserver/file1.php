<?php
    class File1 {
        function process_input($input){
            $input = strip_tags($input);
            include('file2.php');
            $file2 = new File2();
            $file2->process_input($input);
        }
    }
?>
