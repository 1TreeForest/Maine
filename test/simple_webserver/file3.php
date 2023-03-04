<?php
    class File3 {
        function process_input($input1, $input2){
            $input1 = strip_tags($input1);
            $input2 = strip_tags($input2);
            
            if($input1 == 'admin' && $input2 == 'password'){
                echo "Login successful!";
            }
            else{
                echo "Invalid login!";
            }
        }
    }
?>
